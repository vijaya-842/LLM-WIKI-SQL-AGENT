---
title: purchase_requisition_lines → items (item_no)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_requisition_lines
  - live-database:public.items
source_count: 2
---

# purchase_requisition_lines → items

## Summary
Each items row can have zero or many purchase_requisition_lines rows attached to it; each purchase_requisition_lines row must belong to exactly one items. This reflects the relationship where each purchase requisition line is associated with a specific item, such as "FRESH ROMAINE LETTUCE 24CT" or "CANOLA OIL 35LB JUG," ensuring that every requisition line is tied to a valid item.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/purchase_requisition_lines]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `purchase_requisition_lines_item_no_fkey` |
| Cardinality (purchase_requisition_lines → items) | many-to-one |
| Cardinality (items → purchase_requisition_lines) | one-to-many |
| Optionality | mandatory — item_no is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `purchase_requisition_lines.item_no` | `items.item_no` |

## Sample Matches
| purchase_requisition_lines.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |
| SUPC-500005 | SUPC-500005 | SHREDDED MOZZARELLA CHEESE 5LB |
| SUPC-300003 | SUPC-300003 | CANOLA OIL 35LB JUG |

## Tensions Or Gaps
There are no notable modeling risks present, as the foreign key relationship is mandatory, ensuring all purchase_requisition_lines entries are associated with existing items.

## Related
- [[entities/purchase_requisition_lines]]
- [[entities/items]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/po_receipt_lines-items]]
- [[relationships/purchase_order_lines-items]]
- [[relationships/purchase_requisition_lines-purchase_requisitions]]
- [[relationships/sales_invoice_lines-items]]
- [[relationships/sales_order_lines-items]]
- [[relationships/sales_return_lines-items]]
- [[relationships/shipment_lines-items]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_invoice_lines-items]]
- [[relationships/vendor_pricing-items]]
- [[relationships/overview]]
