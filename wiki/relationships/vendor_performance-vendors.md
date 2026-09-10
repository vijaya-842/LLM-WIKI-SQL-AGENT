---
title: vendor_performance → vendors (vendor_id)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.vendor_performance
  - live-database:public.vendors
source_count: 2
---

# vendor_performance → vendors

## Summary
This foreign key establishes a many-to-one relationship where each `vendor_performance` row must link to exactly one `vendors` row, while each `vendors` row can have zero or many `vendor_performance` rows attached to it. The link captures monthly performance metrics such as `on_time_rate` and `quality_score` for specific vendors, allowing the system to track historical performance data against the static vendor master record.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_performance]] |
| Source column | `vendor_id` |
| Target table | [[entities/vendors]] |
| Target column | `vendor_id` |
| Constraint | `vendor_performance_vendor_id_fkey` |
| Cardinality (vendor_performance → vendors) | many-to-one |
| Cardinality (vendors → vendor_performance) | one-to-many |
| Optionality | mandatory — vendor_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_performance.vendor_id` | `vendors.vendor_id` |

## Sample Matches
| vendor_performance.vendor_id | vendors.vendor_id | vendors.vendor_name |
|---|---|---|
| V00234 | V00234 | National Dry Goods Corp |
| V00234 | V00234 | National Dry Goods Corp |
| V00234 | V00234 | National Dry Goods Corp |
| V00345 | V00345 | Sunrise Dairy Cooperative |
| V00345 | V00345 | Sunrise Dairy Cooperative |

## Tensions Or Gaps
No notable modeling risks were identified; the mandatory foreign key ensures that every performance record is strictly attributed to a valid vendor, preventing orphaned data.

## Related
- [[entities/vendor_performance]]
- [[entities/vendors]]
- [[relationships/site_vendor_assignments-vendors]]
- [[relationships/vendor_contracts-vendors]]
- [[relationships/vendor_pricing-vendors]]
- [[relationships/vendor_shipping_points-vendors]]
- [[relationships/overview]]
