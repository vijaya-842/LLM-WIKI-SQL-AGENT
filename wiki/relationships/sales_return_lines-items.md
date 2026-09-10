---
title: sales_return_lines → items (item_no)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_return_lines
  - live-database:public.items
source_count: 2
---

# sales_return_lines → items

## Summary
Each items row can have zero or many sales_return_lines rows attached to it; each sales_return_lines row must belong to exactly one items. This relationship ensures that each returned sale must correspond to a valid item in the inventory, as demonstrated by the sample matches where each sales_return_lines entry links to an existing item.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_return_lines]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `sales_return_lines_item_no_fkey` |
| Cardinality (sales_return_lines → items) | many-to-one |
| Cardinality (items → sales_return_lines) | one-to-many |
| Optionality | mandatory — item_no is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_return_lines.item_no` | `items.item_no` |

## Sample Matches
| sales_return_lines.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |

## Tensions Or Gaps
There are no notable modeling risks or gaps in this relationship as defined. The foreign key constraint makes the relationship mandatory, preventing orphaned sales_return_lines rows.

## Related
- [[entities/sales_return_lines]]
- [[entities/items]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/po_receipt_lines-items]]
- [[relationships/purchase_order_lines-items]]
- [[relationships/purchase_requisition_lines-items]]
- [[relationships/sales_invoice_lines-items]]
- [[relationships/sales_order_lines-items]]
- [[relationships/sales_return_lines-sales_returns]]
- [[relationships/shipment_lines-items]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_invoice_lines-items]]
- [[relationships/vendor_pricing-items]]
- [[relationships/overview]]
