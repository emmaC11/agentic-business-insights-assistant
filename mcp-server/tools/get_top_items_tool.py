import pandas as pd

def get_top_items(df: pd.DataFrame, start_date: str, end_date: str) -> str:
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

    # calc revenue col 
    # use assign as return new df does not alter the df passed as that will be used in other tool calls
    window = window.assign(revenue_cents=window["quantity"] * window["price_cents"])

    # create new agg df with required cols
    agg = (
        window.groupby("item", as_index=False)
        .agg(
            quantity=("quantity", "sum"),
            category=("category", "first"),
            weeks_active=("quantity", lambda x: (x > 0).sum()),
            revenue_cents=("revenue_cents", "sum")
        )
        .sort_values("quantity", ascending=False)
        .head()
        .reset_index(drop=True)
    )
