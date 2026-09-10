"""Create a small dummy relational schema fanning out from vendors/source_vendors, seeded partly
from the real codes already in growth_opportunity_event, so wiki_agent.py has FK relationships
worth documenting (ERD, cross-links) instead of one isolated table.

Tables created (10):
    vendors, source_vendors, items, sites                (master/reference tables)
    vendor_pricing, source_vendor_pricing                 (price history)
    vendor_contracts, vendor_shipping_points               (vendor detail)
    site_vendor_assignments, vendor_performance            (relationship/fact tables)

Also adds FK constraints from growth_opportunity_event.true_vendor/source_vendor/item_no/site
into the new master tables, so the existing table joins the FK graph.

Safe to re-run: drops and recreates the 10 new tables each time (CASCADE), and skips the
growth_opportunity_event FKs if they already exist.
"""

from dbconnection import get_connection

DROP_SQL = """
DROP TABLE IF EXISTS vendor_performance CASCADE;
DROP TABLE IF EXISTS site_vendor_assignments CASCADE;
DROP TABLE IF EXISTS vendor_shipping_points CASCADE;
DROP TABLE IF EXISTS vendor_contracts CASCADE;
DROP TABLE IF EXISTS source_vendor_pricing CASCADE;
DROP TABLE IF EXISTS vendor_pricing CASCADE;
DROP TABLE IF EXISTS sites CASCADE;
DROP TABLE IF EXISTS items CASCADE;
DROP TABLE IF EXISTS source_vendors CASCADE;
DROP TABLE IF EXISTS vendors CASCADE;
"""

CREATE_SQL = """
CREATE TABLE vendors (
    vendor_id VARCHAR(20) PRIMARY KEY,
    vendor_name VARCHAR(100) NOT NULL,
    vendor_type VARCHAR(30),
    active_flag CHAR(1) DEFAULT 'Y',
    onboarded_date DATE,
    created_timestamp TIMESTAMP DEFAULT now()
);

CREATE TABLE source_vendors (
    source_vendor_id VARCHAR(20) PRIMARY KEY,
    source_vendor_name VARCHAR(100) NOT NULL,
    source_vendor_group VARCHAR(50),
    region VARCHAR(50),
    created_timestamp TIMESTAMP DEFAULT now()
);

CREATE TABLE items (
    item_no VARCHAR(20) PRIMARY KEY,
    item_desc VARCHAR(200),
    brand VARCHAR(50),
    item_size VARCHAR(30),
    pack INTEGER
);

CREATE TABLE sites (
    site VARCHAR(10) PRIMARY KEY,
    site_name VARCHAR(100),
    region VARCHAR(50),
    market VARCHAR(50)
);

CREATE TABLE vendor_pricing (
    pricing_id SERIAL PRIMARY KEY,
    vendor_id VARCHAR(20) NOT NULL REFERENCES vendors(vendor_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    vendor_price NUMERIC(10,4) NOT NULL,
    price_unit VARCHAR(10) DEFAULT 'CS',
    price_effective_date DATE NOT NULL
);

CREATE TABLE source_vendor_pricing (
    pricing_id SERIAL PRIMARY KEY,
    source_vendor_id VARCHAR(20) NOT NULL REFERENCES source_vendors(source_vendor_id),
    item_no VARCHAR(20) NOT NULL REFERENCES items(item_no),
    source_price NUMERIC(10,4) NOT NULL,
    price_unit VARCHAR(10) DEFAULT 'CS',
    price_effective_date DATE NOT NULL
);

CREATE TABLE vendor_contracts (
    contract_id SERIAL PRIMARY KEY,
    vendor_id VARCHAR(20) NOT NULL REFERENCES vendors(vendor_id),
    source_vendor_id VARCHAR(20) REFERENCES source_vendors(source_vendor_id),
    contract_start DATE NOT NULL,
    contract_end DATE,
    payment_terms VARCHAR(30)
);

CREATE TABLE vendor_shipping_points (
    vendor_id VARCHAR(20) NOT NULL REFERENCES vendors(vendor_id),
    ship_point VARCHAR(20) NOT NULL,
    ship_point_address VARCHAR(200),
    PRIMARY KEY (vendor_id, ship_point)
);

CREATE TABLE site_vendor_assignments (
    site VARCHAR(10) NOT NULL REFERENCES sites(site),
    vendor_id VARCHAR(20) NOT NULL REFERENCES vendors(vendor_id),
    is_primary CHAR(1) DEFAULT 'Y',
    assigned_date DATE,
    PRIMARY KEY (site, vendor_id)
);

CREATE TABLE vendor_performance (
    vendor_id VARCHAR(20) NOT NULL REFERENCES vendors(vendor_id),
    period_month DATE NOT NULL,
    on_time_rate NUMERIC(5,2),
    quality_score NUMERIC(5,2),
    fill_rate NUMERIC(5,2),
    PRIMARY KEY (vendor_id, period_month)
);
"""

