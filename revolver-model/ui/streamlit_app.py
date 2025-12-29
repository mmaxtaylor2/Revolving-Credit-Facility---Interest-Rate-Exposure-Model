# ui/streamlit_app.py
# Full version with DSCR, hedging, covenants, and export.

import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os

# Ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.engine import RevolverModel

st.set_page_config(page_title="Revolver Model", layout="wide")
st.title("Revolving Credit Facility & Interest Rate Exposure Model")
st.write("This version includes DSCR, hedging, covenant checks, and shock scenarios.")

# ------------------------------------------------------------
# Facility Inputs
# ------------------------------------------------------------
st.subheader("Facility Structure")

col1, col2, col3, col4 = st.columns(4)
revolver_limit = col1.number_input("Revolver Limit ($)", value=5_000_000)
base_rate = col2.number_input("Base Rate (SOFR/Prime)", value=0.05)
spread = col3.number_input("Credit Spread", value=0.02)
commitment_fee = col4.number_input("Commitment Fee %", value=0.005)
min_cash_target = st.number_input("Minimum Cash Target ($)", value=50_000)

# ------------------------------------------------------------
# Risk, Hedge, and Covenant Inputs
# ------------------------------------------------------------
st.subheader("Hedging and Covenant Settings")

colA, colB, colC = st.columns(3)
hedge_percent = colA.slider("Hedge % of Revolver", 0.0, 1.0, 0.50)
fixed_rate = colB.number_input("Fixed Swap Rate", value=0.032)
dscr_floor = colC.number_input("DSCR Covenant Floor", value=1.10)

# ------------------------------------------------------------
# Liquidity Forecast Input
# ------------------------------------------------------------
st.subheader("Liquidity Forecast")

uploaded = st.file_uploader("Upload Forecast CSV (single column)", type="csv")
if uploaded:
    liquidity_forecast = pd.read_csv(uploaded).iloc[:, 0].tolist()
else:
    liquidity_forecast = [40000, 30000, 60000, 55000, 45000, 80000, 30000]

# Placeholder EBITDA
ebitda_forecast = [150000] * len(liquidity_forecast)

# ------------------------------------------------------------
# Run Model
# ------------------------------------------------------------
if st.button("Run Revolver Analysis"):

    model = RevolverModel(base_rate, spread, commitment_fee, revolver_limit, min_cash_target)
    scenarios = model.run_scenarios(liquidity_forecast)

    st.subheader("Results")
    for name, df in scenarios.items():

        df = model.calculate_dscr(df, ebitda_forecast)
        df = model.apply_hedge(df, hedge_percent, fixed_rate)
        df = model.run_covenants(df, dscr_floor=dscr_floor)

        st.write(f"Scenario: {name}")
        st.dataframe(df)

        # Chart
        fig = px.line(df, y=f"Total_Cost_{name}", title=f"Rate Shock Cost Curve: {name}")
        st.plotly_chart(fig, use_container_width=True)

        # Export to outputs folder
        df.to_excel(f"outputs/{name}_results.xlsx", index=False)

    st.write("Files exported to the /outputs directory.")

