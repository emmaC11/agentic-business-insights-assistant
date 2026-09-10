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

        item_rows = window[window["item"] == item]
        total = item_rows["quantity"].sum()
        weeks_sold = (item_rows["quantity"] > 0).sum()
        weeks_in_range = window["week_start"].nunique() 

        if total == 0:
              return f"{item} sold nothing in range chosen"

        # idmax finds index label (row num) to find where max col occurs
        # rows loc uses idmax index labelto extract entire row with the max value
        best_week = item_rows.loc[item_rows["quantity"].idxmax()]

        # agent generate res from this
        return (
            f"'{item}' — {start.date()} to {end.date()}\n"
            f"- Total sold: {total} units\n"
            f"- Sold in {weeks_sold} of {weeks_in_range} weeks\n"
            f"- Best week: {best_week['week_start'].date()} ({int(best_week['quantity'])} units)"
        )