from datetime import datetime
from typing import List, Optional
from lib.core.entities.order import Order, OrderType
from lib.core.interfaces.order_repository import OrderRepository
from lib.core.db_config import DatabaseConnection

class MySQLOrderRepository(OrderRepository):
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def create(self, order: Order) -> Order:
        query = """
        INSERT INTO orders (name, crypto_symbol, order_type, quantity, price, total_amount, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            order.name,
            order.crypto_symbol,
            order.order_type.value,
            order.quantity,
            order.price,
            order.total_amount,
            datetime.now()
        )
        self.db.execute_update(query, params)
        return order

    def get_by_name(self, name: str) -> List[Order]:
        query = "SELECT * FROM orders WHERE name = %s ORDER BY created_at DESC"
        results = self.db.execute_query(query, (name,))
        return [self._map_to_order(row) for row in results]

    def get_by_name_and_crypto(self, name: str, crypto_symbol: str, order_type: OrderType) -> Optional[Order]:
        query = "SELECT * FROM orders WHERE name = %s AND crypto_symbol = %s AND order_type = %s"
        result = self.db.execute_query(query, (name, crypto_symbol, order_type.value))
        if result and len(result) > 0:
            return self._map_to_order(result[0])
        return None

    def update(self, order: Order) -> Order:
        query = """
        UPDATE orders 
        SET quantity = %s, price = %s, total_amount = %s
        WHERE name = %s AND crypto_symbol = %s AND order_type = %s
        """
        params = (order.quantity, order.price, order.total_amount, order.name, order.crypto_symbol, order.order_type.value)
        self.db.execute_update(query, params)
        return order

    def delete_by_name_and_crypto(self, name: str, crypto_symbol: str, order_type: OrderType) -> bool:
        query = "DELETE FROM orders WHERE name = %s AND crypto_symbol = %s AND order_type = %s"
        return self.db.execute_update(query, (name, crypto_symbol, order_type.value))

    def _map_to_order(self, row: tuple) -> Order:
        """Map database row to Order entity"""
        return Order(
            name=row[0],
            crypto_symbol=row[1],
            order_type=OrderType(row[2]),
            quantity=row[3],
            price=row[4],
            total_amount=row[5],
            created_at=row[6]
        ) 