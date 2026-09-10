---
title: Schema Relationships Overview
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
source_count: 0
---

# Schema Relationships Overview

## Summary
This page indexes every foreign-key relationship in the live schema (10 total). See [[index]] for the full entity catalog and [[overview]] for context.

## Evidence
| Source Table | Source Column | Target Table | Target Column | Cardinality | Detail |
|---|---|---|---|---|---|
| [[entities/site_vendor_assignments]] | `site` | [[entities/sites]] | `site` | many-to-one | [[relationships/site_vendor_assignments-sites]] |
| [[entities/site_vendor_assignments]] | `vendor_id` | [[entities/vendors]] | `vendor_id` | many-to-one | [[relationships/site_vendor_assignments-vendors]] |
| [[entities/source_vendor_pricing]] | `item_no` | [[entities/items]] | `item_no` | many-to-one | [[relationships/source_vendor_pricing-items]] |
| [[entities/source_vendor_pricing]] | `source_vendor_id` | [[entities/source_vendors]] | `source_vendor_id` | many-to-one | [[relationships/source_vendor_pricing-source_vendors]] |
| [[entities/vendor_contracts]] | `source_vendor_id` | [[entities/source_vendors]] | `source_vendor_id` | many-to-one | [[relationships/vendor_contracts-source_vendors]] |
| [[entities/vendor_contracts]] | `vendor_id` | [[entities/vendors]] | `vendor_id` | many-to-one | [[relationships/vendor_contracts-vendors]] |
| [[entities/vendor_performance]] | `vendor_id` | [[entities/vendors]] | `vendor_id` | many-to-one | [[relationships/vendor_performance-vendors]] |
| [[entities/vendor_pricing]] | `item_no` | [[entities/items]] | `item_no` | many-to-one | [[relationships/vendor_pricing-items]] |
| [[entities/vendor_pricing]] | `vendor_id` | [[entities/vendors]] | `vendor_id` | many-to-one | [[relationships/vendor_pricing-vendors]] |
| [[entities/vendor_shipping_points]] | `vendor_id` | [[entities/vendors]] | `vendor_id` | many-to-one | [[relationships/vendor_shipping_points-vendors]] |

## Tensions Or Gaps
Each row links to a dedicated relationship page with the field mapping, cardinality, and real matched sample rows for that FK.

## Related
- [[index]]
- [[overview]]
