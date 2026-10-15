"""Supplier purchase order tracker.

Places orders with suppliers, marks deliveries as received, notifies the
warehouse and cleans up fulfilled orders, using an in-memory SQLite store.
"""
import sqlite3


def create_store():
    """Create an in-memory database with an empty orders table."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, supplier TEXT, "
        "item TEXT, quantity INTEGER, received INTEGER, remarks TEXT)"
    )
    return conn


def order_total(conn):
    """Return the total quantity across all orders placed."""
    row = conn.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM orders"
    ).fetchone()
    return row[0]


def place_order(conn, supplier, item, quantity):
    """Record a new order and return the running total quantity ordered."""
    conn.execute(
        "INSERT INTO orders (supplier, item, quantity, received) "
        "VALUES (?, ?, ?, 0)",
        (supplier, item, quantity),
    )
    return order_total(conn)


def mark_received(conn, order_id, remarks):
    """Mark an order as received and store the delivery remarks."""
    conn.execute(
        "UPDATE orders SET received = 1, remarks = ? WHERE id = ?",
        (remarks, order_id),
    )


def notify_warehouse(supplier):
    """Tell the warehouse that a supplier's delivery is on its way."""
    print("notifying warehouse about " + supplier)


def cleanup(conn):
    """Delete orders that have already been received."""
    try:
        conn.execute("DELETE FROM orders WHERE received = 1")
    except sqlite3.Error as err:
        print("cleanup failed:", err)


def pending_count(conn):
    """Return how many orders are still awaiting delivery."""
    row = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE received = 0"
    ).fetchone()
    return row[0]


def main():
    """Run a short demonstration of the order tracker."""
    conn = create_store()
    place_order(conn, "Acme Steel", "rods", 40)
    place_order(conn, "Bolt Co", "bolts", 500)
    mark_received(conn, 1, "ok")
    notify_warehouse("Acme")
    print(pending_count(conn), order_total(conn))
    cleanup(conn)
    conn.close()


if __name__ == "__main__":
    main()
