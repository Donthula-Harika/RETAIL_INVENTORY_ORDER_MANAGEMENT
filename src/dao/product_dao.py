# src/dao/product_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class ProductDAO:
    def __init__(self):
        self.db = get_supabase().table("products")

    def create_product(self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category:
            payload["category"] = category
        # insert
        get_supabase().table("products").insert(payload).execute()
        # fetch inserted row
        resp = get_supabase().table("products").select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_product_by_id(self, prod_id: int) -> Optional[Dict]:
        resp = self.db.select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_product_by_sku(self, sku: str) -> Optional[Dict]:
        resp = self.db.select("*").eq("sku", sku).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_product(self, prod_id: int, fields: Dict) -> Optional[Dict]:
        self.db.update(fields).eq("prod_id", prod_id).execute()
        resp = self.db.select("*").eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_product(self, prod_id: int) -> Optional[Dict]:
        before = self.get_product_by_id(prod_id)
        self.db.delete().eq("prod_id", prod_id).execute()
        return before

    def list_products(self, limit: int = 100, category: str | None = None) -> List[Dict]:
        q = self.db.select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []
