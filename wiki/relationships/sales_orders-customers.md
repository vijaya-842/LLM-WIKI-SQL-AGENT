---
title: sales_orders → customers (customer_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_orders
  - live-database:public.customers
source_count: 2
---

# sales_orders → customers

## Summary
Each customers row can have zero or many sales_orders rows attached to it; each sales_orders row must belong to exactly one customers. This relationship is crucial for tracking which customer placed each order, as demonstrated by the sample matches where each order in the sales_orders table is associated with a specific customer in the customers table.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_orders]] |
| Source column | `customer_id` |
| Target table | [[entities/customers]] |
| Target column | `customer_id` |
| Constraint | `sales_orders_customer_id_fkey` |
| Cardinality (sales_orders → customers) | many-to-one |
| Cardinality (customers → sales_orders) | one-to-many |
| Optionality | mandatory — customer_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_orders.customer_id` | `customers.customer_id` |

## Sample Matches
| sales_orders.customer_id | customers.customer_id | customers.customer_name |
|---|---|---|
| C00101 | C00101 | Riverside Diner Group |
| C00102 | C00102 | Metro School District |
| C00103 | C00103 | Harborview Hotel Chain |
| C00104 | C00104 | Summit Health System |
| C00105 | C00105 | Lonestar Cafe Group |

## Tensions Or Gaps
There are no notable tensions or gaps in this relationship as the foreign key constraint ensures that every sales_orders row is properly linked to an existing customers row, maintaining data integrity.

## Related
- [[entities/sales_orders]]
- [[entities/customers]]
- [[relationships/customer_credit_terms-customers]]
- [[relationships/customers-sites]]
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_order_lines-sales_orders]]
- [[relationships/sales_orders-sales_reps]]
- [[relationships/sales_orders-sites]]
- [[relationships/shipments-sales_orders]]
- [[relationships/overview]]
