import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from black_scholes import OptionInputs, price_and_greeks


st.set_page_config(
    page_title="Equity Derivatives Trading Analytics MVP",
    layout="wide",
)

st.title("Equity Derivatives Trading Analytics MVP")
st.caption("Black-Scholes pricing, Greeks, and simple scenario analysis for desk-style option risk analytics.")

with st.sidebar:
    st.header("Option Inputs")

    option_type = st.selectbox("Option type", ["call", "put"])
    spot = st.number_input("Spot price", min_value=1.0, value=100.0, step=1.0)
    strike = st.number_input("Strike price", min_value=1.0, value=100.0, step=1.0)
    time_to_expiry = st.number_input(
        "Time to expiry, years",
        min_value=0.01,
        value=0.50,
        step=0.05,
    )
    risk_free_rate = st.number_input(
        "Risk-free rate",
        min_value=-0.05,
        max_value=0.30,
        value=0.05,
        step=0.005,
        format="%.3f",
    )
    volatility = st.number_input(
        "Volatility",
        min_value=0.01,
        max_value=2.00,
        value=0.25,
        step=0.01,
        format="%.2f",
    )

inputs = OptionInputs(
    spot=spot,
    strike=strike,
    time_to_expiry=time_to_expiry,
    risk_free_rate=risk_free_rate,
    volatility=volatility,
    option_type=option_type,
)

result = price_and_greeks(inputs)

st.subheader("Pricing and Greeks")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Price", f"{result['price']:.4f}")
col2.metric("Delta", f"{result['delta']:.4f}")
col3.metric("Gamma", f"{result['gamma']:.6f}")
col4.metric("Vega", f"{result['vega']:.4f}")
col5.metric("Theta / day", f"{result['theta']:.4f}")

st.subheader("Scenario Analysis")

spot_shocks = np.linspace(-0.10, 0.10, 9)
vol_shocks = np.linspace(-0.05, 0.05, 5)

rows = []
for spot_shock in spot_shocks:
    for vol_shock in vol_shocks:
        scenario_spot = spot * (1 + spot_shock)
        scenario_vol = max(0.01, volatility + vol_shock)

        scenario_inputs = OptionInputs(
            spot=scenario_spot,
            strike=strike,
            time_to_expiry=time_to_expiry,
            risk_free_rate=risk_free_rate,
            volatility=scenario_vol,
            option_type=option_type,
        )

        scenario_result = price_and_greeks(scenario_inputs)

        rows.append(
            {
                "spot_shock": spot_shock,
                "vol_shock": vol_shock,
                "scenario_spot": scenario_spot,
                "scenario_vol": scenario_vol,
                "price": scenario_result["price"],
                "delta": scenario_result["delta"],
                "gamma": scenario_result["gamma"],
                "vega": scenario_result["vega"],
                "theta": scenario_result["theta"],
            }
        )

scenario_df = pd.DataFrame(rows)

left, right = st.columns([1.2, 1])

with left:
    st.dataframe(
        scenario_df.round(
            {
                "spot_shock": 4,
                "vol_shock": 4,
                "scenario_spot": 2,
                "scenario_vol": 4,
                "price": 4,
                "delta": 4,
                "gamma": 6,
                "vega": 4,
                "theta": 4,
            }
        ),
        width="stretch",
    )

with right:
    base_vol_df = scenario_df[scenario_df["vol_shock"].abs() < 1e-9].copy()

    fig, ax = plt.subplots()
    ax.plot(base_vol_df["scenario_spot"], base_vol_df["price"], marker="o")
    ax.set_xlabel("Scenario spot")
    ax.set_ylabel("Option price")
    ax.set_title("Option Price vs Spot Shock")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

st.subheader("Desk Use Case")
st.write(
    "This MVP shows how a trader or quant could quickly inspect price sensitivity, Greeks, "
    "and scenario-driven option risk across spot and volatility shocks. It is intentionally "
    "small, but structured as a starting point for front-office analytics, pricing tools, "
    "and risk dashboards."
)
