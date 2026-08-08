import pandas as pd
from pathlib import Path
from ingestion.sales_data_model import SalesRecord


def save_sales_records(rec: list[SalesRecord], accountId: str) -> Path:
    """
    save sales records called from square client 
    flow is pull from Square API -> build a table of SalesRecords with pd -> save as parquet -> everything downstream (EDA, features, models, MCP tools) reads that parquet file instead of calling directly from the API.
    """
