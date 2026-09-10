---
title: sales_order_lines → sales_orders (order_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_order_lines
  - live-database:public.sales_orders
source_count: 2
---

# sales_order_lines → sales_orders

## Summary
Each `sales_orders` row can have zero or many `sales_order_lines` rows attached to it; each `sales_order_lines` row must belong to exactly one `sales_orders`. This relationship is evident in the sample matches, where multiple order lines with distinct item details are associated with a single sales order.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_order_lines]] |
| Source column | `order_id` |
| Target table | [[entities/sales_orders]] |
| Target column | `order_id` |
| Constraint | `sales_order_lines_order_id_fkey` |
| Cardinality (sales_order_lines → sales_orders) | many-to-one |
| Cardinality (sales_orders → sales_order_lines) | one-to-many |
| Optionality | mandatory — order_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_order_lines.order_id` | `sales_orders.order_id` |

## Sample Matches
| sales_order_lines.order_id | sales_orders.order_id | sales_orders.order_id |
|---|---|---|
| 1 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

## Tensions Or Gaps
There are no notable modeling risks identified in this relationship, as each `sales_order_lines` row is mandated to have a corresponding `sales_orders` row, ensuring referential integrity.

## Related
- [[entities/sales_order_lines]]
- [[entities/sales_orders]]
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_order_lines-items]]
- [[relationships/sales_orders-sales_reps]]
- [[relationships/sales_orders-sites]]
- [[relationships/sales_orders-customers]]
- [[relationships/shipments-sales_orders]]
- [[relationships/overview]]
