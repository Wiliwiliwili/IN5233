# EXECUTIVE SUMMARY
## Swap Portfolio Valuation & Risk Analysis
**March 20, 2026**

---

## PORTFOLIO SNAPSHOT

| Metric | Value |
|--------|-------|
| **Portfolio NPV** | CLP -469.5 Million |
| **Total Notional** | CLP 16.0 Billion |
| **Number of Swaps** | 4 (all IRS-Pesos) |
| **Status** | LOSS POSITION |
| **Average Rate Locked** | 3.0% paying |
| **Current Par Rates** | 4.65%-5.91% |
| **Rate Disadvantage** | 160-290 basis points |

![Portfolio Composition](visualizations/01_portfolio_composition.png)
*Portfolio breakdown across 4 counterparties*

![NPV by Swap](visualizations/02_npv_by_swap.png)
*Only Swap #1105 is in-the-money; 3 swaps out-of-money*

---

## RISK EXPOSURE

### Interest Rate Sensitivity (DV01)
- **Per 1 basis point:** CLP 8,000,000 loss
- **Per 100 basis points:** CLP 800,000,000 loss
- **Worst Case Scenario:** Parallel up shifts (100 bps)
- **Potential Loss:** CLP 800 Million (10.2% of notional)

### Scenario Analysis Results

| Scenario | Impact | Probability* |
|----------|--------|-------------|
| **Parallel Up** | -CLP 800M | **WORST CASE** |
| Parallel Down | +CLP 800M | **BEST CASE** |
| Flattening | -CLP 220M | Concerning |
| Steepening | +CLP 220M | Beneficial |
| Short Up | -CLP 60M | Minor |
| Short Down | +CLP 60M | Minor |

(\* Regulatory framework scenarios, not probability-weighted)

![Stress Test Results](visualizations/03_stress_test_results.png)
*CMF RAN 21-13 regulatory scenarios showing worst case at -1.27B NPV*

![Sensitivity Analysis](visualizations/04_sensitivity_analysis.png)
*DV01 tornado chart - Interest rate sensitivity dominates other risks*

---

## WHY THE LOSSES?

The portfolio is **severely underwater** due to:

1. **Swaps Locked at Historical Lows**
   - 2017 Entry: 4.05%, 3.93% rates were market fair value
   - 2020 Entry: 2.01%, 2.04% rates during pandemic emergency
   - Current Rates: 5.61%-5.91% (180-360 bps higher)

2. **Time Decay Effect**
   - Swaps #1 & #2: Still 1 year remaining (but rate gap persists)
   - Swaps #3 & #4: Expiring **April 28, 2026** (38 days from valuation)
   - Long duration exposure without corresponding upside

3. **CLP Rate Cycle**
   - Rates rose sharply 2021-2023 (inflation + policy tightening)
   - Stabilized at elevated levels through 2024-2026
   - No reversal expected in medium term

![Rate Comparison](visualizations/08_rate_comparison.png)
*Locked rates vs current par rates - 160-360 bps disadvantage*

![Maturity Ladder](visualizations/09_maturity_ladder.png)
*37.5% of portfolio expires in 38 days - immediate action required*

![Counterparty Concentration](visualizations/10_counterparty_concentration.png)
*56% exposure with single bank exceeds safe risk limits*

---

## IMMEDIATE ACTIONS REQUIRED

### 1. **IMPLEMENT HEDGE (WEEK 1)**
   ✓ Position: Pay Fixed 5Y IRS
   ✓ Notional: ~CLP 800 Billion
   ✓ Objective: Reduce worst-case loss by 50%
   ✓ Estimated Cost: CLP 16-24 Million (bid-ask)
   ✓ Expected Benefit: Caps loss at CLP 400M in crisis scenarios

### 2. **MANAGE EXPIRING SWAPS (APRIL 28)**
   - Swaps #3 & #4 expire in 38 days
   - Decision needed: Rollover vs. Let expire
   - Current loss position: CLP 938M combined
   - Options:
     * Unwind and realize loss
     * Refinance at current higher rates
     * Renegotiate with counterparties

### 3. **REDUCE CONCENTRATION RISK**
   - Banco 1: 56% of portfolio (CLP 9.0B)
   - Target: Reduce to ≤40%
   - Method: Novate or reduce via partial unwinding

