from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from ingestion.sales_data_model import SalesRecord
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

client = Square(
    environment=SquareEnvironment.PRODUCTION,
    token=os.environ['SQUARE_PROD_ACCESS_TOKEN']
)
