# src/services/order_service.py
from typing import List, Dict
from src.dao import order_dao, product_dao, customer_dao

class OrderError(Exception):
    pass

class OrderService:
    def __init__(self, order_dao_instance=None, product_dao_instance=None, customer_dao_instance=None):
        self._order_dao = order_dao_instance or order_dao.OrderDAO()
        self._product_dao = product_dao_instance or product_dao.ProductDAO()
        self._customer_dao = customer_dao_instance or customer_dao.CustomerDAO()

    # Create order
    def create_order(self, customer_id: int, items: List[Dict]) -> Dict:
        # check customer exists
        if not self._customer_dao.get_by_id(customer_id):
            raise OrderError(f"Customer {customer_id} does not exist")

        total_amount = 0
        # check stock
        for item in items:
            product = self._product_dao.get_product_by_id(item["prod_id"])
            if not product:
                raise OrderError(f"Product {item['prod_id']} not found")
            if (product.get("stock") or 0) < item["qty"]:
                raise OrderError(f"Insufficient stock for {product['name']}")
            total_amount += product["price"] * item["qty"]

        # deduct stock
        for item in items:
            product = self._product_dao.get_product_by_id(item["prod_id"])
            new_stock = (product.get("stock") or 0) - item["qty"]
            self._product_dao.update_product(product["prod_id"], {"stock": new_stock})

        # create order and order_items
        order = self._order_dao.create_order(customer_id, total_amount)
        self._order_dao.add_order_items(order["order_id"], items)
        return self.get_order_details(order["order_id"])

    def get_order_details(self, order_id: int) -> Dict:
        order = self._order_dao.get_order(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found")
        # fetch customer info
        customer = self._customer_dao.get_by_id(order["customer_id"])
        order["customer"] = customer
        return order

    def list_customer_orders(self, customer_id: int) -> List[Dict]:
        return self._order_dao.list_orders_by_customer(customer_id)

    def cancel_order(self, order_id: int) -> Dict:
        order = self._order_dao.get_order(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found")
        if order.get("status") != "PLACED":
            raise OrderError("Only PLACED orders can be cancelled")
        # restore stock
        for item in order.get("items", []):
            product = self._product_dao.get_product_by_id(item["prod_id"])
            new_stock = (product.get("stock") or 0) + item["quantity"]
            self._product_dao.update_product(product["prod_id"], {"stock": new_stock})
        # update order status
        return self._order_dao.update_order(order_id, {"status": "CANCELLED"})

    def complete_order(self, order_id: int) -> Dict:
        order = self._order_dao.get_order(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found")
        return self._order_dao.update_order(order_id, {"status": "COMPLETED"})


# default instance
default_order_service = OrderService()

