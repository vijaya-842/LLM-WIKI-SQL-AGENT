---
title: price_unit enum
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.source_vendor_pricing
  - live-database:public.vendor_pricing
source_count: 2
---

# price_unit

## Summary
Observed distinct values for `price_unit`, queried live from 2 table(s) rather than inferred.

## Evidence
### `source_vendor_pricing.price_unit`

| Value | Count |
|---|---|
| CS | 7 |
### `vendor_pricing.price_unit`

| Value | Count |
|---|---|
| CS | 14 |

## Tensions Or Gaps
All tables using this column name share the same observed value set.

## Related
- [[entities/source_vendor_pricing]]
- [[entities/vendor_pricing]]
- [[glossary]]
