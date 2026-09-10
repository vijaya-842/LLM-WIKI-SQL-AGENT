---
title: po_receipt_lines → po_receipts (receipt_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.po_receipt_lines
  - live-database:public.po_receipts
source_count: 2
---

# po_receipt_lines → po_receipts

## Summary
Each `po_receipts` row can have zero or many `po_receipt_lines` rows attached to it; each `po_receipt_lines` row must belong to exactly one `po_receipts`. This relationship ensures that every line item recorded in the `po_receipt_lines` table is associated with a corresponding receipt in the `po_receipts` table, as illustrated by the matched sample rows.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/po_receipt_lines]] |
| Source column | `receipt_id` |
| Target table | [[entities/po_receipts]] |
| Target column | `receipt_id` |
| Constraint | `po_receipt_lines_receipt_id_fkey` |
| Cardinality (po_receipt_lines → po_receipts) | many-to-one |
| Cardinality (po_receipts → po_receipt_lines) | one-to-many |
| Optionality | mandatory — receipt_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `po_receipt_lines.receipt_id` | `po_receipts.receipt_id` |

## Sample Matches
| po_receipt_lines.receipt_id | po_receipts.receipt_id | po_receipts.receipt_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

## Tensions Or Gaps
There are no notable modeling risks in this relationship. The mandatory foreign key constraint ensures that every `po_receipt_lines` row is properly linked to a `po_receipts` row, eliminating the possibility of orphaned records.

## Related
- [[entities/po_receipt_lines]]
- [[entities/po_receipts]]
- [[relationships/po_receipt_lines-items]]
- [[relationships/po_receipts-purchase_orders]]
- [[relationships/overview]]
