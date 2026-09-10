---
title: sales_invoices → sales_orders (order_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_invoices
  - live-database:public.sales_orders
source_count: 2
---

# sales_invoices → sales_orders

## Summary
Each sales_orders row can have zero or many sales_invoices rows attached to it; each sales_invoices row must belong to exactly one sales_orders. This relationship ensures that every invoice, such as those for orders 1 through 5, is linked to a specific order, thereby maintaining the integrity of billing and order management.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_invoices]] |
| Source column | `order_id` |
| Target table | [[entities/sales_orders]] |
| Target column | `order_id` |
| Constraint | `sales_invoices_order_id_fkey` |
| Cardinality (sales_invoices → sales_orders) | many-to-one |
| Cardinality (sales_orders → sales_invoices) | one-to-many |
| Optionality | mandatory — order_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_invoices.order_id` | `sales_orders.order_id` |

## Sample Matches
| sales_invoices.order_id | sales_orders.order_id | sales_orders.order_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

## Tensions Or Gaps
There are no notable modeling risks or gaps in this relationship; the foreign key constraint correctly enforces the mandatory link between sales_invoices and sales_orders.

## Related
- [[entities/sales_invoices]]
- [[entities/sales_orders]]
- [[relationships/payment_transactions-sales_invoices]]
- [[relationships/sales_invoice_lines-sales_invoices]]
- [[relationships/sales_order_lines-sales_orders]]
- [[relationships/sales_orders-sales_reps]]
- [[relationships/sales_orders-sites]]
- [[relationships/sales_orders-customers]]
- [[relationships/sales_returns-sales_invoices]]
- [[relationships/shipments-sales_orders]]
- [[relationships/overview]]
