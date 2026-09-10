---
title: sales_orders → sites (site)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.sales_orders
  - live-database:public.sites
source_count: 2
---

# sales_orders → sites

## Summary
Each `sites` row can have zero or many `sales_orders` rows attached to it; each `sales_orders` row must belong to exactly one `sites`. This relationship ensures that every order is associated with a specific distribution site, as seen in the sample matches where each order is tied to a distinct site with its corresponding details.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/sales_orders]] |
| Source column | `site` |
| Target table | [[entities/sites]] |
| Target column | `site` |
| Constraint | `sales_orders_site_fkey` |
| Cardinality (sales_orders → sites) | many-to-one |
| Cardinality (sites → sales_orders) | one-to-many |
| Optionality | mandatory — site is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `sales_orders.site` | `sites.site` |

## Sample Matches
| sales_orders.site | sites.site | sites.site_name |
|---|---|---|
| 0091 | 0091 | Site 0091 - Distribution Center |
| 0055 | 0055 | Site 0055 - Distribution Center |
| 0019 | 0019 | Site 0019 - Distribution Center |
| 0078 | 0078 | Site 0078 - Distribution Center |
| 0042 | 0042 | Site 0042 - Distribution Center |

## Tensions Or Gaps
There are no notable modeling risks in this relationship as the foreign key constraint enforces mandatory linkage from `sales_orders` to `sites`, ensuring that all sales orders are properly associated with a site.

## Related
- [[entities/sales_orders]]
- [[entities/sites]]
- [[relationships/customers-sites]]
- [[relationships/growth_opportunity_event-sites]]
- [[relationships/purchase_orders-sites]]
- [[relationships/purchase_requisitions-sites]]
- [[relationships/sales_invoices-sales_orders]]
- [[relationships/sales_order_lines-sales_orders]]
- [[relationships/sales_orders-sales_reps]]
- [[relationships/sales_orders-customers]]
- [[relationships/shipments-sites]]
- [[relationships/shipments-sales_orders]]
- [[relationships/site_vendor_assignments-sites]]
- [[relationships/overview]]
