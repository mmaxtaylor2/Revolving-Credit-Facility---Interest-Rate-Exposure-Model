# model/engine.py
# Revolver modeling engine: draws, repayments, rate shocks, DSCR, hedging, covenants.

import pandas as pd

class RevolverModel:
    def __init__(self, base_rate, spread, commitment_fee, revolver_limit, min_cash_target):
        self.base_rate = base_rate
        self.spread = spread
        self.commitment_fee = commitment_fee
        self.revolver_limit = revolver_limit
        self.min_cash_target = min_cash_target

    # -------------------------------
    # Liquidity logic
    # -------------------------------
    def manage_liquidity(self, liquidity_forecast):
        balance = 0
        draws, repays, balances = [], [], []
        for cash in liquidity_forecast:
            if cash < self.min_cash_target:
                draw = min(self.min_cash_target - cash, self.revolver_limit - balance)
                balance += draw
                repay = 0
            elif cash > self.min_cash_target and balance > 0:
                repay = min(cash - self.min_cash_target, balance)
                balance -= repay
                draw = 0
            else:
                draw = 0
                repay = 0
            draws.append(draw)
            repays.append(repay)
            balances.append(balance)
        return pd.DataFrame({
            "Cash_Forecast": liquidity_forecast,
            "Draws": draws,
            "Repayments": repays,
            "Revolver_Balance": balances
        })

    # -------------------------------
    # Rate scenarios
    # -------------------------------
    def run_scenarios(self, liquidity_forecast):
        shocks = {
            "Base": self.base_rate,
            "+25bps": self.base_rate + 0.0025,
            "+50bps": self.base_rate + 0.0050,
            "+100bps": self.base_rate + 0.0100
        }
        base = self.manage_liquidity(liquidity_forecast)
        results = {}
        for label, rate in shocks.items():
            full = rate + self.spread
            df = base.copy()
            df[f"Interest_{label}"] = df["Revolver_Balance"] * full
            df[f"Unused_Fees_{label}"] = (
                (self.revolver_limit - df["Revolver_Balance"]).clip(lower=0) * self.commitment_fee
            )
            df[f"Total_Cost_{label}"] = df[f"Interest_{label}"] + df[f"Unused_Fees_{label}"]
            results[label] = df
        return results

    # -------------------------------
    # DSCR coverage
    # -------------------------------
    def calculate_dscr(self, df, ebitda_forecast):
        df["EBITDA"] = ebitda_forecast
        for col in [c for c in df.columns if "Total_Cost_" in c]:
            name = col.replace("Total_Cost_", "")
            df[f"DSCR_{name}"] = df["EBITDA"] / df[col]
        return df

    # -------------------------------
    # Hedging
    # -------------------------------
    def apply_hedge(self, df, hedge_percent, fixed_rate):
        hedged = df["Revolver_Balance"] * hedge_percent
        df["Hedged_Balance"] = hedged
        df["Floating_Balance"] = df["Revolver_Balance"] - hedged
        df["Swap_Fixed_Cost"] = hedged * fixed_rate
        return df

    # -------------------------------
    # Covenant checks
    # -------------------------------
    def run_covenants(self, df, dscr_floor=1.10, util_limit=0.85):
        df["Utilization"] = df["Revolver_Balance"] / self.revolver_limit
        dscr_cols = [c for c in df.columns if "DSCR_" in c]
        df["DSCR_Fail"] = df[dscr_cols].lt(dscr_floor).any(axis=1)
        df["Util_Fail"] = df["Utilization"] > util_limit
        df["Covenant_Fail"] = df["DSCR_Fail"] | df["Util_Fail"]
        return df

