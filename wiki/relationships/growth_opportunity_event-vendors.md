---
title: growth_opportunity_event → vendors (true_vendor)
type: concept
status: active
created: 2026-07-31
updated: 2026-08-03
source_paths:
  - live-database:public.growth_opportunity_event
  - live-database:public.vendors
source_count: 2
---

# growth_opportunity_event → vendors

## Summary
Each vendors row can have zero or many growth_opportunity_event rows attached to it; each growth_opportunity_event row's link to vendors is optional, meaning it may not always have an associated vendor. This is exemplified in the sample matches where several growth_opportunity_event entries reference various vendors, showcasing the many-to-one relationship.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/growth_opportunity_event]] |
| Source column | `true_vendor` |
| Target table | [[entities/vendors]] |
| Target column | `vendor_id` |
| Constraint | `fk_goe_true_vendor` |
| Cardinality (growth_opportunity_event → vendors) | many-to-one |
| Cardinality (vendors → growth_opportunity_event) | one-to-many |
| Optionality | optional — true_vendor is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `growth_opportunity_event.true_vendor` | `vendors.vendor_id` |

## Sample Matches
| growth_opportunity_event.true_vendor | vendors.vendor_id | vendors.vendor_name |
|---|---|---|
| V00123 | V00123 | ABC Food Distributors Inc |
| V00789 | V00789 | Global Produce Partners LLC |
| V00234 | V00234 | National Dry Goods Corp |
| V00567 | V00567 | Premium Meat Solutions Inc |
| V00345 | V00345 | Sunrise Dairy Cooperative |

## Tensions Or Gaps
There is a potential modeling risk due to the optional foreign key, which means some growth_opportunity_event rows may be orphaned by design, lacking an associated vendor. This could lead to incomplete data in scenarios where vendor information is crucial for business operations.

## Related
- [[entities/growth_opportunity_event]]
- [[entities/vendors]]
- [[relationships/growth_opportunity_event-sites]]
- [[relationships/growth_opportunity_event-source_vendors]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/purchase_orders-vendors]]
- [[relationships/site_vendor_assignments-vendors]]
- [[relationships/vendor_contracts-vendors]]
- [[relationships/vendor_invoices-vendors]]
- [[relationships/vendor_performance-vendors]]
- [[relationships/vendor_pricing-vendors]]
- [[relationships/vendor_shipping_points-vendors]]
- [[relationships/overview]]
