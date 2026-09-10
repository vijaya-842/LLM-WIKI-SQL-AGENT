---
title: customers → sites (site)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.customers
  - live-database:public.sites
source_count: 2
---

# customers → sites

## Summary
Each sites row can have zero or many customers rows attached to it; each customers row can belong to exactly one sites. The foreign key relationship between the "customers" table and the "sites" table reflects that some customers, like "Riverside Diner Group" and "Metro School District," are linked to specific site locations such as "Site 0091" and "Site 0055," while others may not have a corresponding site.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/customers]] |
| Source column | `site` |
| Target table | [[entities/sites]] |
| Target column | `site` |
| Constraint | `customers_site_fkey` |
| Cardinality (customers → sites) | many-to-one |
| Cardinality (sites → customers) | one-to-many |
| Optionality | optional — site is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `customers.site` | `sites.site` |

## Sample Matches
| customers.site | sites.site | sites.site_name |
|---|---|---|
| 0091 | 0091 | Site 0091 - Distribution Center |
| 0055 | 0055 | Site 0055 - Distribution Center |
| 0019 | 0019 | Site 0019 - Distribution Center |
| 0078 | 0078 | Site 0078 - Distribution Center |
| 0042 | 0042 | Site 0042 - Distribution Center |

## Tensions Or Gaps
The optional foreign key from "customers" to "sites" indicates that some customers may not be associated with any site at all, which could lead to potential orphaned records.

## Related
- [[entities/customers]]
- [[entities/sites]]
- [[relationships/customer_credit_terms-customers]]
- [[relationships/growth_opportunity_event-sites]]
- [[relationships/purchase_orders-sites]]
- [[relationships/purchase_requisitions-sites]]
- [[relationships/sales_orders-sites]]
- [[relationships/sales_orders-customers]]
- [[relationships/shipments-sites]]
- [[relationships/site_vendor_assignments-sites]]
- [[relationships/overview]]
