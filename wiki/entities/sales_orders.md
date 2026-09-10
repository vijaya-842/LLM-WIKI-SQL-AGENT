---
title: Sales Orders
type: entity
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_orders
source_count: 1
---

# sales_orders

## Overview
The `sales_orders` table is designed to track individual sales orders made by customers. It contains essential information such as the unique order ID, customer identification, the site where the order originated, the representative associated with the order, the order date, and its current status. This structure enables businesses to efficiently manage and analyze their sales transactions.

## Entity Relationship Diagram
```mermaid
erDiagram
    customers {
        character_varying customer_id PK
        character_varying customer_name
        character_varying customer_type
        character_varying region
        character_varying site
        character active_flag
        timestamp_without_time_zone created_timestamp
    }
    sales_invoices {
        integer invoice_id PK
        integer order_id
        date invoice_date
        numeric total_amount
        character_varying status
    }
    sales_order_lines {
        integer line_id PK
        integer order_id
        character_varying item_no
        integer qty_ordered
        numeric unit_price
    }
    sales_orders {
        integer order_id PK
        character_varying customer_id
        character_varying site
        character_varying rep_id
        date order_date
        character_varying status
    }
    sales_reps {
        character_varying rep_id PK
        character_varying rep_name
        character_varying region
        date hire_date
    }
    shipments {
        integer shipment_id PK
        integer order_id
        character_varying site
        date ship_date
        character_varying carrier
    }
    sites {
        character_varying site PK
        character_varying site_name
        character_varying region
        character_varying market
    }
    sales_orders }o--|| customers : "customer_id -> customer_id"
    sales_orders }o--|| sites : "site -> site"
    sales_orders }o--|| sales_reps : "rep_id -> rep_id"
    sales_invoices }o--|| sales_orders : "order_id -> order_id"
    sales_order_lines }o--|| sales_orders : "order_id -> order_id"
    shipments }o--|| sales_orders : "order_id -> order_id"
```

## Column Reference Table
| Column | Type | Nullable | Default | Description |
|---|---|---|---|---|
| order_id | integer | No | nextval('sales_orders_order_id_seq'::regclass) | Unique identifier for each sales order. |
| customer_id | character varying(20) | No |  | Identifier for the customer placing the order. |
| site | character varying(10) | No |  | Location code where the order is processed. |
| rep_id | character varying(20) | Yes |  | Identifier for the sales representative handling the order. |
| order_date | date | No |  | Date when the order was placed. |
| status | character varying(20) | Yes | 'Open'::character varying | Current state of the order, e.g., Open or Closed. |

## Business Rules
The `sales_orders` table enforces several business rules through check constraints:
- `sales_orders_order_id_not_null`: Ensures that every order has a non-null `order_id`.
- `sales_orders_customer_id_not_null`: Ensures that every order is associated with a valid `customer_id`.
- `sales_orders_site_not_null`: Ensures that each order references a valid `site`.
- `sales_orders_order_date_not_null`: Ensures that the order date is provided for each order.

## Common Query Examples
Retrieve all orders along with their status:
```sql
SELECT * FROM sales_orders;
```

Find all open orders placed by a specific customer:
```sql
SELECT * FROM sales_orders WHERE customer_id = 'C00101' AND status = 'Open';
```

Count the total number of orders for each site:
```sql
SELECT site, COUNT(*) as total_orders FROM sales_orders GROUP BY site;
```

Get the orders placed by a specific sales representative within a date range:
```sql
SELECT * FROM sales_orders WHERE rep_id = 'R002' AND order_date BETWEEN '2025-01-01' AND '2025-03-31';
```

## Index Documentation
The `sales_orders` table has the following index:
- **Index Name**: `sales_orders_pkey`
  - **Column Name**: `order_id`
  - **Unique**: Yes
  - **Primary**: Yes

There are no additional indexes specified. However, indexes on the `customer_id`, `site`, and `rep_id` columns could enhance query performance, especially for filtering and joining operations in common queries analyzed earlier.

## Migration History
This database has no migration-tracking table (checked for alembic, flyway, django, knex, and sequelize conventions). Schema changes here are not currently tracked.

## Related
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_order_lines-sales_orders]]
- [[relationships/sales_orders-sales_reps]]
- [[relationships/sales_orders-sites]]
- [[relationships/sales_orders-customers]]
- [[relationships/shipments-sales_orders]]
- [[relationships/overview]]
- [[domains/order-management]]
- [[enums/site]]
- [[enums/status]]
- [[queries/recent-sales-orders]] — Recent sales orders and their total amounts
- [[queries/sales-reps-orders]] — Sales representatives and their associated sales orders
- [[queries/sales-orders-shipments]] — Sales orders with shipment details
- [[queries/customer-credit-terms-sales-orders]] — Customer credit terms to sales orders
- [[queries/customer-sales-orders]] — Customer Sales Order Details
- [[erd]]
- [[overview]]
- [[index]]
