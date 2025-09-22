# 🛒 Retail Inventory Order Management System

A modular **command-line application** for managing retail operations — products, customers, orders, payments, and reporting.  
Built with **Python** and **Supabase** as the backend database.

---

## 📌 Features

### ✅ Products
- Add, update, delete, and list products.
- Manage stock (increase/restock, auto-deduct on orders).
- Search by SKU, category, or name.

### ✅ Customers
- Add, update, delete, and list customers.
- Search customers by email or city.

### ✅ Orders
- Create new orders for customers.
- Validate stock and deduct quantities automatically.
- Cancel orders (restores stock, updates status).
- Mark orders as completed after payment.
- Fetch detailed order info (customer + items).

### ✅ Payments
- Pending payment record created when order is placed.
- Process payment (Cash, Card, UPI).
- Refunds supported when order is cancelled.
- Syncs payment status with order status.

### ✅ Reporting
- Top 5 selling products (by quantity sold).
- Total revenue in the last month.
- Orders placed by each customer.
- Frequent customers (more than 2 orders).

---

## 📂 Project Structure

```
retail_inventory_order_management/
│
├── src/
│   ├── cli/
│   │   └── main.py              # CLI entry point using argparse
│   │
│   ├── dao/                     # Data Access Layer (direct DB queries)
│   │   ├── product_dao.py
│   │   ├── customer_dao.py
│   │   ├── order_dao.py
│   │   ├── payment_dao.py
│   │   └── report_dao.py
│   │
│   ├── services/                # Business Logic Layer
│   │   ├── product_service.py
│   │   ├── customer_service.py
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   └── report_service.py
│   │
│   ├── config.py                # Database connection (Supabase client)
│   └── utils.py                 # Helper functions
│
├── requirements.txt             # Dependencies
└── README.md                    # Project documentation
```

---

## ⚙️ Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/retail_inventory_order_management.git
   cd retail_inventory_order_management
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure **Supabase** in `config.py`:
   ```python
   SUPABASE_URL = "your-supabase-url"
   SUPABASE_KEY = "your-supabase-key"
   ```

---

## 🚀 Usage

Run the CLI:
```bash
python -m src.cli.main <command> [options]
```

### 🔹 Product Commands
```bash
python -m src.cli.main product add --name "Mouse" --sku "M-001" --price 599 --stock 20 --category "Accessories"
python -m src.cli.main product list
```

### 🔹 Customer Commands
```bash
python -m src.cli.main customer add --name "Alice" --email "alice@example.com" --city "Hyderabad"
python -m src.cli.main customer list
```

### 🔹 Order Commands
```bash
python -m src.cli.main order create --customer 1 --items "1:2,3:1"
python -m src.cli.main order show --id 1
python -m src.cli.main order cancel --id 1
```

### 🔹 Payment Commands
```bash
python -m src.cli.main payment process --order 1 --method "UPI"
python -m src.cli.main payment refund --order 1
```

### 🔹 Reporting Commands
```bash
python -m src.cli.main report top5
python -m src.cli.main report revenue
python -m src.cli.main report orders_per_customer
python -m src.cli.main report frequent_customers
```

---

## 🧩 Module Design

- **DAO Layer** → Talks directly to database.
- **Service Layer** → Business logic, validation, rules.
- **CLI Layer** → User interface (argparse commands).

**Flow Example (Order Creation):**
```
CLI → OrderService → OrderDAO → DB (orders, order_items)
             └── ProductDAO (update stock)
             └── PaymentService (pending payment)
```

---

## 📊 Example Report Outputs

**Top 5 Products:**
```
1. Laptop (120 sold)
2. Mouse (95 sold)
3. Keyboard (80 sold)
4. Headphones (60 sold)
5. Monitor (50 sold)
```

**Total Revenue (Last Month):**
```
₹1,25,000
```

**Orders per Customer:**
```
Alice → 3 orders
Bob → 1 order
Charlie → 5 orders
```

**Frequent Customers (>2 Orders):**
```
Alice
Charlie
```

---

## 👨‍💻 Tech Stack

- **Python 3.11+**
- **Supabase (PostgreSQL backend)**
- **argparse** (for CLI interface)
