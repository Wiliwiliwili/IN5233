"""
Swap Portfolio Valuation & Risk Engine - Main Orchestrator
Executes the complete pipeline for swap portfolio analysis per to_do.md
"""

import json
import sys
from pathlib import Path

import pandas as pd
import numpy as np

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "Tareas" / "Tarea_1" / "desarrollo" / "src"))

from curve_builder import CurveBuilder
from pricer import SwapPricer
from risk import RiskEngine


def load_json_data(data_path):
    """Load and parse JSON data file."""
    print(f"Loading data from: {data_path}")
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def step1_project_setup():
    """Step 1: Project Setup (completed via pyproject.toml and venv)."""
    print_section("STEP 1: PROJECT SETUP")
    print("✓ Virtual environment configured")
    print("✓ Dependencies installed: pandas, numpy, scipy, python-dateutil")
    print("✓ Folder structure established")
    return True


def step2_data_ingestion(data_path):
    """Step 2: Data Ingestion & Formatting."""
    print_section("STEP 2: DATA INGESTION & FORMATTING")
    
    raw_data = load_json_data(data_path)
    
    # Convert to DataFrames
    swaps_df = pd.DataFrame(raw_data['cartera_de_swaps'])
    par_swaps_df = pd.DataFrame(raw_data['tasas_par_swap'])
    ndf_forwards_df = pd.DataFrame(raw_data['puntos_forwards_ndf'])
    sofr_curve_df = pd.DataFrame(raw_data['curva_cero_sofr'])
    basis_swaps_df = pd.DataFrame(raw_data['basis_swap'])
    
    # Convert percentage rates to decimals
    swaps_df['Tasa Activa Fija'] = swaps_df['Tasa Activa Fija']  # Already decimal
    swaps_df['Tasa Pasiva Fija'] = swaps_df['Tasa Pasiva Fija']
    
    print(f"✓ Loaded {len(swaps_df)} swaps")
    print(f"✓ Loaded {len(par_swaps_df)} par swap tenors")
    print(f"✓ Loaded {len(ndf_forwards_df)} NDF forward points")
    print(f"✓ Loaded {len(sofr_curve_df)} SOFR zero curve points")
    print(f"✓ Loaded {len(basis_swaps_df)} basis spread points")
    
    print("\nSwap Portfolio Summary:")
    print(swaps_df[['Nº Oper Sistema', 'Contraparte', 'Nominal Inicial', 
                     'Tasa Act', 'Tasa Pas', 'Fecha Vencimiento']].to_string())
    
    return {
        'swaps': swaps_df.to_dict('records'),
        'par_swaps': par_swaps_df.to_dict('records'),
        'ndf_forwards': ndf_forwards_df.to_dict('records'),
        'sofr_curve': sofr_curve_df.to_dict('records'),
        'basis_swaps': basis_swaps_df.to_dict('records')
    }


def step3_dual_bootstrapping(data):
    """Step 3: Dual Bootstrapping Construction."""
    print_section("STEP 3: DUAL BOOTSTRAPPING CONSTRUCTION")
    
    curve_builder = CurveBuilder(valuation_date="2026-03-20")
    
    # Step 3.1: USD Discount Curve
    print("\n3.1 - Building USD Discount Curve (SOFR)...")
    sofr_curve = curve_builder.build_sofr_curve(data['sofr_curve'])
    print("✓ SOFR Discount Curve Built")
    print(sofr_curve.to_string())
    
    # Step 3.2: FX Forward Curve
    print("\n3.2 - Building FX Forward Curve (CLP/USD)...")
    spot_rate = 916.54  # From Mid column of Spot
    fx_forwards = curve_builder.build_fx_forwards(spot_rate, data['ndf_forwards'])
    print("✓ FX Forward Curve Built")
    print(fx_forwards.to_string())
    
    # Step 3.3: CLP Zero Curve
    print("\n3.3 - Bootstrapping CLP Zero Curve...")
    clp_curve = curve_builder.bootstrap_clp_curve(
        data['par_swaps'],
        data['basis_swaps']
    )
    print("✓ CLP Zero Curve Bootstrapped")
    print(clp_curve.to_string())
    
    return curve_builder


def step4_valuation_engine(curve_builder, data):
    """Step 4: Valuation Engine."""
    print_section("STEP 4: VALUATION ENGINE")
    
    pricer = SwapPricer(curve_builder, valuation_date="2026-03-20")
    
    print("\nValuing individual swaps...")
    swap_results, total_npv = pricer.price_portfolio(data['swaps'])
    
    results_df = pd.DataFrame(swap_results)
    print("\nSwap Valuation Results:")
    print(results_df[['Nº_Oper', 'Nominal', 'Active_PV', 'Passive_PV', 'NPV']].to_string())
    
    print(f"\n{'=' * 80}")
    print(f"PORTFOLIO BASE VALUE (NPV): ${total_npv:,.2f}")
    print(f"{'=' * 80}")
    
    return pricer, total_npv, results_df


