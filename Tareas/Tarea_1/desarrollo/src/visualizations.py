"""
Visualization Module
Generates comprehensive charts for the Swap Portfolio Analysis Report
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Load data
data_path = Path("Tareas/Tarea_1/desarrollo/data/cartera_de_swaps.json")
with open(data_path, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Create output directory
output_dir = Path("Tareas/Tarea_1/desarrollo/visualizations")
output_dir.mkdir(exist_ok=True)

# =============================================================================
# 1. PORTFOLIO COMPOSITION - PIE CHART
# =============================================================================
def create_portfolio_composition():
    """Pie chart of notional distribution by swap."""
    swaps = raw_data['cartera_de_swaps']
    labels = [f"Swap #{s['Nº Oper Sistema']}\n({s['Contraparte']})" for s in swaps]
    sizes = [s['Nominal Inicial'] / 1e9 for s in swaps]  # Convert to billions
    colors = ['#2ecc71', '#e74c3c', '#3498db', '#f39c12']
    explode = (0.05, 0, 0.05, 0)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                        colors=colors, explode=explode,
                                        startangle=90, textprops={'fontsize': 11})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
        autotext.set_fontsize(10)
    
    ax.set_title('Portfolio Composition by Notional\nTotal: CLP 16.0 Billion', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add legend with notional amounts
    legend_labels = [f"{l.split('\\n')[0]}: CLP {s:.1f}B" 
                     for l, s in zip(labels, sizes)]
    ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / '01_portfolio_composition.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Portfolio Composition")

# =============================================================================
# 2. NPV BY SWAP - BAR CHART
# =============================================================================
def create_npv_by_swap():
    """Bar chart showing NPV for each swap."""
    npv_data = {
        'Swap #1105': 538.9,
        'Swap #1107': -70.4,
        'Swap #1323': -627.8,
        'Swap #1324': -310.2
    }
    
    swaps = list(npv_data.keys())
    npvs = list(npv_data.values())
    colors = ['green' if x > 0 else 'red' for x in npvs]
    
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.bar(swaps, npvs, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels on bars
    for bar, npv in zip(bars, npvs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'CLP {npv:.1f}M',
                ha='center', va='bottom' if height > 0 else 'top', 
                fontweight='bold', fontsize=11)
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax.set_ylabel('NPV (CLP Millions)', fontsize=12, fontweight='bold')
    ax.set_title('Net Present Value (NPV) by Swap\nValuation Date: March 20, 2026', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    # Add portfolio total
    total_npv = sum(npvs)
    ax.text(0.98, 0.97, f'Portfolio Total: CLP {total_npv:.1f}M',
            transform=ax.transAxes, fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
            verticalalignment='top', horizontalalignment='right')
    
    plt.tight_layout()
    plt.savefig(output_dir / '02_npv_by_swap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: NPV by Swap")

# =============================================================================
# 3. STRESS TESTING RESULTS
# =============================================================================
def create_stress_test_results():
    """Waterfall chart showing stress test scenarios."""
    scenarios = ['Baseline', 'Parallel Up', 'Parallel Down', 'Steepening', 
                'Flattening', 'Short Up', 'Short Down']
    npvs = [-469.5, -1269.5, 330.5, -249.5, -689.5, -529.5, -409.5]
    changes = [-800.0, 800.0, 220.0, -220.0, -60.0, 60.0]
    
    colors_map = {
        'Baseline': '#3498db',
        'Parallel Up': '#e74c3c',
        'Parallel Down': '#2ecc71',
        'Steepening': '#2ecc71',
        'Flattening': '#e74c3c',
        'Short Up': '#f39c12',
        'Short Down': '#2ecc71'
    }
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create grouped bar chart
    x_pos = np.arange(len(scenarios))
    colors = [colors_map[s] for s in scenarios]
    
    bars = ax.bar(x_pos, npvs, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    
    # Add value labels
    for i, (bar, npv) in enumerate(zip(bars, npvs)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{npv:.0f}M',
                ha='center', va='bottom' if height > 0 else 'top',
                fontweight='bold', fontsize=10)
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels(scenarios, rotation=45, ha='right')
    ax.set_ylabel('Portfolio NPV (CLP Millions)', fontsize=12, fontweight='bold')
    ax.set_title('Regulatory Stress Testing Results - CMF RAN 21-13\n6 Scenarios Impact on Portfolio NPV',
                 fontsize=14, fontweight='bold', pad=20)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
    ax.grid(axis='y', alpha=0.3)
    
    # Add annotations for worst and best case
    worst_idx = npvs.index(min(npvs))
    best_idx = npvs.index(max(npvs))
    
    ax.annotate('WORST\nCASE', xy=(worst_idx, npvs[worst_idx]), 
                xytext=(worst_idx, npvs[worst_idx]-150),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=11, fontweight='bold', color='red',
                ha='center')
    
    ax.annotate('BEST\nCASE', xy=(best_idx, npvs[best_idx]),
                xytext=(best_idx, npvs[best_idx]+150),
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                fontsize=11, fontweight='bold', color='green',
                ha='center')
    
    plt.tight_layout()
    plt.savefig(output_dir / '03_stress_test_results.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Stress Test Results")

# =============================================================================
# 4. SENSITIVITY ANALYSIS - TORNADO CHART
# =============================================================================
def create_sensitivity_analysis():
    """Tornado chart showing DV01 sensitivity."""
    factors = ['100 bps Up', '100 bps Down', 'Curve Steep', 'Curve Flat', 
               'Short Up', 'Short Down']
    low_impact = [-800, 0, 0, -220, -60, 0]
    high_impact = [0, 800, 220, 0, 0, 60]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    y_pos = np.arange(len(factors))
    
    # Create horizontal bars
    ax.barh(y_pos, low_impact, left=0, color='#e74c3c', alpha=0.7, 
            edgecolor='black', linewidth=1.5, label='Downside')
    ax.barh(y_pos, high_impact, left=0, color='#2ecc71', alpha=0.7,
            edgecolor='black', linewidth=1.5, label='Upside')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(factors)
    ax.set_xlabel('NPV Impact (CLP Millions)', fontsize=12, fontweight='bold')
    ax.set_title('Sensitivity Analysis - Stress Scenario Impact\nDV01 Analysis: CLP 8M per basis point',
                 fontsize=14, fontweight='bold', pad=20)
    ax.axvline(x=0, color='black', linestyle='-', linewidth=2)
    ax.grid(axis='x', alpha=0.3)
    ax.legend(loc='lower right', fontsize=11)
    
    # Add value labels
    for i, (low, high) in enumerate(zip(low_impact, high_impact)):
        if low != 0:
            ax.text(low-50, i, f'{low:.0f}M', ha='right', va='center', 
                   fontweight='bold', fontsize=10)
        if high != 0:
            ax.text(high+50, i, f'+{high:.0f}M', ha='left', va='center',
                   fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / '04_sensitivity_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Sensitivity Analysis")

# =============================================================================
# 5. YIELD CURVES COMPARISON
# =============================================================================
def create_yield_curves():
    """Plot USD (SOFR) vs CLP zero curves."""
    sofr_data = raw_data['curva_cero_sofr']
    
    # Parse data
    sofr_tenors = [t['Tenor'].replace('Y', '').replace('y', '') for t in sofr_data]
    sofr_rates = [t['Mid'] for t in sofr_data]
    
    # CLP curve (bootstrapped)
    clp_tenors = ['0.25', '0.5', '1', '1.5', '2', '3', '5', '10']
    clp_rates = [4.90, 5.44, 5.44, 5.60, 5.72, 5.82, 6.04, 6.59]
    
    # Par swap rates for reference
    par_tenors = [0.083, 0.167, 0.25, 0.5, 1, 1.5, 2, 3, 5, 10]
    par_rates = [4.650, 4.700, 4.750, 4.763, 4.850, 4.902, 5.000, 5.450, 5.610, 5.910]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot curves
    ax.plot(par_tenors, par_rates, marker='o', linewidth=2.5, markersize=7,
            label='USD Par Swap Rates', color='#3498db')
    ax.plot([float(t) for t in clp_tenors], clp_rates, marker='s', linewidth=2.5, 
            markersize=7, label='CLP Zero Curve', color='#e74c3c')
    
    # Convert SOFR tenors to years
    sofr_tenors_numeric = []
    for t in sofr_tenors:
        if 'm' in t.lower():
            months = float(t.lower().replace('m', ''))
            sofr_tenors_numeric.append(months / 12)
        else:
            sofr_tenors_numeric.append(float(t.lower().replace('y', '')))
    
    ax.plot(sofr_tenors_numeric, sofr_rates, marker='^', linewidth=2, 
            markersize=6, label='USD SOFR Curve', color='#27ae60', linestyle='--')
    
    ax.set_xlabel('Tenor (Years)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Yield / Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Yield Curve Comparison: USD vs CLP\nBaseline Curves as of March 20, 2026',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=11, loc='best')
    ax.grid(True, alpha=0.3)
    
    # Annotations for rates
    ax.text(10, 6.59, 'CLP 10Y: 6.59%', fontsize=10, bbox=dict(boxstyle='round', 
            facecolor='lightyellow', alpha=0.8))
    ax.text(10, 5.91, 'USD 10Y: 5.91%', fontsize=10, bbox=dict(boxstyle='round',
            facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_dir / '05_yield_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Yield Curves")

# =============================================================================
# 6. DISCOUNT FACTOR CURVES
# =============================================================================
def create_discount_curves():
    """Plot USD SOFR vs CLP discount factors."""
    sofr_data = raw_data['curva_cero_sofr']
    
    # Calculate DFs from zero rates
    sofr_tenors_years = []
    sofr_dfs = []
    
    tenor_map = {'1m': 1/12, '3m': 3/12, '6m': 6/12, '1y': 1, '2Y': 2, '3Y': 3,
                 '4Y': 4, '5Y': 5, '6Y': 6, '7Y': 7, '8Y': 8, '9Y': 9, '10Y': 10,
                 '15Y': 15, '20Y': 20}
    
    for t in sofr_data:
        tenor_str = t['Tenor'].lower()
        if tenor_str in tenor_map:
            years = tenor_map[tenor_str]
            rate = t['Mid'] / 100
            df = np.exp(-rate * years)
            sofr_tenors_years.append(years)
            sofr_dfs.append(df)
    
    # CLP DFs (from bootstrapping)
    clp_tenors_years = [0.25, 0.5, 1, 1.5, 2, 3, 5, 10]
    clp_dfs = [0.9724, 0.9469, 0.9469, 0.9207, 0.8932, 0.8354, 0.7405, 0.5315]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    ax.plot(sofr_tenors_years, sofr_dfs, marker='o', linewidth=2.5, markersize=7,
            label='USD SOFR Discount Factors', color='#3498db')
    ax.plot(clp_tenors_years, clp_dfs, marker='s', linewidth=2.5, markersize=7,
            label='CLP Discount Factors', color='#e74c3c')
    
    ax.set_xlabel('Tenor (Years)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Discount Factor', fontsize=12, fontweight='bold')
    ax.set_ylim([0, 1.05])
    ax.set_title('Discount Factor Curves\nUSD SOFR vs CLP Zero Curve',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / '06_discount_curves.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Discount Curves")

# =============================================================================
# 7. BASIS SPREAD CURVE
# =============================================================================
def create_basis_spreads():
    """Plot cross-currency basis spreads."""
    basis_data = raw_data['basis_swap']
    
    tenors = []
    basis_spreads = []
    
    tenor_order = ['6M', '1Y', '18M', '2Y', '3Y', '4Y', '5Y', '6Y', '7Y', '8Y', 
                  '9Y', '10Y', '12Y', '15Y', '20Y', '25Y', '30Y']
    
    basis_dict = {b['Tenor']: b['Mid'] for b in basis_data}
    
    for tenor in tenor_order:
        if tenor in basis_dict:
            tenors.append(tenor)
            basis_spreads.append(basis_dict[tenor])
    
    # Convert to numeric x-axis
    tenor_years = [float(t.replace('M', ''))/12 if 'M' in t else float(t.replace('Y', '')) 
                   for t in tenors]
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Create bar chart with color gradient
    colors = ['#e74c3c' if b < -80 else '#f39c12' if b < -50 else '#3498db' 
              for b in basis_spreads]
    
    bars = ax.bar(range(len(tenors)), basis_spreads, color=colors, alpha=0.7,
                  edgecolor='black', linewidth=1.5)
    
    ax.set_xticks(range(len(tenors)))
    ax.set_xticklabels(tenors, rotation=45, ha='right')
    ax.set_ylabel('Basis Spread (bps)', fontsize=12, fontweight='bold')
    ax.set_title('Cross-Currency Basis Spreads (SOFR/Cámara 6M)\nNegative indicates CLP premium',
                 fontsize=14, fontweight='bold', pad=20)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, spread in zip(bars, basis_spreads):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{spread:.1f}',
                ha='center', va='top', fontsize=9, fontweight='bold')
    
    # Add legend
    red_patch = mpatches.Patch(color='#e74c3c', alpha=0.7, label='Very Negative (<-80 bps)')
    orange_patch = mpatches.Patch(color='#f39c12', alpha=0.7, label='Negative (-50 to -80 bps)')
    blue_patch = mpatches.Patch(color='#3498db', alpha=0.7, label='Better (-50 bps)')
    ax.legend(handles=[red_patch, orange_patch, blue_patch], fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / '07_basis_spreads.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Basis Spreads")

# =============================================================================
# 8. RATE COMPARISON - OLD VS NEW
# =============================================================================
def create_rate_comparison():
    """Compare locked rates vs current par rates."""
    swaps = raw_data['cartera_de_swaps']
    
    swap_ids = [f"Swap #{s['Nº Oper Sistema']}" for s in swaps]
    locked_rates = [100*s['Tasa Pasiva Fija'] if s['Tasa Pas']=='FIJO' 
                    else 100*s.get('Tasa Activa Fija', 4.0) for s in swaps]
    current_rates = [5.91, 5.91, 5.61, 5.61]  # Approximate par rates for tenors
    
    x = np.arange(len(swap_ids))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    bars1 = ax.bar(x - width/2, locked_rates, width, label='Locked Rate', 
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, current_rates, width, label='Current Par Rate',
                   color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.set_ylabel('Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Rate Lock Comparison: Locked vs Current Par Rates\nSource of Portfolio Losses',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(swap_ids)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels and spread annotations
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        h1 = bar1.get_height()
        h2 = bar2.get_height()
        
        ax.text(bar1.get_x() + bar1.get_width()/2., h1,
                f'{h1:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
        ax.text(bar2.get_x() + bar2.get_width()/2., h2,
                f'{h2:.2f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        # Spread annotation
        spread = h2 - h1
        ax.annotate('', xy=(i + width/2, h2), xytext=(i - width/2, h1),
                   arrowprops=dict(arrowstyle='<->', color='red', lw=2))
        ax.text(i, (h1 + h2)/2, f'+{spread:.0f} bps', fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
               ha='center', va='center')
    
    plt.tight_layout()
    plt.savefig(output_dir / '08_rate_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Rate Comparison")

# =============================================================================
# 9. MATURITY LADDER
# =============================================================================
def create_maturity_ladder():
    """Stacked bar chart of maturity profile."""
    swaps = raw_data['cartera_de_swaps']
    
    # Group by expiration
    expirations = {}
    for swap in swaps:
        exp_date = swap['Fecha Vencimiento']
        year = exp_date.split('-')[0]
        month = int(exp_date.split('-')[1])
        
        quarter = (month - 1) // 3 + 1
        label = f"{year} Q{quarter}"
        
        if label not in expirations:
            expirations[label] = []
        
        expirations[label].append({
            'Swap': f"#{swap['Nº Oper Sistema']}",
            'Notional': swap['Nominal Inicial'] / 1e9,
            'NPV': 400 if swap['Nº Oper Sistema'] == 1105 else -200  # Simplified
        })
    
    # Sort by date
    sorted_exp = sorted(expirations.items())
    labels = [label for label, _ in sorted_exp]
    notionals = [sum(s['Notional'] for s in swaps_list) for _, swaps_list in sorted_exp]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = range(len(labels))
    colors = ['#2ecc71', '#f39c12']
    
    ax.bar(x, notionals, color=colors[0], alpha=0.7, edgecolor='black', linewidth=2)
    
    for i, (notional, label) in enumerate(zip(notionals, labels)):
        ax.text(i, notional + 0.3, f'CLP {notional:.1f}B', ha='center', 
               fontweight='bold', fontsize=11)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel('Notional (CLP Billions)', fontsize=12, fontweight='bold')
    ax.set_title('Maturity Ladder / Portfolio Expiration Profile\nWhen do swaps terminate?',
                 fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3)
    
    # Highlight near-term expiration
    ax.text(0.5, 0.95, '⚠️ 38 days to expiration', transform=ax.transAxes,
           fontsize=12, fontweight='bold', color='red',
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9),
           verticalalignment='top', horizontalalignment='center')
    
    plt.tight_layout()
    plt.savefig(output_dir / '09_maturity_ladder.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Maturity Ladder")

# =============================================================================
# 10. COUNTERPARTY CONCENTRATION
# =============================================================================
def create_counterparty_concentration():
    """Show counterparty exposure distribution."""
    swaps = raw_data['cartera_de_swaps']
    
    counterparties = {}
    for swap in swaps:
        bank = swap['Contraparte']
        if bank not in counterparties:
            counterparties[bank] = {'notional': 0, 'npv': 0}
        counterparties[bank]['notional'] += swap['Nominal Inicial'] / 1e9
    
    # Add NPV values
    counterparties['BANCO 1']['npv'] = 539
    counterparties['BANCO 2']['npv'] = -381
    counterparties['BANCO 3']['npv'] = -628
    
    banks = list(counterparties.keys())
    notionals = [counterparties[b]['notional'] for b in banks]
    npvs = [counterparties[b]['npv'] for b in banks]
    percentages = [n/sum(notionals)*100 for n in notionals]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left: Notional pie
    colors = ['#f39c12', '#e74c3c', '#3498db']
    wedges, texts, autotexts = ax1.pie(notionals, labels=banks, autopct='%1.1f%%',
                                        colors=colors, explode=[0.05]*3,
                                        startangle=90, textprops={'fontsize': 11})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_weight('bold')
    
    ax1.set_title('Counterparty Concentration by Notional\nMax Safe Limit: 40%',
                  fontsize=12, fontweight='bold', pad=20)
    
    # Add legend
    legend_labels = [f"{b}: CLP {n:.1f}B ({p:.1f}%)"
                    for b, n, p in zip(banks, notionals, percentages)]
    ax1.legend(legend_labels, fontsize=10)
    
    # Right: Notional and NPV bars
    x = np.arange(len(banks))
    width = 0.35
    
    ax2_2 = ax2.twinx()
    
    bars1 = ax2.bar(x - width/2, notionals, width, label='Notional',
                   color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax2_2.bar(x + width/2, npvs, width, label='NPV',
                     color=['green' if n > 0 else 'red' for n in npvs],
                     alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax2.set_ylabel('Notional (CLP Billions)', fontsize=11, fontweight='bold')
    ax2_2.set_ylabel('NPV (CLP Millions)', fontsize=11, fontweight='bold')
    ax2.set_title('Counterparty Exposure & NPV Impact',
                  fontsize=12, fontweight='bold', pad=20)
    ax2.set_xticks(x)
    ax2.set_xticklabels(banks)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}B', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    for bar in bars2:
        height = bar.get_height()
        ax2_2.text(bar.get_x() + bar.get_width()/2., height,
                  f'{height:.0f}M', ha='center', va='bottom' if height > 0 else 'top',
                  fontsize=9, fontweight='bold')
    
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / '10_counterparty_concentration.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Created: Counterparty Concentration")

# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS FOR SWAP PORTFOLIO ANALYSIS REPORT")
    print("="*70 + "\n")
    
    create_portfolio_composition()
    create_npv_by_swap()
    create_stress_test_results()
    create_sensitivity_analysis()
    create_yield_curves()
    create_discount_curves()
    create_basis_spreads()
    create_rate_comparison()
    create_maturity_ladder()
    create_counterparty_concentration()
    
    print("\n" + "="*70)
    print("✓ ALL VISUALIZATIONS GENERATED SUCCESSFULLY")
    print(f"  Location: {output_dir}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
