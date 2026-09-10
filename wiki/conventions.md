---
title: Conventions
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
source_count: 0
---

# Conventions

## Summary
Naming, audit-column, soft-delete, and timestamp patterns observed across the live schema. This consolidates what would otherwise be repeated on every entity page.

## Evidence
- *inferred*: 0/14 table(s) follow a `created_timestamp`/`updated_timestamp` (or `created_at`/`updated_at`) audit-column pair: none.
- *inferred*: soft-delete/active-flag style columns found on: `vendors.active_flag`.
- *inferred*: single-character (`CHAR(1)`) flag columns, likely Y/N-style booleans: `site_vendor_assignments.is_primary`, `vendors.active_flag`.
- *inferred*: timestamp column types in use — `timestamp without time zone` (2 column(s)). None of these are timezone-aware (`timestamp with time zone`); treat all timestamps as naive/local unless a source says otherwise.

### Primary key naming per table
- items: `item_no` (matches `<table>_id`)
- site_vendor_assignments: composite (`site, vendor_id`)
- sites: `site` (matches `<table>_id`)
- source_vendor_pricing: `pricing_id`
- source_vendors: `source_vendor_id` (matches `<table>_id`)
- users: `id`
- vendor_contracts: `contract_id`
- vendor_performance: composite (`vendor_id, period_month`)
- vendor_pricing: `pricing_id`
- vendor_shipping_points: composite (`vendor_id, ship_point`)
- vendors: `vendor_id` (matches `<table>_id`)

## Tensions Or Gaps
All patterns on this page are *inferred* from observed column names/types, not enforced by the database — treat them as convention, not guarantee.

## Related
- [[index]]
- [[glossary]]
- [[erd]]
