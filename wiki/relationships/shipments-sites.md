---
title: shipments → sites (site)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.shipments
  - live-database:public.sites
source_count: 2
---

# shipments → sites

## Summary
Each sites row can have zero or many shipments rows attached to it; each shipments row must belong to exactly one sites. The foreign key relationship between the "shipments" table (specifically the "site" column) and the "sites" table ensures that every shipment is linked to a valid site, as demonstrated by the sample matches.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/shipments]] |
| Source column | `site` |
| Target table | [[entities/sites]] |
| Target column | `site` |
| Constraint | `shipments_site_fkey` |
| Cardinality (shipments → sites) | many-to-one |
| Cardinality (sites → shipments) | one-to-many |
| Optionality | mandatory — site is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `shipments.site` | `sites.site` |

## Sample Matches
| shipments.site | sites.site | sites.site_name |
|---|---|---|
| 0091 | 0091 | Site 0091 - Distribution Center |
| 0055 | 0055 | Site 0055 - Distribution Center |
| 0019 | 0019 | Site 0019 - Distribution Center |
| 0078 | 0078 | Site 0078 - Distribution Center |
| 0042 | 0042 | Site 0042 - Distribution Center |

## Tensions Or Gaps
There are no notable tensions or gaps in the modeling, as the foreign key constraint ensures that each shipments row must be associated with a sites row, eliminating the risk of orphaned shipments.

## Related
- [[entities/shipments]]
- [[entities/sites]]
- [[relationships/customers-sites]]
- [[relationships/growth_opportunity_event-sites]]
- [[relationships/purchase_orders-sites]]
- [[relationships/purchase_requisitions-sites]]
- [[relationships/sales_orders-sites]]
- [[relationships/shipment_lines-shipments]]
- [[relationships/shipments-sales_orders]]
- [[relationships/site_vendor_assignments-sites]]
- [[relationships/overview]]
