# src/services/product_service.py
from typing import List, Dict, Optional
import src.dao.product_dao as product_dao


class ProductError(Exception):
    """Custom exception for product-related errors."""
    pass


class ProductService:
    """OOP Service layer for product operations."""
    
    def __init__(self, dao: Optional[object] = None):
        # allow dependency injection; default to procedural DAO module
        self._dao = dao or product_dao

    def add_product(self, name: str, sku: str, price: float, stock: int = 0, category: Optional[str] = None) -> Dict:
        if price <= 0:
            raise ProductError("Price must be greater than 0")
        if self._dao.get_product_by_sku(sku):
            raise ProductError(f"SKU already exists: {sku}")
        return self._dao.create_product(name, sku, price, stock, category)

    def restock_product(self, prod_id: int, delta: int) -> Dict:
        if delta <= 0:
            raise ProductError("Delta must be positive")
        product = self._dao.get_product_by_id(prod_id)
        if not product:
            raise ProductError("Product not found")
        new_stock = (product.get("stock") or 0) + delta
        return self._dao.update_product(prod_id, {"stock": new_stock})

    def get_low_stock(self, threshold: int = 5) -> List[Dict]:
        all_products = self._dao.list_products(limit=1000)
        return [p for p in all_products if (p.get("stock") or 0) <= threshold]


# Default instance for convenience
default_product_service = ProductService()
