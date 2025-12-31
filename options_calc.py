import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from blackscholes import BlackScholes, calculate_greeks

st.set_page_config("Black-Scholes Option Pricing Model", layout="wide")
st.title("Black-Scholes Option Pricing Model")

# Navigation
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Select Feature",
    [
        "Option Pricer", 
        "Payoff Diagram", 
        "Sensitivity Analysis", 
        "P&L Heatmaps"
    ]
)



# Core Inputs
def sidebar_core():
    S = st.sidebar.number_input("Current Stock Price (S)", 1.0, 1e6, 100.0)
    K = st.sidebar.number_input("Strike Price (K)", 1.0, 1e6, 100.0)
    T = st.sidebar.number_input("Time to Expiry (Years)", 0.01, 10.0, 1.0)
    r = st.sidebar.slider("Risk-Free Interest Rate (%)", 0.0, 20.0, 5.0) / 100
    sigma = st.sidebar.slider("Volatility (%)", 1.0, 150.0, 20.0) / 100
    return S, K, T, r, sigma 



# Page 1: Option Pricer
if page == "Option Pricer":
    st.sidebar.subheader("Option Settings")
    S, K, T, r, sigma = sidebar_core()
    option_type = st.sidebar.selectbox("Option Type", ['call', 'put'])

    call_price = BlackScholes(S, K, T, r, sigma, 'call')
    put_price = BlackScholes(S, K, T, r, sigma, 'put')
    price = call_price if option_type == 'call' else put_price

    greeks = calculate_greeks(S, K, T, r, sigma, option_type)

    c1, c2, c3 = st.columns(3)
    c1.metric("Call Price", f"${call_price:.2f}")
    c2.metric("Put Price", f"${put_price:.2f}")
    c3.metric("Selected Option", f"{price:.2f}")

    st.divider()
    st.subheader("Greeks")

    cols = st.columns(5)
    cols[0].metric("Delta", f"{greeks['delta']:.4f}")
    cols[1].metric("Gamma", f"{greeks['gamma']:.4f}")
    cols[2].metric("Vega (per 1%)", f"{greeks['vega']:.4f}")
    cols[3].metric("Theta (per day)", f"{greeks['theta']:.4f}")
    cols[4].metric("Rho (per 1%)", f"{greeks['rho']:.4f}")

    # Greeks explanation
    with st.expander("Understanding the Greeks - Click to Learn More"):
        greek_tab1, greek_tab2, greek_tab3, greek_tab4, greek_tab5 = st.tabs(
            ["Delta", "Gamma", "Vega", "Theta", "Rho"]
        )
        with greek_tab1:
            st.markdown("### Delta")
            st.write(f'**Current Value:** {greeks["delta"]:.4f}')
            st.write("""
    **Definition:** 

    Delta measures the rate of change of the option price with respect to changes in the underlying asset's price. It indicates how much the option price is expected to change for a $1 change in the underlying asset's price.

    **What it means:**

    - For calls: delta ranges from 0 to 1.
    - For puts: delta ranges from -1 to 0.
    - Delta is higher for in-the-money/profitable options and lower for out-of-the-money/unprofitable options
    - A delta of 0.5 means the option price will move approximately \\$0.50 for every \\$1 move in the underlying asset.
    """)

            st.write("**Example:**")
            if option_type == 'call':
                st.info(f"""
    Your call option has a delta of {greeks['delta']:.4f}.

    If the stock price increases by \\$1, the option price is expected to increase by approximately \\${greeks['delta']:.2f}, from \\${price:.2f} to \\${price + greeks['delta']:.2f}.
    """)
            else:
                st.info(f"""
    Your put option has a delta of {greeks['delta']:.4f}.

    If the stock price increases by \\$1, the option price is expected to decrease by approximately \\${abs(greeks['delta']):.2f}, from \\${price:.2f} to \\${price + greeks['delta']:.2f}.
    """)

        with greek_tab2:
            st.markdown("### Gamma")
            st.write(f"**Current Value:** {greeks['gamma']:.4f}")
            st.write("""
    **Definition:** 
    Gamma measures the rate of change of *delta* with respect to changes in the underlying asset's price. It indicates how much the option's *delta* is expected to change for a $1 change in the underlying asset's price.
            
    **What it means:**
                    
    - Gamma is the same for calls and puts with the same strike and expiration
    - Gamma increases as the option approaches expiration
    - A gamma of 0.1 means that for every $1 increase in the underlying asset's price, the option's *delta* will increase by 0.1.
    - Gamma is typically higher for at-the-money/profitable options and lower for out-of-the-money/unprofitable options
    """)
            st.write("**Example:**")
            st.info(f"""
    Your option has a gamma of {greeks['gamma']:.4f}.

    If the stock price increases by \\$1, the option's *delta* is expected to increase by approximately \\${greeks['gamma']:.2f}, from \\${greeks['delta']:.2f} to \\${greeks['delta'] + greeks['gamma']:.2f}.
    This means the option's sensitivity to price changes is {'increasing' if greeks['gamma'] > 0 else 'decreasing'}.
    """)


        with greek_tab3:
            st.markdown("### Vega")
            st.write(f"**Current Value:** {greeks['vega']:.4f}")
            st.write("""
    **Definition:** 
    Vega measures the rate of change of the option price with respect to changes in the underlying asset's implied volatility (IV). It indicates how much the option price is expected to change for a 1% change in the underlying asset's implied volatility.
            
    **What it means:**

    - Vega is the same for calls and puts with the same strike and expiration
    - Vega increases as the option approaches expiration
    - A vega of 0.1 means that for every 1% increase in the underlying asset's IV, the option price will increase by 0.1.
    - Vega is typically higher for at-the-money/have a longer-term maturity options and lower for out-of-the-money/short-term options
    """)
            st.write("**Example:**")
            st.info(f"""
    Your option has a vega of {greeks['vega']:.4f}.

    If the underlying asset's IV increases by 1%, the option price is expected to increase by approximately \\${greeks['vega']:.2f}, from \\${price:.2f} to \\${price + greeks['vega']:.2f}.
    """)
            st.divider()
            st.caption(f"""
    *Note:*
                    
    *Implied volatility is an estimate, based on market belief, of the future volatility of the underlying asset, not historical volatility. The Black-Scholes formula used in this model can also be used to calculate IV by starting from the actual market option price and solving for the IV that would produce that price.*
    """)

        with greek_tab4:
            st.markdown("### Theta")
            st.write(f"**Current Value:** {greeks['theta']:.4f}")
            st.write("""
    **Definition:** 
    Theta measures the rate of change of the option price with respect to changes in time (time decay). It indicates how much the option price is expected to decrease for a one-day passage of time.
            
    **What it means:**

    - Theta is typically negative for long options (they lose value over time)
    - Theta increases as the option approaches expiration
    - A theta of -0.1 means that for every day that passes, the option price will decrease by 0.1.
    - Theta is typically higher for at-the-money options and lower for out-of-the-money options
    """)
            st.write("**Example:**")
            st.info(f"""
    Your option has a theta of {greeks['theta']:.4f}.

    If one day passes, the option price is expected to decrease by approximately \\${abs(greeks['theta']):.2f}, from \\${price:.2f} to \\${price - abs(greeks['theta']):.2f}.
    This means the option's value is decreasing due to time decay.
    """)
        with greek_tab5:
            st.markdown("### Rho")
            st.write(f"**Current Value:** {greeks['rho']:.4f}")
            st.write("""
    **Definition:**
    Rho measures the rate of change of the option price with respect to changes in the risk-free interest rate. It indicates how much the option price is expected to change for a 1% change in the risk-free interest rate.
            
    **What it means:**

    - Rho is typically positive for calls and negative for puts
    - A rho of 0.1 means that for every 1% increase in the risk-free interest rate, the option price will increase by 0.1.
    - Rho is typically higher for at-the-money/have a longer-term maturity options and lower for out-of-the-money/short-term options
    """)
            st.write("**Example:**")
            st.info(f"""
    Your option has a rho of {greeks['rho']:.4f}.

    If the risk-free interest rate increases by 1%, the option price is expected to increase by approximately \\${abs(greeks['rho']):.2f}, from \\${price:.2f} to \\${price + abs(greeks['rho']):.2f}.
    """)
            st.divider()
            st.caption(f"""
    *Note:
    Because risk-free rates tend to change slowly over time, rho usually has a smaller impact on option prices compared to the other Greeks.*
    """)
    with st.expander("About Black-Scholes"):
        st.markdown("""
- The option can only be exercised at expiration (European options)
- No dividends are paid
- Constant volatility & risk-free interest rates
- Log-normal price dynamics
- Markets are efficient - no arbitrage
        """)
        st.caption(f"""
    *Note:
    This model provides **theoretical fair value**, not a trading recommendation.*
    """)


        
