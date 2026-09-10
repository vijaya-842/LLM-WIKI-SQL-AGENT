---
title: status enum
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_orders
  - live-database:public.purchase_requisitions
  - live-database:public.sales_invoices
  - live-database:public.sales_orders
  - live-database:public.vendor_invoices
source_count: 5
---

# status

## Summary
Observed distinct values for `status`, queried live from 5 table(s) rather than inferred.

## Evidence
### `purchase_orders.status`

| Value | Count |
|---|---|
| Open | 4 |
| Closed | 4 |
### `purchase_requisitions.status`

| Value | Count |
|---|---|
| Approved | 6 |
### `sales_invoices.status`

| Value | Count |
|---|---|
| Unpaid | 4 |
| Paid | 4 |
### `sales_orders.status`

| Value | Count |
|---|---|
| Open | 5 |
| Closed | 3 |
### `vendor_invoices.status`

| Value | Count |
|---|---|
| Unpaid | 4 |
| Paid | 4 |

## Tensions Or Gaps
*inferred*: different tables reuse this column name with different observed values — confirm they mean the same thing before treating them as one shared enum.

## Related
- [[entities/purchase_orders]]
- [[entities/purchase_requisitions]]
- [[entities/sales_invoices]]
- [[entities/sales_orders]]
- [[entities/vendor_invoices]]
- [[glossary]]
