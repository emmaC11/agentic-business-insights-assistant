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
    print(sales_raw_data.shape)
    print(sales_raw_data.head())