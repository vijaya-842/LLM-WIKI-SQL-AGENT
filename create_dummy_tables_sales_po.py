"""Create 20 more dummy tables covering the sales-order-to-cash cycle and the
purchase-requisition-to-pay cycle, fanning out from the existing master tables
(vendors, items, sites) created by create_dummy_tables.py, so wiki_agent.py has a
much richer FK graph to document (ERD, cross-links, complex multi-hop queries).

Tables created (20):
    Sales side (10):
        customers, sales_reps, customer_credit_terms
        sales_orders, sales_order_lines
        shipments, shipment_lines
        sales_invoices, sales_invoice_lines
        sales_returns, sales_return_lines           (11 actually, see note below)
    Purchase side (9):
        purchase_requisitions, purchase_requisition_lines
        purchase_orders, purchase_order_lines
        po_receipts, po_receipt_lines
        vendor_invoices, vendor_invoice_lines
    Shared (1):
        payment_transactions                        (pays either a sales_invoice or a vendor_invoice)

Depends on vendors/items/sites already existing (run create_dummy_tables.py first).
Safe to re-run: drops and recreates these tables each time (CASCADE).
"""

from dbconnection import get_connection
from create_dummy_tables import VENDORS, ITEMS, SITES

DROP_SQL = """
DROP TABLE IF EXISTS payment_transactions CASCADE;
DROP TABLE IF EXISTS vendor_invoice_lines CASCADE;
DROP TABLE IF EXISTS vendor_invoices CASCADE;
DROP TABLE IF EXISTS po_receipt_lines CASCADE;
DROP TABLE IF EXISTS po_receipts CASCADE;
DROP TABLE IF EXISTS purchase_order_lines CASCADE;
DROP TABLE IF EXISTS purchase_orders CASCADE;
DROP TABLE IF EXISTS purchase_requisition_lines CASCADE;
DROP TABLE IF EXISTS purchase_requisitions CASCADE;
DROP TABLE IF EXISTS sales_return_lines CASCADE;
DROP TABLE IF EXISTS sales_returns CASCADE;
DROP TABLE IF EXISTS sales_invoice_lines CASCADE;
DROP TABLE IF EXISTS sales_invoices CASCADE;
DROP TABLE IF EXISTS shipment_lines CASCADE;
DROP TABLE IF EXISTS shipments CASCADE;
DROP TABLE IF EXISTS sales_order_lines CASCADE;
DROP TABLE IF EXISTS sales_orders CASCADE;
DROP TABLE IF EXISTS customer_credit_terms CASCADE;
DROP TABLE IF EXISTS sales_reps CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
"""

