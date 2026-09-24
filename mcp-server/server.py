from mcp.server import MCPServer
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))

import pandas as pd
from tools.get_top_items_tool import get_top_items as top_items_tool
from tools.get_item_sales import get_item_sales as item_sales_tool
from tools.forecast_demand import forecast_demand as forecast_item_demand_tool

mcp = MCPServer("agentic-business-insights")
DATA_DIR = _REPO_ROOT / "data"

def load_weekly(account_id: str) -> pd.DataFrame:
    path = DATA_DIR / account_id / "sales_weekly.parquet"
    if not path.exists():
        raise FileNotFoundError(f"cannot find weekly parquet for {account_id}")
    df = pd.read_parquet(path)
    return df

def load_lookup(account_id: str) -> pd.DataFrame:
    path = DATA_DIR / account_id / "models" / "model_selection_per_item.parquet"
    if not path.exists():
        raise FileNotFoundError(f"cannot find model selection parquet for {account_id}")
    df = pd.read_parquet(path)
    return df

@mcp.tool()
def get_top_items(account_id: str, start_date: str, end_date: str):
    df = load_weekly(account_id=account_id)
    return top_items_tool(df, start_date, end_date)

@mcp.tool()
def get_item_sales(account_id: str, item: str):
    df = load_weekly(account_id=account_id)
    return item_sales_tool(df, item)

@mcp.tool()
def get_item_forecast(account_id: str, item:str, h: int):
    df = load_weekly(account_id=account_id)
    lookup_df =load_lookup(account_id=account_id)
    return forecast_item_demand_tool(df, lookup_df, item, h)

if __name__ == "__main__":
    mcp.run()