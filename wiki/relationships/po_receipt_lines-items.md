---
title: po_receipt_lines → items (item_no)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.po_receipt_lines
  - live-database:public.items
source_count: 2
---

# po_receipt_lines → items

## Summary
Each items row can have zero or many po_receipt_lines rows attached to it; each po_receipt_lines row must belong to exactly one items. This relationship reflects the fact that each receipt line is tied to a specific item, as seen in the sample matches where each item number in po_receipt_lines corresponds to an item in the items table.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/po_receipt_lines]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `po_receipt_lines_item_no_fkey` |
| Cardinality (po_receipt_lines → items) | many-to-one |
| Cardinality (items → po_receipt_lines) | one-to-many |
| Optionality | mandatory — item_no is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `po_receipt_lines.item_no` | `items.item_no` |

## Sample Matches
| po_receipt_lines.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |
| SUPC-500005 | SUPC-500005 | SHREDDED MOZZARELLA CHEESE 5LB |
| SUPC-300003 | SUPC-300003 | CANOLA OIL 35LB JUG |

## Tensions Or Gaps
There are no notable modeling risks or gaps in this relationship, as the foreign key constraint ensures that every po_receipt_lines row must link to an existing item in the items table.

## Related
- [[entities/po_receipt_lines]]
- [[entities/items]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/po_receipt_lines-po_receipts]]
- [[relationships/purchase_order_lines-items]]
- [[relationships/purchase_requisition_lines-items]]
- [[relationships/sales_invoice_lines-items]]
- [[relationships/sales_order_lines-items]]
- [[relationships/sales_return_lines-items]]
- [[relationships/shipment_lines-items]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_invoice_lines-items]]
- [[relationships/vendor_pricing-items]]
- [[relationships/overview]]
