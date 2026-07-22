from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from ingestion.sales_data_model import SalesRecord
import os
import logging

logger = logging.getLogger(__name__)

class SquareIngestionClient:
    def __init__(self, account_id, token, env):
        self.account_id = account_id
        self._client = Square(environment=env, token=token)
