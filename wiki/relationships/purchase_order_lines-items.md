---
title: purchase_order_lines → items (item_no)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_order_lines
  - live-database:public.items
source_count: 2
---

# purchase_order_lines → items

## Summary
Each items row can have zero or many purchase_order_lines rows attached to it; each purchase_order_lines row must belong to exactly one items. This relationship ensures that every line in a purchase order is linked to a specific item, which is reflected in the sample matches where multiple purchase order lines have the same item number connecting them to their respective items.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/purchase_order_lines]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `purchase_order_lines_item_no_fkey` |
| Cardinality (purchase_order_lines → items) | many-to-one |
| Cardinality (items → purchase_order_lines) | one-to-many |
| Optionality | mandatory — item_no is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `purchase_order_lines.item_no` | `items.item_no` |

## Sample Matches
| purchase_order_lines.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |

## Tensions Or Gaps
There are no notable modeling risks in this foreign key relationship; the defined constraints and cardinality align well with the intended business logic.

## Related
- [[entities/purchase_order_lines]]
- [[entities/items]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/po_receipt_lines-items]]
- [[relationships/purchase_order_lines-purchase_orders]]
- [[relationships/purchase_requisition_lines-items]]
- [[relationships/sales_invoice_lines-items]]
- [[relationships/sales_order_lines-items]]
- [[relationships/sales_return_lines-items]]
- [[relationships/shipment_lines-items]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_invoice_lines-items]]
- [[relationships/vendor_pricing-items]]
- [[relationships/overview]]
