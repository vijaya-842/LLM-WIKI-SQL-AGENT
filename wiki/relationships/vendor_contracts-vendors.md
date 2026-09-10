---
title: vendor_contracts → vendors (vendor_id)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.vendor_contracts
  - live-database:public.vendors
source_count: 2
---

# vendor_contracts → vendors

## Summary
This foreign key establishes a many-to-one relationship from `vendor_contracts` to `vendors`, where each `vendor_contracts` row must belong to exactly one `vendors` row while each `vendors` row can have zero or many `vendor_contracts` rows attached to it. Business-wise, this links individual contract records, such as those for "National Dry Goods Corp" or "Sunrise Dairy Cooperative," to their corresponding active vendor master records via the `vendor_id` identifier.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_contracts]] |
| Source column | `vendor_id` |
| Target table | [[entities/vendors]] |
| Target column | `vendor_id` |
| Constraint | `vendor_contracts_vendor_id_fkey` |
| Cardinality (vendor_contracts → vendors) | many-to-one |
| Cardinality (vendors → vendor_contracts) | one-to-many |
| Optionality | mandatory — vendor_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_contracts.vendor_id` | `vendors.vendor_id` |

## Sample Matches
| vendor_contracts.vendor_id | vendors.vendor_id | vendors.vendor_name |
|---|---|---|
| V00234 | V00234 | National Dry Goods Corp |
| V00345 | V00345 | Sunrise Dairy Cooperative |
| V00567 | V00567 | Premium Meat Solutions Inc |
| V00789 | V00789 | Global Produce Partners LLC |
| V00123 | V00123 | ABC Food Distributors Inc |

## Tensions Or Gaps
There are no notable modeling tensions or gaps; the mandatory nature of the link ensures that no contract record exists without a valid reference to a specific vendor, providing a clear and enforced dependency structure.

## Related
- [[entities/vendor_contracts]]
- [[entities/vendors]]
- [[relationships/site_vendor_assignments-vendors]]
- [[relationships/vendor_contracts-source_vendors]]
- [[relationships/vendor_performance-vendors]]
- [[relationships/vendor_pricing-vendors]]
- [[relationships/vendor_shipping_points-vendors]]
- [[relationships/overview]]
