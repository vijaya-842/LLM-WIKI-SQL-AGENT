---
title: sales_orders → sales_reps (rep_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_orders
  - live-database:public.sales_reps
source_count: 2
---

# sales_orders → sales_reps

## Summary
Each sales_reps row can have zero or many sales_orders rows attached to it; each sales_orders row's link to sales_reps is optional, meaning a sales_orders row may not contain a corresponding sales_reps row. This relationship allows for the representation of orders without an associated sales representative, reflecting scenarios where orders may be processed without direct sales rep involvement.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_orders]] |
| Source column | `rep_id` |
| Target table | [[entities/sales_reps]] |
| Target column | `rep_id` |
| Constraint | `sales_orders_rep_id_fkey` |
| Cardinality (sales_orders → sales_reps) | many-to-one |
| Cardinality (sales_reps → sales_orders) | one-to-many |
| Optionality | optional — rep_id is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_orders.rep_id` | `sales_reps.rep_id` |

## Sample Matches
| sales_orders.rep_id | sales_reps.rep_id | sales_reps.rep_name |
|---|---|---|
| R001 | R001 | Alicia Moreno |
| R002 | R002 | David Chen |
| R003 | R003 | Priya Nair |
| R004 | R004 | Marcus Webb |
| R005 | R005 | Sofia Reyes |

## Tensions Or Gaps
The optional foreign key relationship suggests that some sales_orders rows may be orphaned without a corresponding sales_reps entry by design, which could lead to incomplete data in business analysis.

## Related
- [[entities/sales_orders]]
- [[entities/sales_reps]]
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_order_lines-sales_orders]]
- [[relationships/sales_orders-sites]]
- [[relationships/sales_orders-customers]]
- [[relationships/shipments-sales_orders]]
- [[relationships/overview]]