CREATE_SQL = """
CREATE TABLE customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_type VARCHAR(30),
    region VARCHAR(50),
    site VARCHAR(10) REFERENCES sites(site),
    active_flag CHAR(1) DEFAULT 'Y',
    created_timestamp TIMESTAMP DEFAULT now()
);

CREATE TABLE sales_reps (
    rep_id VARCHAR(20) PRIMARY KEY,
    rep_name VARCHAR(100) NOT NULL,
    region VARCHAR(50),
    hire_date DATE
);

CREATE TABLE customer_credit_terms (
    customer_id VARCHAR(20) PRIMARY KEY REFERENCES customers(customer_id),
    credit_limit NUMERIC(12,2),
    payment_terms VARCHAR(30),
    credit_hold_flag CHAR(1) DEFAULT 'N'
);

CREATE TABLE sales_orders (
    order_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL REFERENCES customers(customer_id),
    site VARCHAR(10) NOT NULL REFERENCES sites(site),
    rep_id VARCHAR(20) REFERENCES sales_reps(rep_id),
    order_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Open'
);

CREATE TABLE sales_order_lines (
    line_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES sales_orders(order_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    qty_ordered INTEGER NOT NULL,
    unit_price NUMERIC(10,4) NOT NULL
);

CREATE TABLE shipments (
    shipment_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES sales_orders(order_id),
    site VARCHAR(10) NOT NULL REFERENCES sites(site),
    ship_date DATE,
    carrier VARCHAR(50)
);

CREATE TABLE shipment_lines (
    line_id SERIAL PRIMARY KEY,
    shipment_id INTEGER NOT NULL REFERENCES shipments(shipment_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    qty_shipped INTEGER NOT NULL
);

CREATE TABLE sales_invoices (
    invoice_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES sales_orders(order_id),
    invoice_date DATE NOT NULL,
    total_amount NUMERIC(12,2),
    status VARCHAR(20) DEFAULT 'Unpaid'
);

CREATE TABLE sales_invoice_lines (
    line_id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL REFERENCES sales_invoices(invoice_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    qty_invoiced INTEGER NOT NULL,
    unit_price NUMERIC(10,4) NOT NULL
);

CREATE TABLE sales_returns (
    return_id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL REFERENCES sales_invoices(invoice_id),
    return_date DATE NOT NULL,
    reason VARCHAR(100)
);

CREATE TABLE sales_return_lines (
    line_id SERIAL PRIMARY KEY,
    return_id INTEGER NOT NULL REFERENCES sales_returns(return_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    qty_returned INTEGER NOT NULL
);

CREATE TABLE purchase_requisitions (
    requisition_id SERIAL PRIMARY KEY,
    site VARCHAR(10) NOT NULL REFERENCES sites(site),
    requested_by VARCHAR(100),
    request_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending'
);

CREATE TABLE purchase_requisition_lines (
    line_id SERIAL PRIMARY KEY,
    requisition_id INTEGER NOT NULL REFERENCES purchase_requisitions(requisition_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    qty_requested INTEGER NOT NULL
);

CREATE TABLE purchase_orders (
    po_id SERIAL PRIMARY KEY,
    vendor_id VARCHAR(20) NOT NULL REFERENCES vendors(vendor_id),
    site VARCHAR(10) NOT NULL REFERENCES sites(site),
    requisition_id INTEGER REFERENCES purchase_requisitions(requisition_id),
    po_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Open'
);

CREATE TABLE purchase_order_lines (
    line_id SERIAL PRIMARY KEY,
    po_id INTEGER NOT NULL REFERENCES purchase_orders(po_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    qty_ordered INTEGER NOT NULL,
    unit_cost NUMERIC(10,4) NOT NULL
);

CREATE TABLE po_receipts (
    receipt_id SERIAL PRIMARY KEY,
    po_id INTEGER NOT NULL REFERENCES purchase_orders(po_id),
    receipt_date DATE NOT NULL,
    received_by VARCHAR(100)
);

CREATE TABLE po_receipt_lines (
    line_id SERIAL PRIMARY KEY,
    receipt_id INTEGER NOT NULL REFERENCES po_receipts(receipt_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    qty_received INTEGER NOT NULL
);

CREATE TABLE vendor_invoices (
    invoice_id SERIAL PRIMARY KEY,
    po_id INTEGER NOT NULL REFERENCES purchase_orders(po_id),
    vendor_id VARCHAR(20) NOT NULL REFERENCES vendors(vendor_id),
    invoice_date DATE NOT NULL,
    total_amount NUMERIC(12,2),
    status VARCHAR(20) DEFAULT 'Unpaid'
);

CREATE TABLE vendor_invoice_lines (
    line_id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL REFERENCES vendor_invoices(invoice_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    qty_invoiced INTEGER NOT NULL,
    unit_cost NUMERIC(10,4) NOT NULL
);

CREATE TABLE payment_transactions (
    payment_id SERIAL PRIMARY KEY,
    vendor_invoice_id INTEGER REFERENCES vendor_invoices(invoice_id),
    sales_invoice_id INTEGER REFERENCES sales_invoices(invoice_id),
    payment_date DATE NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    payment_method VARCHAR(30),
    CHECK (
        (vendor_invoice_id IS NOT NULL AND sales_invoice_id IS NULL)
        OR (vendor_invoice_id IS NULL AND sales_invoice_id IS NOT NULL)
    )
);
"""

