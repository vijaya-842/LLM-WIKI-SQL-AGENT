---
title: growth_opportunity_event → source_vendors (source_vendor)
type: concept
status: active
created: 2026-07-31
updated: 2026-08-03
source_paths:
  - live-database:public.growth_opportunity_event
  - live-database:public.source_vendors
source_count: 2
---

# growth_opportunity_event → source_vendors

## Summary
Each source_vendors row can have zero or many growth_opportunity_event rows attached to it; each growth_opportunity_event row must belong to exactly one source_vendors. This relationship supports the tracking of growth opportunities related to specific vendors, as illustrated by rows in the sample matches, where events are linked to particular source vendors.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/growth_opportunity_event]] |
| Source column | `source_vendor` |
| Target table | [[entities/source_vendors]] |
| Target column | `source_vendor_id` |
| Constraint | `fk_goe_source_vendor` |
| Cardinality (growth_opportunity_event → source_vendors) | many-to-one |
| Cardinality (source_vendors → growth_opportunity_event) | one-to-many |
| Optionality | optional — source_vendor is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `growth_opportunity_event.source_vendor` | `source_vendors.source_vendor_id` |

## Sample Matches
| growth_opportunity_event.source_vendor | source_vendors.source_vendor_id | source_vendors.source_vendor_name |
|---|---|---|
| SV00456 | SV00456 | Western Food Supply Co |
| SV00321 | SV00321 | Eastern Fresh Goods Ltd |
| SV00567 | SV00567 | Central Supply Network |
| SV00890 | SV00890 | Northern Protein Co |
| SV00678 | SV00678 | Pacific Dairy Group |

## Tensions Or Gaps
The optional foreign key from growth_opportunity_event to source_vendors indicates that some growth_opportunity_event rows may be orphaned by design, meaning they do not necessarily have an associated source vendor. This could lead to a potential inconsistency in understanding the context of certain events.

## Related
- [[entities/growth_opportunity_event]]
- [[entities/source_vendors]]
- [[relationships/growth_opportunity_event-sites]]
- [[relationships/growth_opportunity_event-vendors]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/source_vendor_pricing-source_vendors]]
- [[relationships/vendor_contracts-source_vendors]]
- [[relationships/overview]]
