from square import Square
from square.environment import SquareEnvironment
from square.core.api_error import ApiError
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os

load_dotenv()

client = Square(
    environment=SquareEnvironment.PRODUCTION,
    token=os.environ['SQUARE_PROD_ACCESS_TOKEN']
)
