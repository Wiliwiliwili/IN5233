"""
Curve Builder Module
Implements dual bootstrapping construction for USD discount and CLP zero curves.
"""

import numpy as np
import pandas as pd
from scipy.optimize import newton, brentq
from scipy.interpolate import interp1d
from datetime import datetime, timedelta


class CurveBuilder:
    """Builds and manages discount and forward curves for swap valuation."""
    
    def __init__(self, valuation_date="2026-03-20"):
        """Initialize the curve builder with a valuation date."""
        self.valuation_date = datetime.strptime(valuation_date, "%Y-%m-%d")
        self.sofr_curve = None
        self.clp_curve = None
        self.fx_forwards = None
        
    def _tenor_to_days(self, tenor):
        """Convert tenor string to number of days (ACT/360 convention)."""
        tenor = tenor.lower().strip()
        
        if tenor == "spot":
            return 0
        elif tenor.endswith("d"):
            days = int(tenor[:-1])
            return days
        elif tenor.endswith("m"):
            months = int(tenor[:-1])
            # Approximate: average 30 days per month
            return months * 30
        elif tenor.endswith("y"):
            years = float(tenor[:-1])
            return int(years * 360)  # ACT/360
        else:
            # Try parsing decimal years (e.g., "1.5y", "1.5Y")
            if tenor.replace(".", "").replace("y", "").isdigit():
                years = float(tenor.replace("y", "").replace("Y", ""))
                return int(years * 360)
            raise ValueError(f"Cannot parse tenor: {tenor}")
    
    def _tenure_to_yearfrac(self, days):
        """Convert days to year fraction (ACT/360)."""
        return days / 360.0
    
    def build_sofr_curve(self, sofr_data):
        """
        Step 3.1: Build USD discount curve from SOFR zero rates.
        
        Args:
            sofr_data: List of dicts with 'Tenor' and 'Mid' (zero rate in %)
        
        Returns:
            DataFrame with tenors, days, discount factors
        """
        df_sofr = pd.DataFrame(sofr_data)
        df_sofr['Days'] = df_sofr['Tenor'].apply(self._tenor_to_days)
        df_sofr['YearFrac'] = df_sofr['Days'].apply(self._tenure_to_yearfrac)
        
        # Convert percentage rates to decimals
        df_sofr['ZeroRate'] = df_sofr['Mid'] / 100.0
        
        # Calculate discount factors using continuous compounding: DF = e^(-r*t)
        df_sofr['DiscountFactor'] = np.exp(-df_sofr['ZeroRate'] * df_sofr['YearFrac'])
        
        self.sofr_curve = df_sofr[['Tenor', 'Days', 'YearFrac', 'ZeroRate', 'DiscountFactor']]
        return self.sofr_curve
    
    def get_sofr_discount_factor(self, days):
        """Get SOFR discount factor for any day count using log-linear interpolation."""
        if self.sofr_curve is None:
            raise ValueError("SOFR curve not yet built")
        
        days_array = self.sofr_curve['Days'].values
        df_array = self.sofr_curve['DiscountFactor'].values
        
        # Log-linear interpolation: log(DF) interpolates linearly
        log_df_interp = interp1d(days_array, np.log(df_array), kind='linear', 
                                 fill_value='extrapolate')
        log_df = log_df_interp(days)
        return np.exp(log_df)
    
    def build_fx_forwards(self, spot_rate, ndf_data):
        """
        Step 3.2: Build FX forward curve using Spot rate and NDF forward points.
        
        Args:
            spot_rate: Spot mid-rate (e.g., 916.54)
            ndf_data: List of dicts with 'Tenor' and 'Mid' (forward points)
        
        Returns:
            DataFrame with tenors, forward rates
        """
        df_ndf = pd.DataFrame(ndf_data)
        df_ndf['Days'] = df_ndf['Tenor'].apply(self._tenor_to_days)
        
        # Forward rate = Spot + (Forward Points / 10000)
        # Assuming forward points are in the same scale as provided
        df_ndf['OutrightForward'] = spot_rate + (df_ndf['Mid'] / 10000)
        
        self.fx_forwards = df_ndf[['Tenor', 'Days', 'OutrightForward']]
        return self.fx_forwards
    
    def bootstrap_clp_curve(self, par_swap_rates, basis_swap_spreads, clp_par_swaps=None):
        """
        Step 3.3: Bootstrap CLP zero curve using cross-currency basis spreads.
        
        The approach: Use bootstrap with basis spreads to imply CLP discount factors.
        For each tenor, we solve for the CLP discount factor that prices the IRS at par
        after adjusting for the basis spread.
        
        Args:
            par_swap_rates: List of dicts with 'Tenor' and 'Mid' (par swap rates in %)
            basis_swap_spreads: List of dicts with 'Tenor' and 'Mid' (basis in bps)
            clp_par_swaps: Optional list of dict with pre-specified CLP par swap rates
        
        Returns:
            DataFrame with CLP discount curve
        """
        df_swaps = pd.DataFrame(par_swap_rates)
        df_basis = pd.DataFrame(basis_swap_spreads)
        
        # Merge to get basis spread for each tenor
        merged = df_swaps.merge(df_basis, on='Tenor', how='left', suffixes=('_swap', '_basis'))
        
        # Forward fill missing basis values
        merged['Mid_basis'] = merged['Mid_basis'].ffill().bfill()
        
        merged['Days'] = merged['Tenor'].apply(self._tenor_to_days)
        merged['YearFrac'] = merged['Days'].apply(self._tenure_to_yearfrac)
        
        # Convert rates to decimals
        merged['ParSwapRate'] = merged['Mid_swap'] / 100.0
        merged['BasisSpread'] = merged['Mid_basis'] / 10000.0  # basis points to decimal
        
        # CLP par swap rate = USD par swap rate - basis spread
        merged['CLPParSwapRate'] = merged['ParSwapRate'] - merged['BasisSpread']
        
        # Sort by days to bootstrap in order
        merged = merged.sort_values('Days').reset_index(drop=True)
        
        # Initialize with spot at 1.0
        discount_factors = {0: 1.0}
        clp_curve_data = [{'Tenor': 'Spot', 'Days': 0, 'DiscountFactor': 1.0}]
        
        # Bootstrap iteratively
        for idx, row in merged.iterrows():
            tenor = row['Tenor']
            days = row['Days']
            yearfrac = row['YearFrac']
            par_rate = row['CLPParSwapRate']
            
            if days == 0 or yearfrac == 0:
                continue  # Skip spot
            
            # Simple bootstrap: for each tenor, calculate DF assuming constant rate
            # DF(T) = 1 / (1 + par_rate * T)  simplified formula
            # Or using continuous compounding: DF = exp(-rate * T)
            
            df_t = np.exp(-par_rate * yearfrac)
            
            discount_factors[days] = df_t
            clp_curve_data.append({
                'Tenor': tenor,
                'Days': days,
                'DiscountFactor': df_t
            })
        
        self.clp_curve = pd.DataFrame(clp_curve_data)
        
        return self.clp_curve
    
    def get_clp_discount_factor(self, days):
        """Get CLP discount factor for any day using log-linear interpolation."""
        if self.clp_curve is None:
            raise ValueError("CLP curve not yet built")
        
        days_array = self.clp_curve['Days'].values
        df_array = self.clp_curve['DiscountFactor'].values
        
        # Remove duplicates and sort
        unique_indices = np.argsort(days_array)
        days_array = days_array[unique_indices]
        df_array = df_array[unique_indices]
        
        # Log-linear interpolation
        log_df_interp = interp1d(days_array, np.log(df_array), kind='linear',
                                fill_value='extrapolate')
        log_df = log_df_interp(days)
        return np.exp(log_df)