# Page 2: Payoff Diagram        
elif page == "Payoff Diagram":
    st.sidebar.header("Payoff Settings")
    S, K, T, r, sigma = sidebar_core()
    option_type = st.sidebar.selectbox("Option Type", ["call", "put"])

    premium = BlackScholes(S, K, T, r, sigma, option_type)

    S_range = np.linspace(0.5 * S, 1.5 * S, 300)
    payoff = (
        np.maximum(S_range - K, 0) if option_type == "call"
        else np.maximum(K - S_range, 0)
    )

    pnl = payoff - premium

    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(S_range, pnl, lw=2)
    ax.axhline(0, color="black")
    ax.axvline(K, ls="--", color="red", label="Strike")
    ax.axvline(S, ls="--", color="blue", label="Spot")

    ax.set_xlabel("Stock Price at Expiration")
    ax.set_ylabel("Profit / Loss")
    ax.legend()
    ax.grid(alpha=0.3)

    st.pyplot(fig)

# Page 3: Value Heatmaps

elif page == "Sensitivity Analysis":
    st.sidebar.subheader("Heatmap Settings")
    S, K, T, r, sigma = sidebar_core()

    s_min = st.sidebar.number_input("Min Spot", value=0.7 * S)
    s_max = st.sidebar.number_input("Max Spot", value=1.3 * S)
    v_min = st.sidebar.slider("Min Vol (%)", 1, 100, 10) / 100
    v_max = st.sidebar.slider("Max Vol (%)", 1, 150, 40) / 100

    S_grid = np.linspace(s_min, s_max, 25)
    V_grid = np.linspace(v_min, v_max, 25)

    call_vals = np.array([
        [BlackScholes(s, K, T, r, v, "call") for s in S_grid]
        for v in V_grid
    ])

    put_vals = np.array([
        [BlackScholes(s, K, T, r, v, "put") for s in S_grid]
        for v in V_grid
    ])

    fig, axs = plt.subplots(1, 2, figsize=(16,6))

    im1 = axs[0].imshow(
        call_vals, origin="lower", aspect="auto",
        extent=[s_min, s_max, v_min * 100, v_max * 100]
    )
    fig.colorbar(im1, ax=axs[0])
    axs[0].set_title("Call Option Value")

    im2 = axs[1].imshow(
        put_vals, origin="lower", aspect="auto",
        extent=[s_min, s_max, v_min * 100, v_max * 100]
    )
    fig.colorbar(im2, ax=axs[1])
    axs[1].set_title("Put Option Value")

    st.pyplot(fig)



