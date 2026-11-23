"""Idempotent additive migrations for the project's database.

Never re-seed or reclassify existing purchases. New columns have conservative
defaults; legacy orders do not acquire stock reservations retroactively.
"""
from sqlalchemy import inspect, text

ADDITIONS = {
    "orders": {
        "checkout_key": "VARCHAR(64)",
        "checkout_fingerprint": "VARCHAR(64)",
        "access_token_hash": "VARCHAR(64)",
        "expires_at": "DATETIME",
        "delivered_at": "DATETIME",
        "stock_reserved": "BOOLEAN NOT NULL DEFAULT 0",
        "promo_claimed": "BOOLEAN NOT NULL DEFAULT 0",
        "rewards_credited": "BOOLEAN NOT NULL DEFAULT 0",
        "events": "JSON",
        "discount_code": "VARCHAR(64)",
        "shipping_carrier": "VARCHAR(100) DEFAULT 'vet_express'",
        "delivery_lat": "FLOAT",
        "delivery_lng": "FLOAT",
        "delivery_notes": "VARCHAR(500)",
        "map_url": "VARCHAR(255)",
        "payway_gateway": "VARCHAR(150)",
        "payway_started_at": "DATETIME",
        "payway_qr": "TEXT",
    },
    "users": {"profile_data": "JSON", "token_version": "INTEGER NOT NULL DEFAULT 1"},
    "articles": {"tags": "JSON", "status": "VARCHAR(30) NOT NULL DEFAULT 'Published'"},
    "return_requests": {"order_item_id": "INTEGER", "refund_reference": "VARCHAR(150)"},
    "order_items": {"returned_quantity": "INTEGER NOT NULL DEFAULT 0"},
}

def migrate_schema(engine, *, seed_demo_promotions=True):
    with engine.begin() as connection:
        inspector = inspect(connection)
        for table, columns in ADDITIONS.items():
            if not inspector.has_table(table):
                continue
            existing = {c["name"] for c in inspector.get_columns(table)}
            for name, sql_type in columns.items():
                if name not in existing:
                    if connection.dialect.name == "postgresql":
                        sql_type = {"DATETIME": "TIMESTAMP", "BOOLEAN NOT NULL DEFAULT 0": "BOOLEAN NOT NULL DEFAULT FALSE"}.get(sql_type, sql_type)
                    connection.execute(text(f'ALTER TABLE "{table}" ADD COLUMN "{name}" {sql_type}'))
        if inspector.has_table("orders"):
            order_cols = {c["name"] for c in inspector.get_columns("orders")}
            if "checkout_key" in order_cols:
                connection.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ix_orders_checkout_key ON orders (checkout_key)'))
            if {"user_id", "status", "payment_method"}.issubset(order_cols):
                connection.execute(text("""
                    CREATE UNIQUE INDEX IF NOT EXISTS ix_orders_user_awaiting_cod 
                    ON orders (user_id) 
                    WHERE status = 'Awaiting Confirmation' AND payment_method = 'cod'
                """))
            if {"discount_code", "status", "promo_claimed"}.issubset(order_cols):
                if connection.dialect.name == "postgresql":
                    connection.execute(text("""
                        UPDATE orders 
                        SET promo_claimed = TRUE 
                        WHERE discount_code IS NOT NULL AND status NOT IN ('Cancelled', 'Expired') AND (promo_claimed IS FALSE OR promo_claimed IS NULL)
                    """))
                else:
                    connection.execute(text("""
                        UPDATE orders 
                        SET promo_claimed = 1 
                        WHERE discount_code IS NOT NULL AND status NOT IN ('Cancelled', 'Expired') AND (promo_claimed = 0 OR promo_claimed IS NULL)
                    """))
        if inspector.has_table('articles'):
            connection.execute(text("UPDATE articles SET tags='[]' WHERE tags IS NULL"))
        if inspector.has_table('order_items') and inspector.has_table('return_requests'):
            connection.execute(text("""
                UPDATE order_items SET returned_quantity = COALESCE((
                    SELECT SUM(rr.quantity) FROM return_requests rr
                    WHERE rr.order_item_id = order_items.id
                    AND rr.status NOT IN ('Rejected', 'rejected')
                ), 0)
            """))
        if connection.dialect.name == "postgresql" and inspector.has_table("products") and inspector.has_table("categories"):
            fk_rows = connection.execute(text("""
                SELECT con.conname, con.confdeltype
                FROM pg_constraint con
                JOIN pg_class rel ON rel.oid = con.conrelid
                JOIN pg_class frel ON frel.oid = con.confrelid
                WHERE rel.relname = 'products'
                  AND frel.relname = 'categories'
                  AND con.contype = 'f'
            """)).fetchall()
            for conname, confdeltype in fk_rows:
                if confdeltype == 'c':  # CASCADE
                    connection.execute(text(f'ALTER TABLE products DROP CONSTRAINT "{conname}"'))
                    connection.execute(text(f'ALTER TABLE products ADD CONSTRAINT "{conname}" FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT'))
        connection.execute(text('CREATE TABLE IF NOT EXISTS flow_migrations (name VARCHAR(100) PRIMARY KEY)'))
        if seed_demo_promotions and inspector.has_table('promotions') and not connection.execute(text("SELECT name FROM flow_migrations WHERE name='initial_promotions'")).first():
            for code, percent in [('LUMEA10', 10), ('ATELIER15', 15), ('LUMEA20', 20)]:
                connection.execute(text(
                    'INSERT INTO promotions (name, code, percent, max_uses, used, status, is_featured) '
                    'VALUES (:code, :code, :percent, 1000, 0, :status, FALSE) ON CONFLICT (code) DO NOTHING'
                ), {'code': code, 'percent': percent, 'status': 'Active'})
            connection.execute(text("INSERT INTO flow_migrations (name) VALUES ('initial_promotions')"))
