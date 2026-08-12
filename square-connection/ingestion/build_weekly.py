import pandas as pd
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def build_weekly_parquet(account_id: str):
    """
    create new sales_weekly.parquet from sales_raw.parquet
    use this parquet for the data queries & models
    output schema: (one row per item x valid week):
    account_id, item, category, week_start, quantity, price_cents, weeks_sold, tier
    """

    # load raw parquet
    sales_raw_path = _REPO_ROOT / "data" / account_id / "sales_raw.parquet"
    sales_raw_data = pd.read_parquet(sales_raw_path)
    # print(sales_raw_data.shape)
    # print(sales_raw_data.head())

    # add week col to each row (raw data only has date, we need to map to specific week, M->S)
    # can remove time conversion if ingestion is set to correct timezone
    sales_raw_data["week"] = pd.to_datetime(sales_raw_data["date"], utc=True).dt.tz_convert("Europe/Dublin").dt.to_period("W-SUN")
    # print(sales_raw_data.head())

    # identify valid weeks - identify ingestion gaps, or if data pulled midweek
    all_weeks = pd.period_range(
        sales_raw_data["week"].min(),
        sales_raw_data["week"].max()
    )

    # find gaps / weeks with no sales for that week
    weeks_with_sales = set(sales_raw_data["week"])
    gap_weeks = set(all_weeks) - weeks_with_sales

    min_date = sales_raw_data["date"].min()
    max_date = sales_raw_data["date"].max()

    # check if ingestion start and end dates are midweek / partial
    partial_weeks = set()
    # .weekday 0-6 rep weekday
    if min_date.weekday() != 0: # 0 -> monday
        partial_weeks.add(all_weeks[0])
    if max_date.weekday() != 6: # 6 -> sunday
        partial_weeks.add(all_weeks[-1])

    # combine sets
    excluded = gap_weeks | partial_weeks
    valid_weeks = pd.PeriodIndex(sorted(set(all_weeks) - excluded), freq="W-SUN")

    print(f"cal weeks count ->{len(all_weeks)}")
    print(f"gap weeks count -> {len(gap_weeks)} - {sorted(gap_weeks)}")
    print(f"partial weeks count -> {len(partial_weeks)} -  {sorted(partial_weeks)}")
    print(f"valid weeks count -> {len(valid_weeks)}")

    # agg one row per item per week
    # currently same item can appear 5 times as seperate rows in the same week
    # data shape we need is this data aggregated into one weekly row per item

    # validate week is part of valid_weeks
    valid_df = sales_raw_data[sales_raw_data["week"].isin(valid_weeks)]

    weekly_agg = (
        valid_df
        .groupby(["item", "week"])
        .agg(
            quantity=("quantity","sum"), # sum input of quant
            price_cents=("price_cents", "last") # take last value of price cents in each grouping (is same for all so any pick is fine)
        )
        .reset_index()
    )

    print(type(weekly_agg))
    print(weekly_agg.shape)
    print(weekly_agg.head())