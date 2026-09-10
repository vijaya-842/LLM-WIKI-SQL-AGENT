---
title: vendor_invoice_lines → items (item_no)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.vendor_invoice_lines
  - live-database:public.items
source_count: 2
---

# vendor_invoice_lines → items

## Summary
Each items row can have zero or many vendor_invoice_lines rows attached to it; each vendor_invoice_lines row must belong to exactly one items. This relationship ensures that every invoice line in the vendor_invoice_lines table is associated with a specific item in the items table, as demonstrated by the sample matches where item numbers in vendor_invoice_lines correspond directly to those in items.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_invoice_lines]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `vendor_invoice_lines_item_no_fkey` |
| Cardinality (vendor_invoice_lines → items) | many-to-one |
| Cardinality (items → vendor_invoice_lines) | one-to-many |
| Optionality | mandatory — item_no is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_invoice_lines.item_no` | `items.item_no` |

## Sample Matches
| vendor_invoice_lines.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |

## Tensions Or Gaps
There do not appear to be any notable modeling risks in this relationship, as the foreign key constraint enforces that every vendor_invoice_lines entry is linked to a valid item, ensuring data integrity.

## Related
- [[entities/vendor_invoice_lines]]
- [[entities/items]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/po_receipt_lines-items]]
- [[relationships/purchase_order_lines-items]]
- [[relationships/purchase_requisition_lines-items]]
- [[relationships/sales_invoice_lines-items]]
- [[relationships/sales_order_lines-items]]
- [[relationships/sales_return_lines-items]]
- [[relationships/shipment_lines-items]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_invoice_lines-vendor_invoices]]
- [[relationships/vendor_pricing-items]]
- [[relationships/overview]]
