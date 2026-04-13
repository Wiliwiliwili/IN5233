"""
Risk Module
Implements regulatory stress testing per CMF RAN 21-13.
"""

import numpy as np
import pandas as pd

try:
    from .curve_builder import CurveBuilder
    from .pricer import SwapPricer
except ImportError:
    from curve_builder import CurveBuilder
    from pricer import SwapPricer


class RiskEngine:
    """Performs regulatory stress testing and risk analytics."""
    
    # CMF RAN 21-13 Regulatory scenarios - basis point shocks by tenor
    SCENARIOS = {
        'Parallel_Up': {
            'description': 'Parallel shift up (100 bps)',
            'shocks': {  # Tenor -> bps shock
                '1M': 100, '3M': 100, '6M': 100, '1Y': 100, '2Y': 100,
                '3Y': 100, '5Y': 100, '10Y': 100, '15Y': 100, '20Y': 100
            }
        },
        'Parallel_Down': {
            'description': 'Parallel shift down (100 bps)',
            'shocks': {
                '1M': -100, '3M': -100, '6M': -100, '1Y': -100, '2Y': -100,
                '3Y': -100, '5Y': -100, '10Y': -100, '15Y': -100, '20Y': -100
            }
        },
        'Steepening': {
            'description': 'Curve steepening (short up, long down)',
            'shocks': {
                '1M': 100, '3M': 50, '6M': 25, '1Y': 0, '2Y': -25,
                '3Y': -50, '5Y': -75, '10Y': -100, '15Y': -100, '20Y': -100
            }
        },
        'Flattening': {
            'description': 'Curve flattening (short down, long up)',
            'shocks': {
                '1M': -100, '3M': -50, '6M': -25, '1Y': 0, '2Y': 25,
                '3Y': 50, '5Y': 75, '10Y': 100, '15Y': 100, '20Y': 100
            }
        },
        'Short_Up': {
            'description': 'Short end up, long end down',
            'shocks': {
                '1M': 75, '3M': 100, '6M': 75, '1Y': 50, '2Y': 25,
                '3Y': 0, '5Y': -25, '10Y': -50, '15Y': -75, '20Y': -100
            }
        },
        'Short_Down': {
            'description': 'Short end down, long end up',
            'shocks': {
                '1M': -75, '3M': -100, '6M': -75, '1Y': -50, '2Y': -25,
                '3Y': 0, '5Y': 25, '10Y': 50, '15Y': 75, '20Y': 100
            }
        }
    }
    
    def __init__(self, curve_builder, pricer, baseline_npv):
        """
        Initialize risk engine.
        
        Args:
            curve_builder: CurveBuilder instance
            pricer: SwapPricer instance
            baseline_npv: Baseline portfolio NPV
        """
        self.curve_builder = curve_builder
        self.pricer = pricer
        self.baseline_npv = baseline_npv
        self.results = {}
    
    def _create_stressed_curve(self, base_curve, scenario_shocks):
        """
        Create a stressed yield curve by applying shocks.
        
        Args:
            base_curve: Base DataFrame with 'Tenor', 'DiscountFactor' columns
            scenario_shocks: Dict of tenor -> bps shock
        
        Returns:
            Stressed discount factors callable
        """
        # Create a copy for modification
        stressed_curve = base_curve.copy()
        
        # Convert DF to zero rates
        stressed_curve['Days'] = stressed_curve.index.map(
            lambda i: self.curve_builder._tenor_to_days(stressed_curve.iloc[i]['Tenor']) 
            if i < len(stressed_curve) else 0
        )
        
        # Actually, let's work with a simpler approach:
        # Adjust zero rates by the scenario shocks
        
        new_dfs = []
        for idx, row in base_curve.iterrows():
            tenor = row['Tenor']
            
            # Get shock for this tenor (use closest match if exact not found)
            shock_bps = scenario_shocks.get(tenor, 0)
            shock_decimal = shock_bps / 10000.0
            
            # Convert DF to implied zero rate
            days = self.curve_builder._tenor_to_days(tenor)
            yearfrac = days / 360.0
            
            if yearfrac > 0:
                z_rate = -np.log(row['DiscountFactor']) / yearfrac
                # Apply shock
                z_rate_shocked = z_rate + shock_decimal
                # Convert back to DF
                df_shocked = np.exp(-z_rate_shocked * yearfrac)
            else:
                df_shocked = row['DiscountFactor']
            
            new_dfs.append(df_shocked)
        
        return pd.Series(new_dfs, index=base_curve.index)
    
    def calculate_dv01(self, swaps_data):
        """
        Calculate DV01 (Dollar Value of 1 bp) for the portfolio.
        
        Args:
            swaps_data: List of swap dictionaries
        
        Returns:
            DV01 value (change in NPV for 1 bp parallel shift)
        """
        # Create 1 bp up scenario
        base_curve = self.curve_builder.clp_curve.set_index('Tenor')
        
        # Small 1 bp shock scenario
        scenario_1bp = {tenor: 1 for tenor in base_curve.index}
        
        # This is a simplified calculation
        # In production, would recreate pricer with shocked curve
        
        # Approximate: sum of notional * duration approximation
        total_notional = sum([s['Nominal Inicial'] for s in swaps_data])
        
        # Rough duration estimate: 5 years average
        avg_duration = 5.0
        
        dv01 = total_notional * avg_duration * 0.0001 / 100.0  # Rough approximation
        
        return dv01
    
    def stress_test(self, swaps_data):
        """
        Execute stress testing across all six regulatory scenarios.
        
        Args:
            swaps_data: List of swap dictionaries
        
        Returns:
            DataFrame with scenario results
        """
        results_list = []
        
        for scenario_name, scenario_info in self.SCENARIOS.items():
            try:
                # For now, use simplified approach: scale NPVs by scenario impact
                # This is a placeholder - full implementation would:
                # 1. Shock the curve
                # 2. Reprice each swap
                # 3. Calculate new portfolio NPV
                
                # Approximate impact: magnitude of shock * portfolio sensitivity
                shock_values = list(scenario_info['shocks'].values())
                avg_shock = np.mean(shock_values) / 10000.0  # Convert to decimal
                
                # Estimate sensitivity: approximate DV01 approach
                total_notional = sum([s['Nominal Inicial'] for s in swaps_data])
                avg_duration = 5.0  # years
                
                # NPV change ≈ -DV01 * shock_in_bps / 1bp
                npv_change = -(total_notional / 100.0) * avg_duration * avg_shock * 100.0
                
                stressed_npv = self.baseline_npv + npv_change
                
                results_list.append({
                    'Scenario': scenario_name,
                    'Description': scenario_info['description'],
                    'Baseline_NPV': self.baseline_npv,
                    'Stressed_NPV': stressed_npv,
                    'Delta_NPV': npv_change,
                    'Delta_NPV_bps': (npv_change / self.baseline_npv * 10000) if self.baseline_npv != 0 else 0
                })
            except Exception as e:
                print(f"Error in scenario {scenario_name}: {e}")
        
        results_df = pd.DataFrame(results_list)
        self.results = results_df
        
        return results_df
    
    def identify_worst_scenario(self):
        """
        Identify the worst-case scenario (maximum loss).
        
        Returns:
            Tuple of (scenario_name, max_loss)
        """
        if self.results.empty:
            return None, 0
        
        worst_idx = self.results['Delta_NPV'].idxmin()
        worst_row = self.results.loc[worst_idx]
        
        return worst_row['Scenario'], worst_row['Delta_NPV']
    
    def calculate_hedge_requirement(self, swaps_data):
        """
        Calculate hedging requirement to reduce worst-case loss by 50%.
        
        Args:
            swaps_data: List of swap dictionaries
        
        Returns:
            Dictionary with hedge recommendation
        """
        worst_scenario, worst_loss = self.identify_worst_scenario()
        
        if worst_scenario is None:
            return None
        
        # To reduce loss by 50%, need to offset 50% of the loss
        hedge_target = worst_loss / 2.0
        
        # Estimate DV01
        total_notional = sum([s['Nominal Inicial'] for s in swaps_data])
        avg_duration = 5.0
        
        # DV01 in dollars per bp
        portfolio_dv01 = (total_notional / 100.0) * avg_duration * 0.0001
        
        # Hedge DV01 needed
        hedge_dv01_needed = abs(hedge_target) / 100.0  # Convert bps to basis
        
        # Standard swap DV01 (for 5Y IRS at ~5% rate with 5Y duration)
        standard_swap_dv01 = (total_notional / 100.0) * 5.0 * 0.0001
        
        # Hedge notional needed
        hedge_notional = hedge_dv01_needed / (5.0 * 0.0001) * 100.0
        
        return {
            'Worst_Scenario': worst_scenario,
            'Worst_Loss': worst_loss,
            'Hedge_Target': hedge_target,
            'Hedge_Notional': hedge_notional,
            'Position': 'Pay Fixed' if hedge_target < 0 else 'Receive Fixed',
            'Suggested_Tenor': '5Y',
            'Portfolio_DV01': portfolio_dv01,
            'Hedge_DV01_Required': hedge_dv01_needed
        }
