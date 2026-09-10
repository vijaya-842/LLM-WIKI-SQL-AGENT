---
title: sales_invoice_lines → sales_invoices (invoice_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_invoice_lines
  - live-database:public.sales_invoices
source_count: 2
---

# sales_invoice_lines → sales_invoices

## Summary
Each sales_invoices row can have zero or many sales_invoice_lines rows attached to it; each sales_invoice_lines row must belong to exactly one sales_invoices. This relationship ensures that every line item on an invoice is tied to a specific invoice, reflecting the necessity of items (like "SUPC-200002" or "SUPC-400004") being accounted for under the correct invoice.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_invoice_lines]] |
| Source column | `invoice_id` |
| Target table | [[entities/sales_invoices]] |
| Target column | `invoice_id` |
| Constraint | `sales_invoice_lines_invoice_id_fkey` |
| Cardinality (sales_invoice_lines → sales_invoices) | many-to-one |
| Cardinality (sales_invoices → sales_invoice_lines) | one-to-many |
| Optionality | mandatory — invoice_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_invoice_lines.invoice_id` | `sales_invoices.invoice_id` |

## Sample Matches
| sales_invoice_lines.invoice_id | sales_invoices.invoice_id | sales_invoices.invoice_id |
|---|---|---|
| 1 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

## Tensions Or Gaps
There are no notable modeling risks or gaps in the current design, as each sales_invoice_lines row's link to sales_invoices is mandatory, preventing any possibility of orphaned rows.

## Related
- [[entities/sales_invoice_lines]]
- [[entities/sales_invoices]]
- [[relationships/payment_transactions-sales_invoices]]
- [[relationships/sales_invoice_lines-items]]
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_returns-sales_invoices]]
- [[relationships/overview]]
