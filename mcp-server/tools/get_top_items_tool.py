import pandas as pd

def get_top_items(df: pd.DataFrame, start_date: str, end_date: str) -> str:
    # parse str to datetime
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    
    
