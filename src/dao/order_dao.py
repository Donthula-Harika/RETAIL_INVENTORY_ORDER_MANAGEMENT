# src/dao/order_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class OrderDAO:
    def __init__(self):
        self.db = get_supabase().table("orders")
        self.items_db = get_supabase().table("order_items")

    # Create order record
    def create_order(self, customer_id: int, total_amount: float) -> Dict:
        payload = {"customer_id": customer_id, "total_amount": total_amount, "status": "PLACED"}
        self.db.insert(payload).execute()
        resp = self.db.select("*").eq("customer_id", customer_id).order("order_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    # Add order items
    def add_order_items(self, order_id: int, items: List[Dict]):
        for item in items:
            payload = {"order_id": order_id, "prod_id": item["prod_id"], "quantity": item["qty"]}
            self.items_db.insert(payload).execute()

    def get_order(self, order_id: int) -> Optional[Dict]:
        resp = self.db.select("*").eq("order_id", order_id).limit(1).execute()
        order = resp.data[0] if resp.data else None
        if not order:
            return None
        # fetch items
        items_resp = self.items_db.select("*").eq("order_id", order_id).execute()
        order["items"] = items_resp.data or []
        return order

    def list_orders_by_customer(self, customer_id: int) -> List[Dict]:
        resp = self.db.select("*").eq("customer_id", customer_id).execute()
        return resp.data or []

    def update_order(self, order_id: int, fields: Dict) -> Optional[Dict]:
        self.db.update(fields).eq("order_id", order_id).execute()
        return self.get_order(order_id)