# Page 4: P&L Heatmaps
elif page == "P&L Heatmaps":
    st.sidebar.subheader("Purchase Prices")
    S, K, T, r, sigma = sidebar_core()

    call_buy = st.sidebar.number_input(
        "Call Purchase Price",
        value=BlackScholes(S, K, T, r, sigma, "call")
    )
    put_buy = st.sidebar.number_input(
        "Put Purchase Price",
        value=BlackScholes(S, K, T, r, sigma, "put")
    )

    s_min = st.sidebar.number_input("Min Spot", value=0.7 * S)
    s_max = st.sidebar.number_input("Max Spot", value=1.3 * S)
    v_min = st.sidebar.slider("Min Vol (%)", 1, 100, 10) / 100
    v_max = st.sidebar.slider("Max Vol (%)", 1, 150, 40) / 100

    S_grid = np.linspace(s_min, s_max, 25)
    V_grid = np.linspace(v_min, v_max, 25)

    call_pnl = np.array([
        [BlackScholes(s, K, T, r, v, "call") - call_buy for s in S_grid]
        for v in V_grid
    ])

    put_pnl = np.array([
        [BlackScholes(s, K, T, r, v, "put") - put_buy for s in S_grid]
        for v in V_grid
    ])
    
    fig, axs = plt.subplots(1, 2, figsize=(16,6))

    im1 = axs[0].imshow(
        call_pnl, origin="lower", aspect="auto", cmap="RdYlGn",
        extent=[s_min, s_max, v_min * 100, v_max * 100]
    )
    fig.colorbar(im1, ax=axs[0])
    axs[0].set_title("Call Option P&L")

    im2 = axs[1].imshow(
        put_pnl, origin="lower", aspect="auto", cmap="RdYlGn",
        extent=[s_min, s_max, v_min * 100, v_max * 100]
    )
    fig.colorbar(im2, ax=axs[1])
    axs[1].set_title("Put Option P&L")
    
    st.pyplot(fig)