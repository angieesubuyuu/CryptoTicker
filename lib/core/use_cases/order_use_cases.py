from typing import List, Optional
from lib.core.entities.order import Order, OrderType
from lib.core.interfaces.order_repository import OrderRepository

class OrderUseCases:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def create_order(self, name: str, crypto_symbol: str, order_type: OrderType, 
                    quantity: float, price: float) -> Order:
        """Create a new order with validation"""
        if quantity <= 0 or price <= 0:
            raise ValueError("Cantidad y precio deben ser mayores a 0")

        order = Order(
            name=name,
            crypto_symbol=crypto_symbol,
            order_type=order_type,
            quantity=quantity,
            price=price,
            total_amount=quantity * price
        )
        return self.order_repository.create(order)

    def get_orders_by_name(self, name: str) -> List[Order]:
        """Get all orders for a user name"""
        return self.order_repository.get_by_name(name)

    def update_order(self, name: str, crypto_symbol: str, order_type: OrderType, quantity: float = None, price: float = None) -> Order:
        """Update an existing order by name and crypto_symbol/order_type (for demo, as no id)"""
        order = self.order_repository.get_by_name_and_crypto(name, crypto_symbol, order_type)
        if not order:
            raise ValueError("Order not found")

        if quantity is not None:
            if quantity <= 0:
                raise ValueError("Cantidad debe ser mayor a 0")
            order.quantity = quantity

        if price is not None:
            if price <= 0:
                raise ValueError("Precio debe ser mayor a 0")
            order.price = price

        order.total_amount = order.calculate_total()
        return self.order_repository.update(order)

    def delete_order(self, name: str, crypto_symbol: str, order_type: OrderType) -> bool:
        """Delete an order by name and crypto_symbol/order_type (for demo, as no id)"""
        return self.order_repository.delete_by_name_and_crypto(name, crypto_symbol, order_type)

    def get_all_orders(self) -> List[Order]:
        """Get all orders in the system"""
        return self.order_repository.get_all() 