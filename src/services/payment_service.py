# src/services/payment_service.py
from src.dao import payment_dao, order_dao

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self):
        self._payment_dao = payment_dao.PaymentDAO()
        self._order_dao = order_dao.OrderDAO()

    # Insert pending payment when order is created
    def create_pending_payment(self, order_id: int, amount: float):
        return self._payment_dao.create_payment(order_id, amount)

    # Process payment
    def process_payment(self, order_id: int, method: str):
        payment = self._payment_dao.get_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        if payment["status"] == "PAID":
            raise PaymentError("Payment already completed")
        self._payment_dao.update_payment(payment["payment_id"], {"status": "PAID", "method": method})
        # update order status to COMPLETED
        self._order_dao.update_order(order_id, {"status": "COMPLETED"})
        return self._payment_dao.get_by_order(order_id)

    # Refund payment
    def refund_payment(self, order_id: int):
        payment = self._payment_dao.get_by_order(order_id)
        if not payment:
            raise PaymentError("Payment record not found")
        self._payment_dao.update_payment(payment["payment_id"], {"status": "REFUNDED"})
        return self._payment_dao.get_by_order(order_id)


# default instance
default_payment_service = PaymentService()
