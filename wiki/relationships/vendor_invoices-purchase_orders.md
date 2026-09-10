---
title: vendor_invoices → purchase_orders (po_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.vendor_invoices
  - live-database:public.purchase_orders
source_count: 2
---

# vendor_invoices → purchase_orders

## Summary
Each purchase_orders row can have zero or many vendor_invoices rows attached to it; each vendor_invoices row must belong to exactly one purchase_orders. This relationship ensures that every vendor invoice is linked to a specific purchase order, as seen in the sample matched rows where invoices are tied to their respective purchase orders.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_invoices]] |
| Source column | `po_id` |
| Target table | [[entities/purchase_orders]] |
| Target column | `po_id` |
| Constraint | `vendor_invoices_po_id_fkey` |
| Cardinality (vendor_invoices → purchase_orders) | many-to-one |
| Cardinality (purchase_orders → vendor_invoices) | one-to-many |
| Optionality | mandatory — po_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_invoices.po_id` | `purchase_orders.po_id` |

## Sample Matches
| vendor_invoices.po_id | purchase_orders.po_id | purchase_orders.po_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

## Tensions Or Gaps
There are no notable tensions or gaps in this relationship, as the modeling accurately reflects the mandatory association of vendor_invoices to purchase_orders without any nullable foreign keys or potential orphaned records.

## Related
- [[entities/vendor_invoices]]
- [[entities/purchase_orders]]
- [[relationships/payment_transactions-vendor_invoices]]
- [[relationships/po_receipts-purchase_orders]]
- [[relationships/purchase_order_lines-purchase_orders]]
- [[relationships/purchase_orders-vendors]]
- [[relationships/purchase_orders-purchase_requisitions]]
- [[relationships/purchase_orders-sites]]
- [[relationships/vendor_invoice_lines-vendor_invoices]]
- [[relationships/vendor_invoices-vendors]]
- [[relationships/overview]]
