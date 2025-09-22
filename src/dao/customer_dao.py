# src/dao/customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class CustomerError(Exception):
    pass


class CustomerDAO:
    """Direct DB access for customers table."""
    
    def __init__(self):
        self._db = get_supabase().table("customers")

    def _first_or_none(self, resp) -> Optional[Dict]:
        return resp.data[0] if getattr(resp, "data", None) else None

    def email_exists(self, email: str) -> bool:
        resp = self._db.select("*").eq("email", email).limit(1).execute()
        return bool(resp.data)

    def create(self, name: str, email: str, phone: str, city: str) -> Optional[Dict]:
        if self.email_exists(email):
            return None
        payload = {"name": name, "email": email, "phone": phone, "city": city}
        self._db.insert(payload).execute()
        resp = self._db.select("*").eq("email", email).limit(1).execute()
        return self._first_or_none(resp)

    def update(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        self._db.update(fields).eq("cust_id", cust_id).execute()
        resp = self._db.select("*").eq("cust_id", cust_id).limit(1).execute()
        return self._first_or_none(resp)

    def delete(self, cust_id: int) -> Optional[Dict]:
        # fetch row before delete
        resp_before = self._db.select("*").eq("cust_id", cust_id).limit(1).execute()
        row = self._first_or_none(resp_before)
        self._db.delete().eq("cust_id", cust_id).execute()
        return row

    def list(self, limit: int = 100) -> List[Dict]:
        resp = self._db.select("*").order("cust_id").limit(limit).execute()
        return resp.data or []

    def search(self, email: str = None, city: str = None) -> List[Dict]:
        q = self._db.select("*")
        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return resp.data or []