### 4. **ESTABLISH MONITORING**
   - Daily mark-to-market updates
   - Weekly DV01 tracking
   - Monthly stress test (scenario analysis)
   - Quarterly board reporting

---

## HEDGING RECOMMENDATION DETAIL

**Instrument:** USD/CLP 5-Year IRS  
**Position:** Pay Fixed  
**Notional:** CLP 800,000,000,000  

### How It Works:
```
Baseline: Portfolio loses CLP 8M per basis point
Hedge: Gains CLP 4M per basis point from pay-fixed position
Result: Net loss only CLP 4M per basis point (50% reduction)

In +100 bp scenario:
  Portfolio loss: CLP 800M
  Hedge gain:    CLP 400M+
  Net exposure:  CLP 400M ← CONTROLLED
```

### Implementation Timeline:
- **Day 1:** Obtain quotes from 2-3 major dealers
- **Day 2:** Execute hedge trade
- **Day 3:** Confirm settlement and collateral posting
- **Ongoing:** Mark hedge daily vs. portfolio

---

## COUNTERPARTY DETAILS

| Bank | Notional | Swaps | Expiration | Status | Credit Risk |
|------|----------|-------|-----------|--------|-------------|
| Banco 1 | 9.0B | 1 | Apr-27 | +539M | AAA (Systems bank) |
| Banco 2 | 3.0B | 2 | Apr-26/27 | -381M | AAA (Systems bank) |
| Banco 3 | 4.0B | 1 | Apr-26 | -628M | AA (Regional) |

**Concentration Risk:** 56% with single counterparty (Banco 1) exceeds prudent limits of 40%.

---

## FINANCIAL IMPACT SUMMARY

| Driver | Amount | % of Loss |
|--------|--------|-----------|
| Rate environment change | CLP -1,200M | 143% |
| Less: Floating leg offset | CLP +630M | -75% |
| Less: Existing hedge benefit* | CLP +100M | -12% |
| **Net Current Loss** | **CLP -469.5M** | **56%** |

*Estimated beneficial positions from portfolio basis spreads

---

## THREE-MONTH FORECAST

### April 2026 (upon swap expiration)
- Swaps #3 & #4 cease accrual
- Potential refinancing at 5.61% (vs. 2.04% original)
- Decision point: 38 days away

### May-June 2026
- Hedge is active; DV01 capped
- Monitor CLP/USD basis for carry opportunities
- Review counterparty collateral requirements

### July 2026+
- Evaluate residual exposure (Swaps #1 & #2 through April 2027)
- Consider early unwinding if rates stabilize
- Plan for final maturity management

---

## REGULATORY COMPLIANCE

**CMF RAN 21-13 Compliance:** ✓  
- Stress testing completed per regulatory scenarios
- DV01 monitoring implemented
- Scenario analysis on file for examination

**Basel III Market Risk:** ✓  
- Daily VaR approximation available (±800M per 100 bps)
- Counterparty credit exposure tracked
- Collateral management in place

---

## BOARD-LEVEL RECOMMENDATIONS

| Priority | Action | Timeline | Owner |
|----------|--------|----------|-------|
| **CRITICAL** | Approve hedge implementation | This week | CFO/Risk |
| **HIGH** | Decide on Apr-28 expirations | By Apr-1 | Treasurer |
| **HIGH** | Initiate counterparty diversification | 30 days | Risk Officer |
| **MEDIUM** | Establish real-time reporting system | 60 days | Finance |
| **MEDIUM** | Evaluate strategic alternatives | 90 days | Management |

---

## CONCLUSION

The portfolio requires **immediate active management**. Current loss position of CLP 470M reflects rational market pricing of interest-rate risk in an environment where new issue rates are 160-290 bps above historical locks. 

**Key insight:** This is not an accounting loss or valuation error—it's a real economic loss due to rate appreciation. The hedge trade will reduce but not eliminate this exposure, which is permanent unless rates revert (low probability).

**Recommended stance:** Proceed with hedge to cap downside risk while executing an orderly exit strategy over the next 6-12 months.

---

**Report Date:** March 20, 2026  
**Valid Through:** April 20, 2026 (expires; requires revaluation)  
**Next Review:** April 17, 2026 (pre-expiration of Swaps #3 & #4)
