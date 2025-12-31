# Black-Scholes Option Pricing Model

A **Streamlit web app** for calculating and visualizing option prices, Greeks, payoff diagrams, and sensitivity/P&L heatmaps using the Black-Scholes model.

---

## Features

1. **Option Pricer**
   - Compute call and put option prices using the Black-Scholes formula.
   - Display key option Greeks: Delta, Gamma, Vega, Theta, and Rho.
   - Interactive explanations and examples for each Greek.

2. **Payoff Diagram**
   - Visualize the profit/loss of call and put options at expiration.
   - Highlight strike price and current spot price.

3. **Sensitivity Analysis**
   - Generate heatmaps of option values across a range of underlying prices and volatilities.
   - Compare call and put values for better risk assessment.
   - **Color Significance:**
     - **Darker colors** → lower option values
     - **Brighter colors** → higher option values

4. **P&L Heatmaps**
   - Track potential profit and loss based on user-specified purchase prices.
   - Visualize the impact of spot price and implied volatility changes on option P&L.
   - **Color Significance:**
     - **Red shades** → losses
     - **Green shades** → gains
     - **Yellow shades (middle)** → near break-even
