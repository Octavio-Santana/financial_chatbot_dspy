import pandas as pd
import json


class FinancialRepository:

    def __init__(self, transactions_path: str, user_path: str):
        self.transactions_path = transactions_path
        self.user_path = user_path

        self._transactions_df = pd.read_csv(self.transactions_path)
        self._transactions_df["date"] = pd.to_datetime(self._transactions_df["date"])
    

    def get_user_income(self) -> float:
        with open(self.user_path, "r") as f:
            data = json.load(f)
        
        return data["monthly_income"]


    def get_all_transactions(self) -> pd.DataFrame:
        return self._transactions_df.copy()


    def get_transactions_by_month(self, year: int, month: int) -> pd.DataFrame:
        df = self._transactions_df

        return df[
            (df["date"].dt.year == year) &
            (df["date"].dt.month == month)
        ].copy()
