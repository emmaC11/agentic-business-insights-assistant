import pandas as pd

# return specific item sales data within time period
def get_item_sales(df: pd.DataFrame, item: str, start_date: str, end_date:str) -> str:

        # block re-used from get top items tool, create as standalone func to resue?
        # parse str to datetime
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
    
        # week start on monday
        # move start date passed to nearest monday
        # used claude entirely for this block below (line 11 -25 )
        days_forward = (7 - start.weekday()) % 7
        start_snapped = start + pd.Timedelta(days=days_forward)
        end_snapped = end - pd.Timedelta(days=end.weekday())
    
        mask = (df["week_start"] >= start_snapped) & (df["week_start"] <= end_snapped)
        window = df.loc[mask]
    
        if window.empty:
            data_min = df["week_start"].min().date()
            data_max = df["week_start"].max().date()
            return (
                f"No sales found between {start_snapped.date()} and {end_snapped.date()}. "
                f"Available data covers {data_min} to {data_max}."
            )
    