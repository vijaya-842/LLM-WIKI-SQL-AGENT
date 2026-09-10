---
title: site_vendor_assignments → vendors (vendor_id)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.site_vendor_assignments
  - live-database:public.vendors
source_count: 2
---

# site_vendor_assignments → vendors

## Summary
This foreign key establishes a many-to-one relationship where each `site_vendor_assignments` row must belong to exactly one `vendors` row, while each `vendors` row can have zero or many `site_vendor_assignments` rows attached to it. The link is mandatory for every assignment record, meaning a site's vendor designation cannot exist without a corresponding valid vendor entry, as seen in the samples where `vendor_id` values like "V00234" connect specific sites to active vendors such as "National Dry Goods Corp".

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/site_vendor_assignments]] |
| Source column | `vendor_id` |
| Target table | [[entities/vendors]] |
| Target column | `vendor_id` |
| Constraint | `site_vendor_assignments_vendor_id_fkey` |
| Cardinality (site_vendor_assignments → vendors) | many-to-one |
| Cardinality (vendors → site_vendor_assignments) | one-to-many |
| Optionality | mandatory — vendor_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `site_vendor_assignments.vendor_id` | `vendors.vendor_id` |

## Sample Matches
| site_vendor_assignments.vendor_id | vendors.vendor_id | vendors.vendor_name |
|---|---|---|
| V00234 | V00234 | National Dry Goods Corp |
| V00345 | V00345 | Sunrise Dairy Cooperative |
| V00567 | V00567 | Premium Meat Solutions Inc |
| V00789 | V00789 | Global Produce Partners LLC |
| V00123 | V00123 | ABC Food Distributors Inc |

## Tensions Or Gaps
The schema appears robust regarding data integrity for this relationship, as the non-nullable `vendor_id` in `site_vendor_assignments` prevents orphaned records that lack a valid parent vendor. There are no notable modeling risks or gaps identified in the provided facts, given that the cardinality and optionality strictly enforce a dependent-to-independence structure appropriate for this business context.

## Related
- [[entities/site_vendor_assignments]]
- [[entities/vendors]]
- [[relationships/site_vendor_assignments-sites]]
- [[relationships/vendor_contracts-vendors]]
- [[relationships/vendor_performance-vendors]]
- [[relationships/vendor_pricing-vendors]]
- [[relationships/vendor_shipping_points-vendors]]
- [[relationships/overview]]
