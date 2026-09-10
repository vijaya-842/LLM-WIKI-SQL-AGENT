---
title: payment_transactions → vendor_invoices (vendor_invoice_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.payment_transactions
  - live-database:public.vendor_invoices
source_count: 2
---

# payment_transactions → vendor_invoices

## Summary
Each vendor_invoices row can have zero or many payment_transactions rows attached to it; each payment_transactions row's link to vendor_invoices is optional, meaning it can exist without a corresponding invoice. The sample data shows that multiple payment transactions can be linked to different vendor invoices, reflecting the real-world scenario where a vendor may receive several payments corresponding to their invoices.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/payment_transactions]] |
| Source column | `vendor_invoice_id` |
| Target table | [[entities/vendor_invoices]] |
| Target column | `invoice_id` |
| Constraint | `payment_transactions_vendor_invoice_id_fkey` |
| Cardinality (payment_transactions → vendor_invoices) | many-to-one |
| Cardinality (vendor_invoices → payment_transactions) | one-to-many |
| Optionality | optional — vendor_invoice_id is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `payment_transactions.vendor_invoice_id` | `vendor_invoices.invoice_id` |

## Sample Matches
| payment_transactions.vendor_invoice_id | vendor_invoices.invoice_id | vendor_invoices.invoice_id |
|---|---|---|
| 1 | 1 | 1 |
| 3 | 3 | 3 |
| 5 | 5 | 5 |
| 7 | 7 | 7 |

## Tensions Or Gaps
The optional foreign key in payment_transactions means that there may be some rows without an associated vendor invoice, which could lead to orphaned records by design. This could create challenges in ensuring data integrity and accurate reporting.

## Related
- [[entities/payment_transactions]]
- [[entities/vendor_invoices]]
- [[relationships/payment_transactions-sales_invoices]]
- [[relationships/vendor_invoice_lines-vendor_invoices]]
- [[relationships/vendor_invoices-purchase_orders]]
- [[relationships/vendor_invoices-vendors]]
- [[relationships/overview]]
