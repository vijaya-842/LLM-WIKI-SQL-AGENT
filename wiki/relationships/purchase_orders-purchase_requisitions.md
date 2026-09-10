---
title: purchase_orders → purchase_requisitions (requisition_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_orders
  - live-database:public.purchase_requisitions
source_count: 2
---

# purchase_orders → purchase_requisitions

## Summary
Each purchase_requisitions row can have zero or many purchase_orders rows attached to it; each purchase_orders row may belong to zero or one purchase_requisitions. This relationship is reflected in the sample matches, where several purchase_orders are linked to their corresponding purchase_requisitions, indicating that not every purchase_order requires a purchase_requisition.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/purchase_orders]] |
| Source column | `requisition_id` |
| Target table | [[entities/purchase_requisitions]] |
| Target column | `requisition_id` |
| Constraint | `purchase_orders_requisition_id_fkey` |
| Cardinality (purchase_orders → purchase_requisitions) | many-to-one |
| Cardinality (purchase_requisitions → purchase_orders) | one-to-many |
| Optionality | optional — requisition_id is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `purchase_orders.requisition_id` | `purchase_requisitions.requisition_id` |

## Sample Matches
| purchase_orders.requisition_id | purchase_requisitions.requisition_id | purchase_requisitions.requisition_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

## Tensions Or Gaps
The optional foreign key suggests that some purchase_orders rows may be orphaned by design, which could lead to inconsistent data if untracked orders exist without corresponding requisitions.

## Related
- [[entities/purchase_orders]]
- [[entities/purchase_requisitions]]
- [[relationships/po_receipts-purchase_orders]]
- [[relationships/purchase_order_lines-purchase_orders]]
- [[relationships/purchase_orders-vendors]]
- [[relationships/purchase_orders-sites]]
- [[relationships/purchase_requisition_lines-purchase_requisitions]]
- [[relationships/purchase_requisitions-sites]]
- [[relationships/vendor_invoices-purchase_orders]]
- [[relationships/overview]]
