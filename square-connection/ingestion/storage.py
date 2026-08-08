import pandas as pd
from pathlib import Path
from ingestion.sales_data_model import SalesRecord


def save_sales_records(recs: list[SalesRecord], accountId: str) -> Path:
    """
    save sales records called from square client 
    flow is pull from Square API -> build a table of SalesRecords with pd -> save as parquet -> everything downstream (EDA, features, models, MCP tools) reads that parquet file instead of calling directly from the API.
    """

    if not recs:
        raise ValueError("SalesRecord list is empty, no data to save")

    sales_df = pd.DataFrame([vars(r) for r in recs])
    # set data types for date, quant & price
    sales_df["date"] = pd.to_datetime(sales_df["date"], utc=True)
    sales_df["quantity"] = sales_df["quantity"].astype(float)
    sales_df["price_cents"] = sales_df["price_cents"].astype(int)
    
