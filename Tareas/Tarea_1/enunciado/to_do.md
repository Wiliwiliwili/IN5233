# Python Project Roadmap: Swap Portfolio Valuation & Risk Engine

## 1. Project Setup
- Create a virtual environment (`venv` or `conda`).
- Install required mathematical and data libraries: `uv install pandas numpy scipy python-dateutil`.
- Establish the folder structure:
  - `data/` (Store the extracted JSON data here)
  - `src/`
    - `curve_builder.py` (Dual bootstrapping mathematics)
    - `pricer.py` (Swap leg and portfolio valuation)
    - `risk.py` (RAN 21-13 regulatory scenarios)
  - `main.py` (Execution orchestrator)

## 2. Data Ingestion & Formatting
- Load all JSON objects into Pandas DataFrames.
- Standardize all dates using `datetime` (Valuation date: March 20, 2026).
- Convert all quoted percentage rates and basis points to decimals for calculations (e.g., 4.650% -> 0.04650, -83.8 bps -> -0.00838).
- Map tenors (1M, 2Y, etc.) to continuous day counts adhering strictly to the stated ACT/360 convention.

## 3. Dual Bootstrapping Construction (`curve_builder.py`)
- **Step 3.1 USD Discount Curve:** Generate SOFR discount factors using the provided zero rates and log-linear interpolation.
- **Step 3.2 FX Forward Curve:** Compute outright forward rates utilizing the Spot mid-rate and NDF Forward Points (adjusted for tenor).
- **Step 3.3 CLP Zero Curve:** Bootstrap the local CLP zero coupon curve. Because collateral is in USD, use the Cross-Currency Basis spreads (SOFR/Camara 6m) against the Par Swap rates to solve for the implied CLP forward and discount factors. Use a root-finding algorithm (e.g., `scipy.optimize.newton`) to iteratively solve for zero rates that price the par swaps at zero NPV.

## 4. Valuation Engine (`pricer.py`)
- Separate each swap into Active (Receiving) and Passive (Paying) legs.
- Identify the rate type (Fixed vs. ICP/Camara).
- Calculate floating cash flows by estimating forward rates from the bootstrapped CLP zero curve.
- Discount all cash flows (fixed and floating) to March 20, 2026, using the CLP zero curve.
- Calculate the Net Present Value (NPV) per swap and sum them to determine the total portfolio base value.

## 5. Regulatory Stress Testing (`risk.py`)
- Extract the 6 required scenarios from Section 5.2 of the CMF RAN 21-13 regulatory framework (Parallel Up, Parallel Down, Steepening, Flattening, Short Up, Short Down).
- Programmatically perturb the baseline zero curve according to each scenario's basis point shock schedule.
- Execute the valuation engine over all 6 shocked curves.
- Output a comparative summary matrix (Scenario vs. Portfolio NPV vs. ∆ NPV).

## 6. Hedging Strategy Recommendation
- Compute the portfolio's DV01 (Dollar Value of a 1 basis point shift) by applying a 1 bp parallel shift to the baseline curve.
- Identify the regulatory scenario causing the most severe financial loss (the "worst scenario").
- Calculate the necessary DV01 offset required to reduce the loss in this worst-case scenario by exactly 50%.
- Model standard market par swaps (e.g., 5Y or 10Y IRS) to determine the exact nominal amount and position (Pay Fixed / Receive Fixed) needed to fulfill the offset requirement.