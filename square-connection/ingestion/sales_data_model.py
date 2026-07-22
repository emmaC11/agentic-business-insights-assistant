from dataclasses import dataclass
from datetime import datetime

@dataclass
class SalesRecord:
    account_id: str
    location_id: str
    item: str
    category: str
    date: datetime
    quantity: float # target varibale
    price_cents: int