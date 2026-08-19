from mcp.server import MCPServer
from pathlib import Path
import pandas as pd
from tools.get_top_items_tool import get_top_items as top_items_tool

mcp = MCPServer("agentic-business-insights")

_REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = _REPO_ROOT / "data"

def load_weekly(account_id: str) -> pd.DataFrame:
    path = DATA_DIR / account_id / "sales_weekly.parquet"
    if not path.exists():
        raise FileNotFoundError(f"cannot find weekly parquet for {account_id}")
    df = pd.read_parquet(path)
    return df

@mcp.tool()
def get_top_items(account_id: str, start_date: str, end_date: str):
    df = load_weekly(account_id="TestBusinessAcc") # remove hardcoding
    return top_items_tool(df, start_date, end_date)

if __name__ == "__main__":
    mcp.run()