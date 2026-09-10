---
title: sales_returns → sales_invoices (invoice_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_returns
  - live-database:public.sales_invoices
source_count: 2
---

# sales_returns → sales_invoices

## Summary
Each sales_invoices row can have zero or many sales_returns rows attached to it; each sales_returns row must belong to exactly one sales_invoices. This relationship captures instances where products sold through invoices are returned, as demonstrated by the matched rows indicating various return reasons linked to their respective invoices.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_returns]] |
| Source column | `invoice_id` |
| Target table | [[entities/sales_invoices]] |
| Target column | `invoice_id` |
| Constraint | `sales_returns_invoice_id_fkey` |
| Cardinality (sales_returns → sales_invoices) | many-to-one |
| Cardinality (sales_invoices → sales_returns) | one-to-many |
| Optionality | mandatory — invoice_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_returns.invoice_id` | `sales_invoices.invoice_id` |

## Sample Matches
| sales_returns.invoice_id | sales_invoices.invoice_id | sales_invoices.invoice_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

## Tensions Or Gaps
There are no notable modeling risks present in this relationship; the foreign key constraint ensures that every sales_returns record is mandatory linked to a sales_invoices record, which maintains data integrity.

## Related
- [[entities/sales_returns]]
- [[entities/sales_invoices]]
- [[relationships/payment_transactions-sales_invoices]]
- [[relationships/sales_invoice_lines-sales_invoices]]
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_return_lines-sales_returns]]
- [[relationships/overview]]