# Vendor/source-vendor/item/site codes reused so growth_opportunity_event can FK into these.
VENDORS = [
    ("V00234", "National Dry Goods Corp", "Primary", "Y", "2019-03-01"),
    ("V00345", "Sunrise Dairy Cooperative", "Primary", "Y", "2018-07-15"),
    ("V00567", "Premium Meat Solutions Inc", "Primary", "Y", "2020-01-10"),
    ("V00789", "Global Produce Partners LLC", "Primary", "Y", "2017-11-20"),
    ("V00123", "ABC Food Distributors Inc", "Primary", "Y", "2016-05-05"),
    ("V00999", "Sunrise Bakery Co", "Backup", "Y", "2021-09-01"),
    ("V00888", "Coastal Seafood Traders", "Backup", "N", "2015-02-14"),
    ("V00777", "Heritage Grain Mills", "Primary", "Y", "2022-04-18"),
]

SOURCE_VENDORS = [
    ("SV00567", "Central Supply Network", "Group A", "Midwest"),
    ("SV00890", "Northern Protein Co", "Group B", "Northeast"),
    ("SV00321", "Eastern Fresh Goods Ltd", "Group A", "Northeast"),
    ("SV00456", "Western Food Supply Co", "Group C", "West"),
    ("SV00678", "Pacific Dairy Group", "Group B", "West"),
    ("SV00999", "Southern Harvest Co", "Group C", "South"),
    ("SV00888", "Great Lakes Seafood", "Group A", "Midwest"),
]

ITEMS = [
    ("SUPC-200002", "FRESH ROMAINE LETTUCE 24CT", "Sysco", "24CT", 24),
    ("SUPC-400004", "BEEF GROUND 80/20 10LB CHUB", "Sysco", "10LB", 6),
    ("SUPC-100001", "FROZEN CHICKEN BREAST 4OZ", "Sysco", "4OZ", 40),
    ("SUPC-500005", "SHREDDED MOZZARELLA CHEESE 5LB", "Sysco", "5LB", 4),
    ("SUPC-300003", "CANOLA OIL 35LB JUG", "Sysco", "35LB", 1),
    ("SUPC-600006", "WHOLE WHEAT BREAD LOAF 20OZ", "Sysco", "20OZ", 12),
    ("SUPC-700007", "ATLANTIC SALMON FILLET 6OZ", "Sysco", "6OZ", 10),
]

SITES = [
    ("0091", "Site 0091 - Distribution Center", "Southeast", "Atlanta"),
    ("0055", "Site 0055 - Distribution Center", "Midwest", "Chicago"),
    ("0019", "Site 0019 - Distribution Center", "Northeast", "Boston"),
    ("0078", "Site 0078 - Distribution Center", "West", "Denver"),
    ("0042", "Site 0042 - Distribution Center", "South", "Dallas"),
    ("0063", "Site 0063 - Distribution Center", "West", "Seattle"),
]


