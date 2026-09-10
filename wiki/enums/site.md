---
title: site enum
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.site_vendor_assignments
  - live-database:public.sites
source_count: 2
---

# site

## Summary
Observed distinct values for `site`, queried live from 2 table(s) rather than inferred.

## Evidence
### `site_vendor_assignments.site`

| Value | Count |
|---|---|
| 0055 | 2 |
| 0091 | 2 |
| 0019 | 1 |
| 0078 | 1 |
| 0042 | 1 |
| 0063 | 1 |
### `sites.site`

| Value | Count |
|---|---|
| 0055 | 1 |
| 0019 | 1 |
| 0078 | 1 |
| 0042 | 1 |
| 0063 | 1 |
| 0091 | 1 |

## Tensions Or Gaps
All tables using this column name share the same observed value set.

## Related
- [[entities/site_vendor_assignments]]
- [[entities/sites]]
- [[glossary]]