CUSTOMERS = [
    ("C00101", "Riverside Diner Group", "Independent", "Southeast", "0091"),
    ("C00102", "Metro School District", "Institutional", "Midwest", "0055"),
    ("C00103", "Harborview Hotel Chain", "Hospitality", "Northeast", "0019"),
    ("C00104", "Summit Health System", "Institutional", "West", "0078"),
    ("C00105", "Lonestar Cafe Group", "Independent", "South", "0042"),
    ("C00106", "Evergreen Senior Living", "Institutional", "West", "0063"),
    ("C00107", "Downtown Bistro Collective", "Independent", "Southeast", "0091"),
    ("C00108", "Northshore Catering Co", "Hospitality", "Northeast", "0019"),
]

SALES_REPS = [
    ("R001", "Alicia Moreno", "Southeast", "2019-02-10"),
    ("R002", "David Chen", "Midwest", "2020-06-01"),
    ("R003", "Priya Nair", "Northeast", "2018-09-15"),
    ("R004", "Marcus Webb", "West", "2021-03-22"),
    ("R005", "Sofia Reyes", "South", "2022-01-05"),
]


def seed_masters(cur):
    cur.executemany(
        "INSERT INTO customers (customer_id, customer_name, customer_type, region, site) "
        "VALUES (%s, %s, %s, %s, %s)",
        CUSTOMERS,
    )
    cur.executemany(
        "INSERT INTO sales_reps (rep_id, rep_name, region, hire_date) VALUES (%s, %s, %s, %s)",
        SALES_REPS,
    )
    credit_rows = [
        (c[0], 25000.00 + i * 5000, "Net 30" if i % 2 == 0 else "Net 45", "N")
        for i, c in enumerate(CUSTOMERS)
    ]
    cur.executemany(
        "INSERT INTO customer_credit_terms (customer_id, credit_limit, payment_terms, credit_hold_flag) "
        "VALUES (%s, %s, %s, %s)",
        credit_rows,
    )


