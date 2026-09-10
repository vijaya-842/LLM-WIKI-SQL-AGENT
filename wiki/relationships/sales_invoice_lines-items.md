---
title: sales_invoice_lines → items (item_no)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_invoice_lines
  - live-database:public.items
source_count: 2
---

# sales_invoice_lines → items

## Summary
Each items row can have zero or many sales_invoice_lines rows attached to it; each sales_invoice_lines row must belong to exactly one items. This relationship is represented by the foreign key `sales_invoice_lines.item_no` linking to `items.item_no`, ensuring that every sales invoice line corresponds to a valid item in the inventory. The sample matches illustrate various invoice lines associated with specific items, demonstrating this mandatory connection.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_invoice_lines]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `sales_invoice_lines_item_no_fkey` |
| Cardinality (sales_invoice_lines → items) | many-to-one |
| Cardinality (items → sales_invoice_lines) | one-to-many |
| Optionality | mandatory — item_no is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_invoice_lines.item_no` | `items.item_no` |

## Sample Matches
| sales_invoice_lines.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |

## Tensions Or Gaps
There are no notable modeling risks within this foreign key relationship, as each sales_invoice_lines row is required to link to an items row, ensuring that no sales invoice lines are orphaned. The current model appears sound, reflecting the necessary business logic.

## Related
- [[entities/sales_invoice_lines]]
- [[entities/items]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/po_receipt_lines-items]]
- [[relationships/purchase_order_lines-items]]
- [[relationships/purchase_requisition_lines-items]]
- [[relationships/sales_invoice_lines-sales_invoices]]
- [[relationships/sales_order_lines-items]]
- [[relationships/sales_return_lines-items]]
- [[relationships/shipment_lines-items]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_invoice_lines-items]]
- [[relationships/vendor_pricing-items]]
- [[relationships/overview]]
