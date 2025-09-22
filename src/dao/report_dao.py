# src/dao/report_dao.py
from src.config import get_supabase
from datetime import datetime, timedelta

class ReportDAO:
    def __init__(self):
        self.db_orders = get_supabase().table("orders")
        self.db_items = get_supabase().table("order_items")
        self.db_products = get_supabase().table("products")
        self.db_customers = get_supabase().table("customers")

    # Top 5 selling products by quantity
    def top_selling_products(self):
        items = self.db_items.select("*").execute().data or []
        summary = {}
        for i in items:
            summary[i["prod_id"]] = summary.get(i["prod_id"], 0) + i["quantity"]
        top5 = sorted(summary.items(), key=lambda x: x[1], reverse=True)[:5]
        result = []
        for pid, qty in top5:
            product = self.db_products.select("*").eq("prod_id", pid).limit(1).execute().data[0]
            result.append({"product": product["name"], "quantity_sold": qty})
        return result

    # Total revenue in last month
    def total_revenue_last_month(self):
        today = datetime.today()
        last_month = today - timedelta(days=30)
        orders = self.db_orders.select("*").gte("created_at", last_month.isoformat()).execute().data or []
        return sum(o.get("total_amount",0) for o in orders)

    # Total orders per customer
    def orders_per_customer(self):
        orders = self.db_orders.select("*").execute().data or []
        summary = {}
        for o in orders:
            cid = o["customer_id"]
            summary[cid] = summary.get(cid,0)+1
        result = []
        for cid, count in summary.items():
            customer = self.db_customers.select("*").eq("cust_id", cid).limit(1).execute().data[0]
            result.append({"customer": customer["name"], "orders_count": count})
        return result

    # Customers with more than 2 orders
    def frequent_customers(self):
        data = self.orders_per_customer()
        return [d for d in data if d["orders_count"] > 2]