def seed_sales_cycle(cur):
    customer_ids = [c[0] for c in CUSTOMERS]
    rep_ids = [r[0] for r in SALES_REPS]
    item_nos = [i[0] for i in ITEMS]
    site_codes = [s[0] for s in SITES]

    order_dates = ["2025-02-03", "2025-03-11", "2025-04-19", "2025-05-27", "2025-06-14", "2025-07-02"]
    order_ids = []
    for i, customer_id in enumerate(customer_ids):
        cur.execute(
            "INSERT INTO sales_orders (customer_id, site, rep_id, order_date, status) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING order_id",
            (
                customer_id,
                site_codes[i % len(site_codes)],
                rep_ids[i % len(rep_ids)],
                order_dates[i % len(order_dates)],
                "Closed" if i % 3 == 0 else "Open",
            ),
        )
        order_ids.append(cur.fetchone()[0])

    order_line_rows = []
    for i, order_id in enumerate(order_ids):
        for j in range(2):
            item_no = item_nos[(i + j) % len(item_nos)]
            order_line_rows.append((order_id, item_no, 10 + j * 5, 15.00 + j))
    cur.executemany(
        "INSERT INTO sales_order_lines (order_id, item_no, qty_ordered, unit_price) VALUES (%s, %s, %s, %s)",
        order_line_rows,
    )

    shipment_ids = []
    for i, order_id in enumerate(order_ids):
        cur.execute(
            "INSERT INTO shipments (order_id, site, ship_date, carrier) VALUES (%s, %s, %s, %s) "
            "RETURNING shipment_id",
            (order_id, site_codes[i % len(site_codes)], order_dates[i % len(order_dates)], "FleetLogix"),
        )
        shipment_ids.append(cur.fetchone()[0])

    shipment_line_rows = []
    for i, shipment_id in enumerate(shipment_ids):
        item_no = item_nos[i % len(item_nos)]
        shipment_line_rows.append((shipment_id, item_no, 10))
    cur.executemany(
        "INSERT INTO shipment_lines (shipment_id, item_no, qty_shipped) VALUES (%s, %s, %s)",
        shipment_line_rows,
    )

    invoice_ids = []
    for i, order_id in enumerate(order_ids):
        cur.execute(
            "INSERT INTO sales_invoices (order_id, invoice_date, total_amount, status) "
            "VALUES (%s, %s, %s, %s) RETURNING invoice_id",
            (
                order_id,
                order_dates[i % len(order_dates)],
                round(150.00 + i * 23.5, 2),
                "Paid" if i % 2 == 0 else "Unpaid",
            ),
        )
        invoice_ids.append(cur.fetchone()[0])

    invoice_line_rows = []
    for i, invoice_id in enumerate(invoice_ids):
        for j in range(2):
            item_no = item_nos[(i + j) % len(item_nos)]
            invoice_line_rows.append((invoice_id, item_no, 10 + j * 5, 15.00 + j))
    cur.executemany(
        "INSERT INTO sales_invoice_lines (invoice_id, item_no, qty_invoiced, unit_price) "
        "VALUES (%s, %s, %s, %s)",
        invoice_line_rows,
    )

    return_ids = []
    for invoice_id in invoice_ids[:3]:
        cur.execute(
            "INSERT INTO sales_returns (invoice_id, return_date, reason) VALUES (%s, %s, %s) "
            "RETURNING return_id",
            (invoice_id, "2025-07-20", "Damaged in transit"),
        )
        return_ids.append(cur.fetchone()[0])

    return_line_rows = [(return_id, item_nos[i % len(item_nos)], 2) for i, return_id in enumerate(return_ids)]
    cur.executemany(
        "INSERT INTO sales_return_lines (return_id, item_no, qty_returned) VALUES (%s, %s, %s)",
        return_line_rows,
    )

    return invoice_ids


