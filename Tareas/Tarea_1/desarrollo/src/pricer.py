import numpy as np
import pandas as pd
from datetime import datetime

try:
    from .curve_builder import CurveBuilder
except ImportError:
    from curve_builder import CurveBuilder


class SwapPricer:
    """Prices individual swaps and portfolios."""
    
    def __init__(self, curve_builder, valuation_date="2026-03-20"):
        """
        Initialize the pricer.
        
        Args:
            curve_builder: CurveBuilder instance with calibrated curves
            valuation_date: Valuation date as string "YYYY-MM-DD"
        """
        self.curve_builder = curve_builder
        self.valuation_date = datetime.strptime(valuation_date, "%Y-%m-%d")
    
    def _parse_date(self, date_str):
        """Parse date string to datetime object."""
        if isinstance(date_str, str):
            return datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    
    def _calc_days(self, date1, date2):
        """Calculate days between two dates (ACT/360)."""
        delta = date2 - date1
        return delta.days
    
    def _generate_schedule(self, start_date, end_date, frequency='6M'):
        """
        Generate coupon payment schedule.
        
        Args:
            start_date: Effective date
            end_date: Maturity date
            frequency: Payment frequency ('6M', '1Y', etc.)
        
        Returns:
            List of tuples (accrual_start, accrual_end, days)
        """
        schedule = []
        
        # Parse frequency
        if frequency == '6M':
            months = 6
        elif frequency == '1Y':
            months = 12
        elif frequency == '3M':
            months = 3
        else:
            months = 6  # Default to 6M
        
        current_date = self._parse_date(start_date)
        end = self._parse_date(end_date)
        
        while current_date < end:
            # Calculate next coupon date
            month = current_date.month + months
            year = current_date.year + (month - 1) // 12
            month = ((month - 1) % 12) + 1
            
            next_date = current_date.replace(year=year, month=month)
            if next_date > end:
                next_date = end
            
            days = self._calc_days(current_date, next_date)
            schedule.append((current_date, next_date, days))
            
            current_date = next_date
            if current_date >= end:
                break
        
        return schedule
    
    def value_fixed_leg(self, nominal, fixed_rate, start_date, end_date, 
                        frequency='6M', curve_getter=None):
        """
        Value fixed rate leg of swap.
        
        Args:
            nominal: Nominal amount
            fixed_rate: Fixed rate (as decimal, e.g., 0.0405 for 4.05%)
            start_date: Effective date
            end_date: Maturity date
            frequency: Payment frequency
            curve_getter: Function to get discount factor for days (uses CLP by default)
        
        Returns:
            Present value of fixed leg
        """
        if curve_getter is None:
            curve_getter = self.curve_builder.get_clp_discount_factor
        
        schedule = self._generate_schedule(start_date, end_date, frequency)
        pv = 0.0
        
        # If no valid schedule, estimate simply
        if not schedule:
            days_to_maturity = self._calc_days(self.valuation_date, self._parse_date(end_date))
            if days_to_maturity <= 0:
                return nominal  # No time value
            
            yearfrac = days_to_maturity / 360.0
            try:
                df_maturity = curve_getter(days_to_maturity)
            except:
                # Fallback: simple discount
                df_maturity = 1.0 / (1.0 + fixed_rate * yearfrac)
            
            # Simple coupon approximation
            coupon = nominal * fixed_rate * yearfrac
            pv = coupon * df_maturity + nominal * df_maturity
            return pv
        
        for accrual_start, accrual_end, days in schedule:
            # Days fraction (ACT/360)
            yearfrac = days / 360.0
            
            # Discount factor from valuation date
            days_to_end = self._calc_days(self.valuation_date, accrual_end)
            
            if days_to_end <= 0:
                df = 1.0
            else:
                try:
                    df = curve_getter(days_to_end)
                except:
                    df = 1.0 / (1.0 + fixed_rate * yearfrac)
            
            # Fixed coupon: Nominal * Rate * YearFrac
            coupon = nominal * fixed_rate * yearfrac
            cash_flow_pv = coupon * df
            pv += cash_flow_pv
        
        # Final notional payment
        days_to_maturity = self._calc_days(self.valuation_date, self._parse_date(end_date))
        if days_to_maturity > 0:
            try:
                df_maturity = curve_getter(days_to_maturity)
            except:
                yearfrac = days_to_maturity / 360.0
                df_maturity = 1.0 / (1.0 + fixed_rate * yearfrac)
            pv += nominal * df_maturity
        else:
            pv += nominal
        
        return pv
    
    def value_floating_leg(self, nominal, forward_rates, start_date, end_date,
                          frequency='6M', curve_getter=None, spread=0.0):
        """
        Value floating rate leg of swap.
        
        Args:
            nominal: Nominal amount
            forward_rates: Dict mapping tenor to forward rate (as decimal)
            start_date: Effective date
            end_date: Maturity date
            frequency: Payment frequency
            curve_getter: Function to get discount factor for days
            spread: Any spread over floating rate
        
        Returns:
            Present value of floating leg
        """
        if curve_getter is None:
            curve_getter = self.curve_builder.get_clp_discount_factor
        
        schedule = self._generate_schedule(start_date, end_date, frequency)
        pv = 0.0
        
        # Extract forward rate
        if isinstance(forward_rates, dict):
            fwd_rate = list(forward_rates.values())[0] if forward_rates else 0.04
        else:
            fwd_rate = forward_rates
        
        # If no valid schedule
        if not schedule:
            days_to_maturity = self._calc_days(self.valuation_date, self._parse_date(end_date))
            if days_to_maturity <= 0:
                return nominal  # No time value
            
            yearfrac = days_to_maturity / 360.0
            try:
                df_maturity = curve_getter(days_to_maturity)
            except:
                df_maturity = 1.0 / (1.0 + fwd_rate * yearfrac)
            
            coupon = nominal * (fwd_rate + spread) * yearfrac
            pv = coupon * df_maturity + nominal * df_maturity
            return pv
        
        for accrual_start, accrual_end, days in schedule:
            yearfrac = days / 360.0
            
            # Discount factor
            days_to_end = self._calc_days(self.valuation_date, accrual_end)
            
            if days_to_end <= 0:
                df = 1.0
            else:
                try:
                    df = curve_getter(days_to_end)
                except:
                    df = 1.0 / (1.0 + fwd_rate * yearfrac)
            
            # Floating coupon
            coupon = nominal * (fwd_rate + spread) * yearfrac
            cash_flow_pv = coupon * df
            pv += cash_flow_pv
        
        # Final notional payment
        days_to_maturity = self._calc_days(self.valuation_date, self._parse_date(end_date))
        if days_to_maturity > 0:
            try:
                df_maturity = curve_getter(days_to_maturity)
            except:
                yearfrac = days_to_maturity / 360.0
                df_maturity = 1.0 / (1.0 + fwd_rate * yearfrac)
            pv += nominal * df_maturity
        else:
            pv += nominal
        
        return pv
    
    def price_swap(self, swap_data):
        """
        Price a single swap.
        
        Args:
            swap_data: Dictionary with swap details
                - Nominal Inicial: Nominal amount
                - Tasa Activa Fija: Active fixed rate (%)
                - Tasa Pasiva Fija: Passive fixed rate (%)
                - Tasa Activa Variable: Active floating rate (%)
                - Tasa Pasiva Variable: Passive floating rate (%)
                - Fecha Cierre: Start date
                - Fecha Vencimiento: End date
                - Tasa Act: Type of active leg ('FIJO' or rate type)
                - Tasa Pas: Type of passive leg ('FIJO' or rate type)
        
        Returns:
            Dictionary with valuation results
        """
        nominal = swap_data['Nominal Inicial']
        start_date = swap_data['Fecha Cierre']
        end_date = swap_data['Fecha Vencimiento']
        
        # Determine legs
        # Active leg (Receiving)
        if swap_data['Tasa Act'] == 'FIJO':
            # Fixed active leg
            active_pv = self.value_fixed_leg(
                nominal, 
                swap_data['Tasa Activa Fija'] / 100.0,
                start_date, 
                end_date
            )
        else:
            # Floating active leg (ICP, Camara, etc.)
            # Use the variable rate provided as proxy for forward
            active_pv = self.value_floating_leg(
                nominal,
                {'default': swap_data['Tasa Activa Variable'] / 100.0},
                start_date,
                end_date
            )
        
        # Passive leg (Paying)
        if swap_data['Tasa Pas'] == 'FIJO':
            # Fixed passive leg
            passive_pv = self.value_fixed_leg(
                nominal,
                swap_data['Tasa Pasiva Fija'] / 100.0,
                start_date,
                end_date
            )
        else:
            # Floating passive leg
            passive_pv = self.value_floating_leg(
                nominal,
                {'default': swap_data['Tasa Pasiva Variable'] / 100.0},
                start_date,
                end_date
            )
        
        # Net value: Receiving leg - Paying leg
        npv = active_pv - passive_pv
        
        return {
            'Nº_Oper': swap_data['Nº Oper Sistema'],
            'Nominal': nominal,
            'Active_PV': active_pv,
            'Passive_PV': passive_pv,
            'NPV': npv,
            'Start_Date': start_date,
            'End_Date': end_date
        }
    
    def price_portfolio(self, swaps_data):
        """
        Price entire swap portfolio.
        
        Args:
            swaps_data: List of swap dictionaries
        
        Returns:
            Tuple of (list of results, total portfolio NPV)
        """
        results = []
        total_npv = 0.0
        
        for swap in swaps_data:
            swap_result = self.price_swap(swap)
            results.append(swap_result)
            total_npv += swap_result['NPV']
        
        return results, total_npv
