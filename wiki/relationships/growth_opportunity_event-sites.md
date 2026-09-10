---
title: growth_opportunity_event → sites (site)
type: concept
status: active
created: 2026-07-31
updated: 2026-08-03
source_paths:
  - live-database:public.growth_opportunity_event
  - live-database:public.sites
source_count: 2
---

# growth_opportunity_event → sites

## Summary
Each sites row can have zero or many growth_opportunity_event rows attached to it; each growth_opportunity_event row must belong to exactly one sites. This relationship allows tracking multiple opportunity events at specific sites, as demonstrated in the sample matches where events are linked to their respective distribution centers.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/growth_opportunity_event]] |
| Source column | `site` |
| Target table | [[entities/sites]] |
| Target column | `site` |
| Constraint | `fk_goe_site` |
| Cardinality (growth_opportunity_event → sites) | many-to-one |
| Cardinality (sites → growth_opportunity_event) | one-to-many |
| Optionality | optional — site is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `growth_opportunity_event.site` | `sites.site` |

## Sample Matches
| growth_opportunity_event.site | sites.site | sites.site_name |
|---|---|---|
| 0019 | 0019 | Site 0019 - Distribution Center |
| 0042 | 0042 | Site 0042 - Distribution Center |
| 0055 | 0055 | Site 0055 - Distribution Center |
| 0078 | 0078 | Site 0078 - Distribution Center |
| 0091 | 0091 | Site 0091 - Distribution Center |

## Tensions Or Gaps
The optional foreign key indicates that some growth_opportunity_event rows may not be linked to any site, potentially leading to orphaned records by design. This should be monitored to ensure data integrity and relevance.

## Related
- [[entities/growth_opportunity_event]]
- [[entities/sites]]
- [[relationships/customers-sites]]
- [[relationships/growth_opportunity_event-vendors]]
- [[relationships/growth_opportunity_event-source_vendors]]
- [[relationships/growth_opportunity_event-items]]
- [[relationships/purchase_orders-sites]]
- [[relationships/purchase_requisitions-sites]]
- [[relationships/sales_orders-sites]]
- [[relationships/shipments-sites]]
- [[relationships/site_vendor_assignments-sites]]
- [[relationships/overview]]