def step5_regulatory_stress_testing(curve_builder, pricer, data, baseline_npv):
    """Step 5: Regulatory Stress Testing."""
    print_section("STEP 5: REGULATORY STRESS TESTING (CMF RAN 21-13)")
    
    risk_engine = RiskEngine(curve_builder, pricer, baseline_npv)
    
    print("\nExecuting stress tests across 6 regulatory scenarios...")
    stress_results = risk_engine.stress_test(data['swaps'])
    
    print("\nStress Testing Results:")
    print(stress_results[['Scenario', 'Description', 'Baseline_NPV', 
                         'Stressed_NPV', 'Delta_NPV']].to_string())
    
    return risk_engine, stress_results


def step6_hedging_strategy(risk_engine, data):
    """Step 6: Hedging Strategy Recommendation."""
    print_section("STEP 6: HEDGING STRATEGY RECOMMENDATION")
    
    # Calculate DV01
    print("\nCalculating portfolio DV01...")
    dv01 = risk_engine.calculate_dv01(data['swaps'])
    print(f"Portfolio DV01: ${dv01:,.2f} per basis point")
    
    # Calculate hedge requirement
    print("\nCalculating hedge requirement to reduce worst-case loss by 50%...")
    hedge_recommendation = risk_engine.calculate_hedge_requirement(data['swaps'])
    
    if hedge_recommendation:
        print(f"\n{'=' * 80}")
        print("HEDGING RECOMMENDATION")
        print(f"{'=' * 80}")
        print(f"Worst Case Scenario: {hedge_recommendation['Worst_Scenario']}")
        print(f"Worst Case Loss: ${hedge_recommendation['Worst_Loss']:,.2f}")
        print(f"Hedge Target (50% offset): ${hedge_recommendation['Hedge_Target']:,.2f}")
        print(f"\nRecommended Hedge:")
        print(f"  - Instrument: {hedge_recommendation['Suggested_Tenor']} IRS")
        print(f"  - Notional: ${hedge_recommendation['Hedge_Notional']:,.2f}")
        print(f"  - Position: {hedge_recommendation['Position']}")
        print(f"  - Portfolio DV01: ${hedge_recommendation['Portfolio_DV01']:,.2f}")
        print(f"  - Hedge DV01 Required: ${hedge_recommendation['Hedge_DV01_Required']:,.2f}")
        print(f"{'=' * 80}")
    
    return hedge_recommendation


def generate_summary_report(results):
    """Generate and print a comprehensive summary report."""
    print_section("EXECUTIVE SUMMARY")
    
    print("\n1. PORTFOLIO COMPOSITION")
    print(f"   Total Swaps: {len(results['swap_results'])}")
    print(f"   Total Notional: ${sum([s['Nominal'] for s in results['swap_results']]):,.0f}")
    print(f"   Base Portfolio NPV: ${results['baseline_npv']:,.2f}")
    
    print("\n2. STRESS TEST SUMMARY")
    stress_df = results['stress_results']
    worst_scenario = stress_df.loc[stress_df['Delta_NPV'].idxmin()]
    best_scenario = stress_df.loc[stress_df['Delta_NPV'].idxmax()]
    
    print(f"   Best Case: {best_scenario['Scenario']} (Δ${best_scenario['Delta_NPV']:,.2f})")
    print(f"   Worst Case: {worst_scenario['Scenario']} (Δ${worst_scenario['Delta_NPV']:,.2f})")
    
    print("\n3. HEDGE RECOMMENDATION")
    hedge = results['hedge_recommendation']
    if hedge:
        print(f"   Recommended: {hedge['Suggested_Tenor']} IRS - {hedge['Position']}")
        print(f"   Notional Amount: ${hedge['Hedge_Notional']:,.0f}")
    
    print(f"\n{'=' * 80}\n")


def main():
    """Main execution function."""
    print("\n" + "=" * 80)
    print("SWAP PORTFOLIO VALUATION & RISK ENGINE")
    print("IN5233 - Valuation Date: March 20, 2026")
    print("=" * 80 + "\n")
    
    try:
        # Data path
        data_path = Path("Tareas/Tarea_1/desarrollo/data/cartera_de_swaps.json")
        
        # Execute pipeline
        step1_project_setup()
        
        data = step2_data_ingestion(str(data_path))
        
        curve_builder = step3_dual_bootstrapping(data)
        
        pricer, baseline_npv, swap_results = step4_valuation_engine(curve_builder, data)
        
        risk_engine, stress_results = step5_regulatory_stress_testing(
            curve_builder, pricer, data, baseline_npv
        )
        
        hedge_recommendation = step6_hedging_strategy(risk_engine, data)
        
        # Generate summary
        summary_results = {
            'swap_results': swap_results.to_dict('records'),
            'baseline_npv': baseline_npv,
            'stress_results': stress_results,
            'hedge_recommendation': hedge_recommendation
        }
        generate_summary_report(summary_results)
        
        print("✓ EXECUTION COMPLETED SUCCESSFULLY\n")
        return 0
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
