from math import exp, log, sqrt
import streamlit as st
from scipy import stats

def BlackScholes(S, K, T, r, sigma, option_type='call'):
    """Calculate Black-Scholes option price."""

    if S <= 0 or K<= 0 or sigma <= 0 or T <= 0:
        raise ValueError("Must use positive numbers.")
    if option_type not in ['call', 'put']:
        raise ValueError("option_type must be 'call' or 'put'.")
    
    d1 = (log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    
    if option_type == 'call':
        price = S * stats.norm.cdf(d1) - K * exp(-r * T) * stats.norm.cdf(d2)
    else:
        price = K * exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)
    
    return price

def calculate_option_price():
    st.title("Black-Scholes Option Pricing Calculator")

    S = st.number_input("Current Stock Price (S)", min_value=0.01, value=100.0)
    K = st.number_input("Strike Price (K)", min_value=0.01, value=100.0)
    T = st.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0)
    r = st.number_input("Risk-Free Interest Rate (r as decimal)", min_value=0.0, value=0.05)
    sigma = st.number_input("Volatility (sigma as decimal)", min_value=0.01, value=0.2)
    option_type = st.selectbox("Option Type", options=['call', 'put'])

    if st.button("Calculate Option Price"):
        try:
            price = BlackScholes(S, K, T, r, sigma, option_type)
            st.success(f"The {option_type} option price is: {price:.2f}")
        except ValueError as e:

            st.error(f"Error: {e}")

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    """Calculate option Greeks."""
    d1 = (log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)

    # Delta 
    if option_type == 'call':
        delta = stats.norm.cdf(d1)
    else:
        delta = stats.norm.cdf(d1) - 1

    # Gamma (same for call and put)
    gamma = stats.norm.pdf(d1) / (S * sigma * sqrt(T))

    # Vega (same for call and put)
    vega = S * stats.norm.pdf(d1) * sqrt(T) / 100  # Divided by 100 for 1% change (display)

    # Theta
    if option_type == 'call':
        theta = (-S * stats.norm.pdf(d1) * sigma / (2 * sqrt(T)) - r * K * exp(-r * T) * stats.norm.cdf(d2))   / 365
    
    else:
        theta = (-S * stats.norm.pdf(d1) * sigma / (2 * sqrt(T)) + r * K * exp(-r * T) * stats.norm.cdf(-d2)) / 365
    
    # Rho
    if option_type == 'call':
        rho = K * T * exp(-r * T) * stats.norm.cdf(d2) / 100  # Divided by 100 for 1% change (display)
    else:
        rho = -K * T * exp(-r * T) * stats.norm.cdf(-d2) / 100  # Divided by 100 for 1% change (display)

    return {
        'delta': delta,
        'gamma': gamma,
        'theta': theta,
        'vega': vega,
        'rho': rho
    }
