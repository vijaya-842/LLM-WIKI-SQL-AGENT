---
title: shipments → sales_orders (order_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.shipments
  - live-database:public.sales_orders
source_count: 2
---

# shipments → sales_orders

## Summary
Each shipments row must belong to exactly one sales_orders row, establishing a mandatory link between the two tables. This relationship reflects that every shipment is tied to a specific sales order, as evidenced by the sample matches where each shipment's order_id corresponds to a valid order in the sales_orders table.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/shipments]] |
| Source column | `order_id` |
| Target table | [[entities/sales_orders]] |
| Target column | `order_id` |
| Constraint | `shipments_order_id_fkey` |
| Cardinality (shipments → sales_orders) | many-to-one |
| Cardinality (sales_orders → shipments) | one-to-many |
| Optionality | mandatory — order_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `shipments.order_id` | `sales_orders.order_id` |

## Sample Matches
| shipments.order_id | sales_orders.order_id | sales_orders.order_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

## Tensions Or Gaps
There are no notable modeling risks present in this relationship, as all shipments rows are required to have a corresponding sales_orders row, ensuring that no shipments are orphaned.

## Related
- [[entities/shipments]]
- [[entities/sales_orders]]
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_order_lines-sales_orders]]
- [[relationships/sales_orders-sales_reps]]
- [[relationships/sales_orders-sites]]
- [[relationships/sales_orders-customers]]
- [[relationships/shipment_lines-shipments]]
- [[relationships/shipments-sites]]
- [[relationships/overview]]