def seed_data(cur):
    cur.executemany(
        "INSERT INTO vendors (vendor_id, vendor_name, vendor_type, active_flag, onboarded_date) "
        "VALUES (%s, %s, %s, %s, %s)",
        VENDORS,
    )
    cur.executemany(
        "INSERT INTO source_vendors (source_vendor_id, source_vendor_name, source_vendor_group, region) "
        "VALUES (%s, %s, %s, %s)",
        SOURCE_VENDORS,
    )
    cur.executemany(
        "INSERT INTO items (item_no, item_desc, brand, item_size, pack) VALUES (%s, %s, %s, %s, %s)",
        ITEMS,
    )
    cur.executemany(
        "INSERT INTO sites (site, site_name, region, market) VALUES (%s, %s, %s, %s)",
        SITES,
    )

    vendor_ids = [v[0] for v in VENDORS]
    source_vendor_ids = [sv[0] for sv in SOURCE_VENDORS]
    item_nos = [i[0] for i in ITEMS]
    site_codes = [s[0] for s in SITES]

    vendor_pricing_rows = []
    source_pricing_rows = []
    for idx, item_no in enumerate(item_nos):
        vendor_id = vendor_ids[idx % len(vendor_ids)]
        source_vendor_id = source_vendor_ids[idx % len(source_vendor_ids)]
        vendor_pricing_rows.append((vendor_id, item_no, 12.50 + idx, "CS", "2025-01-01"))
        vendor_pricing_rows.append((vendor_id, item_no, 13.25 + idx, "CS", "2025-06-01"))
        source_pricing_rows.append((source_vendor_id, item_no, 10.75 + idx, "CS", "2025-01-01"))
    cur.executemany(
        "INSERT INTO vendor_pricing (vendor_id, item_no, vendor_price, price_unit, price_effective_date) "
        "VALUES (%s, %s, %s, %s, %s)",
        vendor_pricing_rows,
    )
    cur.executemany(
        "INSERT INTO source_vendor_pricing (source_vendor_id, item_no, source_price, price_unit, price_effective_date) "
        "VALUES (%s, %s, %s, %s, %s)",
        source_pricing_rows,
    )

    contract_rows = [
        (vendor_ids[i], source_vendor_ids[i % len(source_vendor_ids)], "2024-01-01", "2026-12-31", "Net 30")
        for i in range(len(vendor_ids))
    ]
    cur.executemany(
        "INSERT INTO vendor_contracts (vendor_id, source_vendor_id, contract_start, contract_end, payment_terms) "
        "VALUES (%s, %s, %s, %s, %s)",
        contract_rows,
    )

    shipping_rows = [(v, f"SP-{v[-3:]}-01", f"{v} Ship Point, Dock 1") for v in vendor_ids]
    cur.executemany(
        "INSERT INTO vendor_shipping_points (vendor_id, ship_point, ship_point_address) VALUES (%s, %s, %s)",
        shipping_rows,
    )

    assignment_rows = [
        (site_codes[i % len(site_codes)], vendor_ids[i], "Y", "2023-01-01") for i in range(len(vendor_ids))
    ]
    cur.executemany(
        "INSERT INTO site_vendor_assignments (site, vendor_id, is_primary, assigned_date) VALUES (%s, %s, %s, %s)",
        assignment_rows,
    )

    performance_rows = []
    for v in vendor_ids:
        for month in ("2025-04-01", "2025-05-01", "2025-06-01"):
            performance_rows.append((v, month, 96.5, 98.0, 94.2))
    cur.executemany(
        "INSERT INTO vendor_performance (vendor_id, period_month, on_time_rate, quality_score, fill_rate) "
        "VALUES (%s, %s, %s, %s, %s)",
        performance_rows,
    )


def add_fk_to_existing_table(cur):
    """Wire growth_opportunity_event into the new FK graph, skipping any constraint that already
    exists or whose data doesn't line up cleanly (so this stays safe to re-run)."""
    fks = [
        ("fk_goe_true_vendor", "true_vendor", "vendors", "vendor_id"),
        ("fk_goe_source_vendor", "source_vendor", "source_vendors", "source_vendor_id"),
        ("fk_goe_item_no", "item_no", "items", "item_no"),
        ("fk_goe_site", "site", "sites", "site"),
    ]
    for constraint_name, column, target_table, target_column in fks:
        cur.execute(
            """
            SELECT 1 FROM information_schema.table_constraints
            WHERE table_name = 'growth_opportunity_event' AND constraint_name = %s;
            """,
            (constraint_name,),
        )
        if cur.fetchone():
            print(f"[skip] {constraint_name} already exists")
            continue
        try:
            cur.execute(
                f'ALTER TABLE growth_opportunity_event ADD CONSTRAINT {constraint_name} '
                f'FOREIGN KEY ("{column}") REFERENCES {target_table}({target_column});'
            )
            print(f"[added] {constraint_name}: growth_opportunity_event.{column} -> {target_table}.{target_column}")
        except Exception as e:  # noqa: BLE001 - report and continue, don't abort the whole run
            cur.connection.rollback()
            print(f"[warn] could not add {constraint_name}: {e}")


def main():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            print("[schema] dropping old dummy tables (if any)...")
            cur.execute(DROP_SQL)
            print("[schema] creating 10 tables...")
            cur.execute(CREATE_SQL)
            print("[data] seeding dummy rows...")
            seed_data(cur)
            conn.commit()
            print("[fk] wiring growth_opportunity_event into the FK graph...")
            add_fk_to_existing_table(cur)
            conn.commit()
        print("Done. Run `python wiki_agent.py` to regenerate the wiki over the new schema.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
