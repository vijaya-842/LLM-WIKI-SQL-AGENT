---
title: vendor_shipping_points → vendors (vendor_id)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.vendor_shipping_points
  - live-database:public.vendors
source_count: 2
---

# vendor_shipping_points → vendors

## Summary
Each `vendor_shipping_points` row must belong to exactly one `vendors` row, establishing that every shipping point is mandatorily linked to a specific vendor. This many-to-one relationship means that a single vendor (such as "National Dry Goods Corp" or "Sunrise Dairy Cooperative") can be associated with one or more distinct shipping points, while no shipping point exists without a valid parent vendor.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_shipping_points]] |
| Source column | `vendor_id` |
| Target table | [[entities/vendors]] |
| Target column | `vendor_id` |
| Constraint | `vendor_shipping_points_vendor_id_fkey` |
| Cardinality (vendor_shipping_points → vendors) | many-to-one |
| Cardinality (vendors → vendor_shipping_points) | one-to-many |
| Optionality | mandatory — vendor_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_shipping_points.vendor_id` | `vendors.vendor_id` |

## Sample Matches
| vendor_shipping_points.vendor_id | vendors.vendor_id | vendors.vendor_name |
|---|---|---|
| V00234 | V00234 | National Dry Goods Corp |
| V00345 | V00345 | Sunrise Dairy Cooperative |
| V00567 | V00567 | Premium Meat Solutions Inc |
| V00789 | V00789 | Global Produce Partners LLC |
| V00123 | V00123 | ABC Food Distributors Inc |

## Tensions Or Gaps
The modeling is sound with no notable risks; the mandatory nature of the foreign key ensures data integrity by preventing orphaned shipping points, and the one-to-many cardinality is appropriate for scenarios where a vendor operates multiple distinct dock or ship locations.

## Related
- [[entities/vendor_shipping_points]]
- [[entities/vendors]]
- [[relationships/site_vendor_assignments-vendors]]
- [[relationships/vendor_contracts-vendors]]
- [[relationships/vendor_performance-vendors]]
- [[relationships/vendor_pricing-vendors]]
- [[relationships/overview]]
