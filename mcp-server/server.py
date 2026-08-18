from mcp.server import MCPServer
from pathlib import Path
import pandas as pd

mcp = MCPServer("agentic-business-insights")

_REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = _REPO_ROOT / "data"
