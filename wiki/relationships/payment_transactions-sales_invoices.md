---
title: payment_transactions → sales_invoices (sales_invoice_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.payment_transactions
  - live-database:public.sales_invoices
source_count: 2
---

# payment_transactions → sales_invoices

## Summary
Each sales_invoices row can have zero or many payment_transactions rows attached to it; each payment_transactions row must belong to exactly one sales_invoices. This relationship indicates that multiple payments can be made for a single invoice, while a payment can only correspond to a specific invoice, as seen in the sample matches where various payments relate back to their respective invoices.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/payment_transactions]] |
| Source column | `sales_invoice_id` |
| Target table | [[entities/sales_invoices]] |
| Target column | `invoice_id` |
| Constraint | `payment_transactions_sales_invoice_id_fkey` |
| Cardinality (payment_transactions → sales_invoices) | many-to-one |
| Cardinality (sales_invoices → payment_transactions) | one-to-many |
| Optionality | optional — sales_invoice_id is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `payment_transactions.sales_invoice_id` | `sales_invoices.invoice_id` |

## Sample Matches
| payment_transactions.sales_invoice_id | sales_invoices.invoice_id | sales_invoices.invoice_id |
|---|---|---|
| 1 | 1 | 1 |
| 3 | 3 | 3 |
| 5 | 5 | 5 |
| 7 | 7 | 7 |

## Tensions Or Gaps
The optional foreign key in payment_transactions implies that some payment_transactions rows may not have a corresponding sales_invoices entry, which could create orphaned records by design. This optionality should be carefully managed to ensure data integrity.

## Related
- [[entities/payment_transactions]]
- [[entities/sales_invoices]]
- [[relationships/payment_transactions-vendor_invoices]]
- [[relationships/sales_invoice_lines-sales_invoices]]
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_returns-sales_invoices]]
- [[relationships/overview]]
