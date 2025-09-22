# src/services/report_service.py
from src.dao import report_dao

class ReportService:
    def __init__(self):
        self._dao = report_dao.ReportDAO()

    def top_5_products(self):
        return self._dao.top_selling_products()

    def total_revenue_last_month(self):
        return self._dao.total_revenue_last_month()

    def orders_per_customer(self):
        return self._dao.orders_per_customer()

    def frequent_customers(self):
        return self._dao.frequent_customers()

# default instance
default_report_service = ReportService()
