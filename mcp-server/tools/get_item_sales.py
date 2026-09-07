import pandas as pd

# return specific item sales data within time period
def get_item_sales(df: pd.DataFrame, item: str, start_date: str, end_date:str) -> str:
    