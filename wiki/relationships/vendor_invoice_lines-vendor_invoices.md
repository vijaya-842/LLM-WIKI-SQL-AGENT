---
title: vendor_invoice_lines → vendor_invoices (invoice_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.vendor_invoice_lines
  - live-database:public.vendor_invoices
source_count: 2
---

# vendor_invoice_lines → vendor_invoices

## Summary
Each `vendor_invoices` row can have zero or many `vendor_invoice_lines` rows attached to it; each `vendor_invoice_lines` row must belong to exactly one `vendor_invoices`. This relationship reflects how individual invoice lines correspond to their respective invoices, as seen in the sample matches where multiple lines exist for a single invoice.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_invoice_lines]] |
| Source column | `invoice_id` |
| Target table | [[entities/vendor_invoices]] |
| Target column | `invoice_id` |
| Constraint | `vendor_invoice_lines_invoice_id_fkey` |
| Cardinality (vendor_invoice_lines → vendor_invoices) | many-to-one |
| Cardinality (vendor_invoices → vendor_invoice_lines) | one-to-many |
| Optionality | mandatory — invoice_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_invoice_lines.invoice_id` | `vendor_invoices.invoice_id` |

## Sample Matches
| vendor_invoice_lines.invoice_id | vendor_invoices.invoice_id | vendor_invoices.invoice_id |
|---|---|---|
| 1 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

## Tensions Or Gaps
There are no notable modeling risks; the relationship is clearly defined as many-to-one from `vendor_invoice_lines` to `vendor_invoices` with mandatory links, ensuring no orphaned rows in `vendor_invoice_lines`.

## Related
- [[entities/vendor_invoice_lines]]
- [[entities/vendor_invoices]]
- [[relationships/payment_transactions-vendor_invoices]]
- [[relationships/vendor_invoice_lines-items]]
- [[relationships/vendor_invoices-purchase_orders]]
- [[relationships/vendor_invoices-vendors]]
- [[relationships/overview]]
