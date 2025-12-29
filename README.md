## Revolving Credit Facility & Interest Rate Exposure Model

A Streamlit-based credit modeling tool that simulates revolver mechanics, interest costs, hedging impact, and covenant sensitivity under changing interest rate environments. The model reflects how corporate treasury, FP&A, and leveraged credit teams evaluate liquidity, borrowing costs, and rate exposure during capital planning.

## Live App
https://revolving-credit-facility---interest-rate-exposure-model-vjwou.streamlit.app

## Project Purpose

This project models the full mechanics of a corporate revolving credit facility, including:

Automated draw and repayment behavior to maintain minimum liquidity
SOFR/Prime-based floating rate interest expense projection
Commitment fee charges on unused borrowing capacity
Hedging through fixed-rate swap on a percentage of revolver balance
DSCR coverage and covenant testing under rate shock scenarios
Sensitivity cases: Base, +25bps, +50bps, +100bps

The purpose is to replicate real-world workflows used in:

Corporate Treasury and Liquidity Management
FP&A and Budgeting for Capital Structure Planning
Banking and Credit Underwriting
Leveraged Finance and Debt Modeling

## Core Features

Category	Capability
Revolver Mechanics	Draw/repay logic based on cash thresholds
Interest Expense	Floating rate model with spread + base index
Unused Fees	Commitment fee applied to undrawn capacity
Hedging	Split between floating exposure and fixed swap rate cost
DSCR	Coverage analysis across interest rate scenarios
Covenants	DSCR floor and utilization breach detection
Outputs	Excel files exported per scenario for review

## How the Model Works

User inputs revolver terms (rate, spread, fees, limits, cash target)
A liquidity forecast drives automated draw and repayment behavior
The model calculates interest cost, fees, and balance outcomes
Hedge settings apply a fixed-rate swap to a share of the balance
DSCR and covenant tests evaluate downside protection
Outputs can be exported for reporting or further analysis

## Project Structure

Revolving-Credit-Facility-&-Interest-Rate-Exposure-Model/
│
├── model/
│   └── engine.py                # Financial logic and scenario functions
│
├── ui/
│   └── streamlit_app.py         # Streamlit interface for running model
│
├── data/                        # Input or example forecasts (optional)
├── outputs/                     # Excel exports from scenario runs
├── requirements.txt             # Dependencies
└── README.md

## Requirements / Installation

Install dependencies:
pip install -r requirements.txt

Run the Streamlit interface:
streamlit run ui/streamlit_app.py

A browser window will open with the model interface.

## Skills Demonstrated

Revolving credit facility mechanics
Liquidity planning and minimum cash thresholds
Floating interest rate modeling (SOFR/Prime + spread)
Hedging and swap overlay to manage rate exposure
DSCR and covenant protection analysis
Scenario testing and Excel reporting
Python, Pandas, Plotly, and Streamlit application development
