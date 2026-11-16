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
        "events": "JSON",
        "discount_code": "VARCHAR(64)",
    },
    "users": {"profile_data": "JSON"},
    "articles": {"tags": "JSON", "status": "VARCHAR(30) NOT NULL DEFAULT 'Published'"},
    "return_requests": {"order_item_id": "INTEGER", "refund_reference": "VARCHAR(150)"},
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
            connection.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ix_orders_checkout_key ON orders (checkout_key)'))
        if inspector.has_table('articles'):
            connection.execute(text("UPDATE articles SET tags='[]' WHERE tags IS NULL"))
        connection.execute(text('CREATE TABLE IF NOT EXISTS flow_migrations (name VARCHAR(100) PRIMARY KEY)'))
        if seed_demo_promotions and inspector.has_table('promotions') and not connection.execute(text("SELECT name FROM flow_migrations WHERE name='initial_promotions'")).first():
            for code, percent in [('LUMEA10', 10), ('ATELIER15', 15), ('LUMEA20', 20)]:
                connection.execute(text(
                    'INSERT INTO promotions (name, code, percent, max_uses, used, status, is_featured) '
                    'VALUES (:code, :code, :percent, 1000, 0, :status, FALSE) ON CONFLICT (code) DO NOTHING'
                ), {'code': code, 'percent': percent, 'status': 'Active'})
            connection.execute(text("INSERT INTO flow_migrations (name) VALUES ('initial_promotions')"))
