---
title: vendor_pricing → vendors (vendor_id)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.vendor_pricing
  - live-database:public.vendors
source_count: 2
---

# vendor_pricing → vendors

## Summary
The `vendor_pricing` table links specific price points to supplier records via `vendor_pricing.vendor_id`, establishing a many-to-one relationship where each pricing row must belong to exactly one vendors row. Conversely, each vendors row can have zero or many vendor_pricing rows attached to it, allowing a single supplier to maintain multiple historical or active price entries for various items. For example, "National Dry Goods Corp" (V00234) appears in multiple pricing rows with different effective dates for the same item, illustrating how individual vendors accumulate numerous pricing records over time.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_pricing]] |
| Source column | `vendor_id` |
| Target table | [[entities/vendors]] |
| Target column | `vendor_id` |
| Constraint | `vendor_pricing_vendor_id_fkey` |
| Cardinality (vendor_pricing → vendors) | many-to-one |
| Cardinality (vendors → vendor_pricing) | one-to-many |
| Optionality | mandatory — vendor_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_pricing.vendor_id` | `vendors.vendor_id` |

## Sample Matches
| vendor_pricing.vendor_id | vendors.vendor_id | vendors.vendor_name |
|---|---|---|
| V00234 | V00234 | National Dry Goods Corp |
| V00234 | V00234 | National Dry Goods Corp |
| V00345 | V00345 | Sunrise Dairy Cooperative |
| V00345 | V00345 | Sunrise Dairy Cooperative |
| V00567 | V00567 | Premium Meat Solutions Inc |

## Tensions Or Gaps
No notable modeling risks are present; the mandatory (NOT NULL) foreign key ensures data integrity by preventing orphaned pricing records, and the many-to-one cardinality is appropriate for tracking multiple price points per vendor.

## Related
- [[entities/vendor_pricing]]
- [[entities/vendors]]
- [[relationships/site_vendor_assignments-vendors]]
- [[relationships/vendor_contracts-vendors]]
- [[relationships/vendor_performance-vendors]]
- [[relationships/vendor_pricing-items]]
- [[relationships/vendor_shipping_points-vendors]]
- [[relationships/overview]]
