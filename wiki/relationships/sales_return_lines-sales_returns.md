---
title: sales_return_lines → sales_returns (return_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_return_lines
  - live-database:public.sales_returns
source_count: 2
---

# sales_return_lines → sales_returns

## Summary
Each sales_returns row can have zero or many sales_return_lines rows attached to it; each sales_return_lines row must belong to exactly one sales_returns. This means that for every item returned in a sales_return_lines entry, there is a corresponding sales_returns entry that documents the return details, such as the reason and date.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_return_lines]] |
| Source column | `return_id` |
| Target table | [[entities/sales_returns]] |
| Target column | `return_id` |
| Constraint | `sales_return_lines_return_id_fkey` |
| Cardinality (sales_return_lines → sales_returns) | many-to-one |
| Cardinality (sales_returns → sales_return_lines) | one-to-many |
| Optionality | mandatory — return_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_return_lines.return_id` | `sales_returns.return_id` |

## Sample Matches
| sales_return_lines.return_id | sales_returns.return_id | sales_returns.return_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |

## Tensions Or Gaps
There are no notable modeling risks in this relationship, as the foreign key constraint ensures that each sales_return_lines row is properly linked to an existing sales_returns row, preventing any orphaned records.

## Related
- [[entities/sales_return_lines]]
- [[entities/sales_returns]]
- [[relationships/sales_return_lines-items]]
- [[relationships/sales_returns-sales_invoices]]
- [[relationships/overview]]
