---
title: purchase_order_lines → purchase_orders (po_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_order_lines
  - live-database:public.purchase_orders
source_count: 2
---

# purchase_order_lines → purchase_orders

## Summary
Each `purchase_orders` row can have zero or many `purchase_order_lines` rows attached to it; each `purchase_order_lines` row must belong to exactly one `purchase_orders`. This relationship ensures that each line item in a purchase order is clearly linked to its respective order, as demonstrated in the sample matches where line items are consistently associated with their corresponding purchase orders.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/purchase_order_lines]] |
| Source column | `po_id` |
| Target table | [[entities/purchase_orders]] |
| Target column | `po_id` |
| Constraint | `purchase_order_lines_po_id_fkey` |
| Cardinality (purchase_order_lines → purchase_orders) | many-to-one |
| Cardinality (purchase_orders → purchase_order_lines) | one-to-many |
| Optionality | mandatory — po_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `purchase_order_lines.po_id` | `purchase_orders.po_id` |

## Sample Matches
| purchase_order_lines.po_id | purchase_orders.po_id | purchase_orders.po_id |
|---|---|---|
| 1 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

## Tensions Or Gaps
There appear to be no notable modeling risks in this foreign key relationship, as the constraints ensure that every `purchase_order_lines` row is required to relate to a `purchase_orders` row.

## Related
- [[entities/purchase_order_lines]]
- [[entities/purchase_orders]]
- [[relationships/po_receipts-purchase_orders]]
- [[relationships/purchase_order_lines-items]]
- [[relationships/purchase_orders-vendors]]
- [[relationships/purchase_orders-purchase_requisitions]]
- [[relationships/purchase_orders-sites]]
- [[relationships/vendor_invoices-purchase_orders]]
- [[relationships/overview]]
