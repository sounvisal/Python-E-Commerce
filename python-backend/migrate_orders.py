import sqlite3

conn = sqlite3.connect("lumea.db")
cols = [c[1] for c in conn.execute("PRAGMA table_info(orders)").fetchall()]
if "payment_status" not in cols:
    conn.execute("ALTER TABLE orders ADD COLUMN payment_status VARCHAR(50) DEFAULT 'Paid'")
    print("Added payment_status")
if "transaction_ref" not in cols:
    conn.execute("ALTER TABLE orders ADD COLUMN transaction_ref VARCHAR(100)")
    print("Added transaction_ref")
conn.commit()
print("Final orders columns:", [c[1] for c in conn.execute("PRAGMA table_info(orders)").fetchall()])
conn.close()
