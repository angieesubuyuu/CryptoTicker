from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class OrderType(Enum):
    BUY = "BUY"
    SELL = "SELL"

@dataclass
class Order:
    name: str = None
    crypto_symbol: str = None
    order_type: OrderType = None
    quantity: float = None
    price: float = None
    total_amount: float = None
    created_at: datetime = None

    def calculate_total(self) -> float:
        """Calculate the total amount of the order"""
        return self.quantity * self.price 