---
title: purchase_requisition_lines → purchase_requisitions (requisition_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_requisition_lines
  - live-database:public.purchase_requisitions
source_count: 2
---

# purchase_requisition_lines → purchase_requisitions

## Summary
Each purchase_requisitions row can have zero or many purchase_requisition_lines rows attached to it; each purchase_requisition_lines row must belong to exactly one purchase_requisitions. This is evidenced by the sample matches, where each line item (like SUPC-200002) corresponds to a unique requisition with a status of "Approved."

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/purchase_requisition_lines]] |
| Source column | `requisition_id` |
| Target table | [[entities/purchase_requisitions]] |
| Target column | `requisition_id` |
| Constraint | `purchase_requisition_lines_requisition_id_fkey` |
| Cardinality (purchase_requisition_lines → purchase_requisitions) | many-to-one |
| Cardinality (purchase_requisitions → purchase_requisition_lines) | one-to-many |
| Optionality | mandatory — requisition_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `purchase_requisition_lines.requisition_id` | `purchase_requisitions.requisition_id` |

## Sample Matches
| purchase_requisition_lines.requisition_id | purchase_requisitions.requisition_id | purchase_requisitions.requisition_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

## Tensions Or Gaps
There are no notable modeling risks identified in this foreign-key relationship, as the cardinality and optionality constraints appear to be appropriately enforced. Each purchase_requisition_lines row is mandated to link to a purchase_requisitions row, preventing any potential orphaned records.

## Related
- [[entities/purchase_requisition_lines]]
- [[entities/purchase_requisitions]]
- [[relationships/purchase_orders-purchase_requisitions]]
- [[relationships/purchase_requisition_lines-items]]
- [[relationships/purchase_requisitions-sites]]
- [[relationships/overview]]
