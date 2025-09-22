# src/cli/main.py
import argparse
import json
from src.services import product_service
from src.dao.customer_dao import CustomerDAO
from src.dao.product_dao import ProductDAO
from src.services import order_service  # the new OrderService module

# Instantiate DAOs
product_dao_instance = ProductDAO()
customer_dao_instance = CustomerDAO()
order_service_instance = order_service.default_order_service  # singleton instance

# --------------------- PRODUCT COMMANDS ---------------------
def cmd_product_add(args):
    try:
        p = product_service.add_product(
            args.name, args.sku, args.price, args.stock, args.category
        )
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_list(args):
    ps = product_dao_instance.list_products(limit=100)
    print(json.dumps(ps, indent=2, default=str))


# --------------------- CUSTOMER COMMANDS ---------------------
def cmd_customer_add(args):
    try:
        c = customer_dao_instance.create(
            args.name, args.email, args.phone, args.city
        )
        if c:
            print("Created customer:")
            print(json.dumps(c, indent=2, default=str))
        else:
            print(f"Customer with email {args.email} already exists")
    except Exception as e:
        print("Error:", e)


# --------------------- ORDER COMMANDS ---------------------
def cmd_order_create(args):
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "qty": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        ord = order_service_instance.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(ord, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_show(args):
    try:
        o = order_service_instance.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_cancel(args):
    try:
        o = order_service_instance.cancel_order(args.order)
        print("Order cancelled (updated):")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_order_complete(args):
    try:
        o = order_service_instance.complete_order(args.order)
        print("Order marked as COMPLETED:")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)


# --------------------- PAYMENT COMMANDS ---------------------

# process payment
def cmd_payment_process(args):
    from src.services import payment_service
    try:
        p = payment_service.default_payment_service.process_payment(args.order, args.method)
        print("Payment processed:")
        print(json.dumps(p, indent=2))
    except Exception as e:
        print("Error:", e)

# refund payment
def cmd_payment_refund(args):
    from src.services import payment_service
    try:
        p = payment_service.default_payment_service.refund_payment(args.order)
        print("Payment refunded:")
        print(json.dumps(p, indent=2))
    except Exception as e:
        print("Error:", e)

# --------------------- REPORT COMMANDS ---------------------

def cmd_report_top5(args):
    from src.services import report_service
    data = report_service.default_report_service.top_5_products()
    print(json.dumps(data, indent=2))

def cmd_report_revenue(args):
    from src.services import report_service
    data = report_service.default_report_service.total_revenue_last_month()
    print("Total revenue last month:", data)

def cmd_report_orders(args):
    from src.services import report_service
    data = report_service.default_report_service.orders_per_customer()
    print(json.dumps(data, indent=2))

def cmd_report_frequent(args):
    from src.services import report_service
    data = report_service.default_report_service.frequent_customers()
    print(json.dumps(data, indent=2))




# --------------------- PARSER SETUP ---------------------
def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")

    # Product
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)
    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    # Customer
    pcust = sub.add_parser("customer")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)

    # Order
    porder = sub.add_parser("order")
    porder_sub = porder.add_subparsers(dest="action")
    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)

    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)

    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    compo = porder_sub.add_parser("complete")
    compo.add_argument("--order", type=int, required=True)
    compo.set_defaults(func=cmd_order_complete)


    # Payment
    p_pay = sub.add_parser("payment")
    p_pay_sub = p_pay.add_subparsers(dest="action")

    proc = p_pay_sub.add_parser("process")
    proc.add_argument("--order", type=int, required=True)
    proc.add_argument("--method", choices=["Cash","Card","UPI"], required=True)
    proc.set_defaults(func=cmd_payment_process)

    refund = p_pay_sub.add_parser("refund")
    refund.add_argument("--order", type=int, required=True)
    refund.set_defaults(func=cmd_payment_refund)



    #report
    p_report = sub.add_parser("report")
    p_report_sub = p_report.add_subparsers(dest="action")

    p_top5 = p_report_sub.add_parser("top5")
    p_top5.set_defaults(func=cmd_report_top5)

    p_rev = p_report_sub.add_parser("revenue")
    p_rev.set_defaults(func=cmd_report_revenue)

    p_orders = p_report_sub.add_parser("orders_per_customer")
    p_orders.set_defaults(func=cmd_report_orders)

    p_freq = p_report_sub.add_parser("frequent_customers")
    p_freq.set_defaults(func=cmd_report_frequent)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
