---
title: po_receipts → purchase_orders (po_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.po_receipts
  - live-database:public.purchase_orders
source_count: 2
---

# po_receipts → purchase_orders

## Summary
Each purchase_orders row can have zero or many po_receipts rows attached to it; each po_receipts row must belong to exactly one purchase_orders. This relationship ensures that every receipt is linked to a specific purchase order, as demonstrated in the sample matches, where multiple receipts correspond to various purchase orders.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/po_receipts]] |
| Source column | `po_id` |
| Target table | [[entities/purchase_orders]] |
| Target column | `po_id` |
| Constraint | `po_receipts_po_id_fkey` |
| Cardinality (po_receipts → purchase_orders) | many-to-one |
| Cardinality (purchase_orders → po_receipts) | one-to-many |
| Optionality | mandatory — po_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `po_receipts.po_id` | `purchase_orders.po_id` |

## Sample Matches
| po_receipts.po_id | purchase_orders.po_id | purchase_orders.po_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

## Tensions Or Gaps
There are no notable modeling risks identified in this foreign key relationship. The mandatory link between po_receipts and purchase_orders ensures that every receipt is appropriately associated with a purchase order, minimizing the risk of orphaned records.

## Related
- [[entities/po_receipts]]
- [[entities/purchase_orders]]
- [[relationships/po_receipt_lines-po_receipts]]
- [[relationships/purchase_order_lines-purchase_orders]]
- [[relationships/purchase_orders-vendors]]
- [[relationships/purchase_orders-purchase_requisitions]]
- [[relationships/purchase_orders-sites]]
- [[relationships/vendor_invoices-purchase_orders]]
- [[relationships/overview]]
