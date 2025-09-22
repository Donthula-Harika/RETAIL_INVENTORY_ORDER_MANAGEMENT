# src/dao/payment_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class PaymentDAO:
    def __init__(self):
        self.db = get_supabase().table("payments")

    def create_payment(self, order_id: int, amount: float) -> Dict:
        payload = {"order_id": order_id, "amount": amount, "status": "PENDING", "method": None}
        self.db.insert(payload).execute()
        resp = self.db.select("*").eq("order_id", order_id).order("payment_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_payment(self, payment_id: int, fields: Dict) -> Optional[Dict]:
        self.db.update(fields).eq("payment_id", payment_id).execute()
        resp = self.db.select("*").eq("payment_id", payment_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_by_order(self, order_id: int) -> Optional[Dict]:
        resp = self.db.select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None
