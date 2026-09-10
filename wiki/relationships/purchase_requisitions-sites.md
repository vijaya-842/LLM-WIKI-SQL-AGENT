---
title: purchase_requisitions → sites (site)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_requisitions
  - live-database:public.sites
source_count: 2
---

# purchase_requisitions → sites

## Summary
Each sites row can have zero or many purchase_requisitions rows attached to it; each purchase_requisitions row must belong to exactly one sites. This relationship ensures that every purchase requisition is linked to an existing site, as demonstrated by the sample matches where each requisition is associated with a specific distribution center.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/purchase_requisitions]] |
| Source column | `site` |
| Target table | [[entities/sites]] |
| Target column | `site` |
| Constraint | `purchase_requisitions_site_fkey` |
| Cardinality (purchase_requisitions → sites) | many-to-one |
| Cardinality (sites → purchase_requisitions) | one-to-many |
| Optionality | mandatory — site is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `purchase_requisitions.site` | `sites.site` |

## Sample Matches
| purchase_requisitions.site | sites.site | sites.site_name |
|---|---|---|
| 0091 | 0091 | Site 0091 - Distribution Center |
| 0055 | 0055 | Site 0055 - Distribution Center |
| 0019 | 0019 | Site 0019 - Distribution Center |
| 0078 | 0078 | Site 0078 - Distribution Center |
| 0042 | 0042 | Site 0042 - Distribution Center |

## Tensions Or Gaps
There do not appear to be any notable modeling risks in this relationship, as each purchase_requisitions row is required to link to an existing sites row, ensuring no orphaned requisitions will occur by design.

## Related
- [[entities/purchase_requisitions]]
- [[entities/sites]]
- [[relationships/customers-sites]]
- [[relationships/growth_opportunity_event-sites]]
- [[relationships/purchase_orders-purchase_requisitions]]
- [[relationships/purchase_orders-sites]]
- [[relationships/purchase_requisition_lines-purchase_requisitions]]
- [[relationships/sales_orders-sites]]
- [[relationships/shipments-sites]]
- [[relationships/site_vendor_assignments-sites]]
- [[relationships/overview]]