def seed_purchase_cycle(cur):
    vendor_ids = [v[0] for v in VENDORS]
    item_nos = [i[0] for i in ITEMS]
    site_codes = [s[0] for s in SITES]

    req_dates = ["2025-01-15", "2025-02-20", "2025-03-25", "2025-04-30", "2025-05-15", "2025-06-20"]
    requisition_ids = []
    for i, site in enumerate(site_codes):
        cur.execute(
            "INSERT INTO purchase_requisitions (site, requested_by, request_date, status) "
            "VALUES (%s, %s, %s, %s) RETURNING requisition_id",
            (site, "Ops Manager", req_dates[i % len(req_dates)], "Approved"),
        )
        requisition_ids.append(cur.fetchone()[0])

    req_line_rows = []
    for i, requisition_id in enumerate(requisition_ids):
        item_no = item_nos[i % len(item_nos)]
        req_line_rows.append((requisition_id, item_no, 50 + i * 10))
    cur.executemany(
        "INSERT INTO purchase_requisition_lines (requisition_id, item_no, qty_requested) VALUES (%s, %s, %s)",
        req_line_rows,
    )

    po_ids = []
    for i, vendor_id in enumerate(vendor_ids):
        requisition_id = requisition_ids[i % len(requisition_ids)]
        cur.execute(
            "INSERT INTO purchase_orders (vendor_id, site, requisition_id, po_date, status) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING po_id",
            (
                vendor_id,
                site_codes[i % len(site_codes)],
                requisition_id,
                req_dates[i % len(req_dates)],
                "Closed" if i % 2 == 0 else "Open",
            ),
        )
        po_ids.append(cur.fetchone()[0])

    po_line_rows = []
    for i, po_id in enumerate(po_ids):
        for j in range(2):
            item_no = item_nos[(i + j) % len(item_nos)]
            po_line_rows.append((po_id, item_no, 50 + j * 10, 11.00 + j))
    cur.executemany(
        "INSERT INTO purchase_order_lines (po_id, item_no, qty_ordered, unit_cost) VALUES (%s, %s, %s, %s)",
        po_line_rows,
    )

    receipt_ids = []
    for i, po_id in enumerate(po_ids):
        cur.execute(
            "INSERT INTO po_receipts (po_id, receipt_date, received_by) VALUES (%s, %s, %s) "
            "RETURNING receipt_id",
            (po_id, req_dates[i % len(req_dates)], "Warehouse Lead"),
        )
        receipt_ids.append(cur.fetchone()[0])

    receipt_line_rows = []
    for i, receipt_id in enumerate(receipt_ids):
        item_no = item_nos[i % len(item_nos)]
        receipt_line_rows.append((receipt_id, item_no, 48))
    cur.executemany(
        "INSERT INTO po_receipt_lines (receipt_id, item_no, qty_received) VALUES (%s, %s, %s)",
        receipt_line_rows,
    )

    vendor_invoice_ids = []
    for i, po_id in enumerate(po_ids):
        vendor_id = vendor_ids[i]
        cur.execute(
            "INSERT INTO vendor_invoices (po_id, vendor_id, invoice_date, total_amount, status) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING invoice_id",
            (
                po_id,
                vendor_id,
                req_dates[i % len(req_dates)],
                round(1100.00 + i * 87.3, 2),
                "Paid" if i % 2 == 0 else "Unpaid",
            ),
        )
        vendor_invoice_ids.append(cur.fetchone()[0])

    vendor_invoice_line_rows = []
    for i, invoice_id in enumerate(vendor_invoice_ids):
        for j in range(2):
            item_no = item_nos[(i + j) % len(item_nos)]
            vendor_invoice_line_rows.append((invoice_id, item_no, 50 + j * 10, 11.00 + j))
    cur.executemany(
        "INSERT INTO vendor_invoice_lines (invoice_id, item_no, qty_invoiced, unit_cost) "
        "VALUES (%s, %s, %s, %s)",
        vendor_invoice_line_rows,
    )

    return vendor_invoice_ids


def seed_payments(cur, sales_invoice_ids, vendor_invoice_ids):
    payment_rows = []
    for i, invoice_id in enumerate(sales_invoice_ids):
        if i % 2 == 0:
            payment_rows.append((None, invoice_id, "2025-07-25", 300.00, "ACH"))
    for i, invoice_id in enumerate(vendor_invoice_ids):
        if i % 2 == 0:
            payment_rows.append((invoice_id, None, "2025-07-28", 1200.00, "Wire"))
    cur.executemany(
        "INSERT INTO payment_transactions (vendor_invoice_id, sales_invoice_id, payment_date, amount, payment_method) "
        "VALUES (%s, %s, %s, %s, %s)",
        payment_rows,
    )


def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            print("[schema] dropping old sales/PO dummy tables (if any)...")
            cur.execute(DROP_SQL)
            print("[schema] creating 20 tables...")
            cur.execute(CREATE_SQL)
            print("[data] seeding master data (customers, sales reps, credit terms)...")
            seed_masters(cur)
            print("[data] seeding sales order-to-cash cycle...")
            sales_invoice_ids = seed_sales_cycle(cur)
            print("[data] seeding purchase requisition-to-pay cycle...")
            vendor_invoice_ids = seed_purchase_cycle(cur)
            print("[data] seeding payment transactions...")
            seed_payments(cur, sales_invoice_ids, vendor_invoice_ids)
            conn.commit()
        print("Done. Run `python wiki_agent.py` to regenerate the wiki over the new schema.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
