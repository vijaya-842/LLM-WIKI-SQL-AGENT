---
title: event_type enum
type: concept
status: active
created: 2026-07-31
updated: 2026-08-03
source_paths:
  - live-database:public.growth_opportunity_event
source_count: 1
---

# event_type

## Summary
Observed distinct values for `event_type`, queried live from 1 table(s) rather than inferred.

## Evidence
### `growth_opportunity_event.event_type`

| Value | Count |
|---|---|
| SOURCE_CHANGE | 1 |
| ITEM_CONVERSION | 1 |
| PRICE_CHANGE | 1 |
| NEW_ITEM | 1 |
| NEW_VENDOR | 1 |

## Tensions Or Gaps
All tables using this column name share the same observed value set.

## Related
- [[entities/growth_opportunity_event]]
- [[glossary]]
