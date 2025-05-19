from abc import ABC, abstractmethod
from typing import List, Optional
from lib.core.entities.order import Order, OrderType

class OrderRepository(ABC):
    @abstractmethod
    def create(self, order: Order) -> Order:
        """Create a new order"""
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> List[Order]:
        """Get all orders for a specific user name"""
        pass

    @abstractmethod
    def get_by_name_and_crypto(self, name: str, crypto_symbol: str, order_type: OrderType) -> Optional[Order]:
        """Get an order by name, crypto_symbol, and order_type"""
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        """Update an existing order"""
        pass

    @abstractmethod
    def delete_by_name_and_crypto(self, name: str, crypto_symbol: str, order_type: OrderType) -> bool:
        """Delete an order by name, crypto_symbol, and order_type"""
        pass

    @abstractmethod
    def get_all(self) -> List[Order]:
        """Get all orders in the system"""
        pass 