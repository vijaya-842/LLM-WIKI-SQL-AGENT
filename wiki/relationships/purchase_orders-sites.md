---
title: purchase_orders → sites (site)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_orders
  - live-database:public.sites
source_count: 2
---

# purchase_orders → sites

## Summary
Each sites row can have zero or many purchase_orders rows attached to it; each purchase_orders row must belong to exactly one sites. This relationship illustrates that every purchase order must be associated with a specific site, ensuring that orders are properly linked to their respective distribution centers, as seen in the sample matches.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/purchase_orders]] |
| Source column | `site` |
| Target table | [[entities/sites]] |
| Target column | `site` |
| Constraint | `purchase_orders_site_fkey` |
| Cardinality (purchase_orders → sites) | many-to-one |
| Cardinality (sites → purchase_orders) | one-to-many |
| Optionality | mandatory — site is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `purchase_orders.site` | `sites.site` |

## Sample Matches
| purchase_orders.site | sites.site | sites.site_name |
|---|---|---|
| 0091 | 0091 | Site 0091 - Distribution Center |
| 0055 | 0055 | Site 0055 - Distribution Center |
| 0019 | 0019 | Site 0019 - Distribution Center |
| 0078 | 0078 | Site 0078 - Distribution Center |
| 0042 | 0042 | Site 0042 - Distribution Center |

## Tensions Or Gaps
There are no notable modeling risks identified; the foreign key relationship is clear, and the structure ensures that each purchase_orders row is properly linked to a sites row.

## Related
- [[entities/purchase_orders]]
- [[entities/sites]]
- [[relationships/customers-sites]]
- [[relationships/growth_opportunity_event-sites]]
- [[relationships/po_receipts-purchase_orders]]
- [[relationships/purchase_order_lines-purchase_orders]]
- [[relationships/purchase_orders-vendors]]
- [[relationships/purchase_orders-purchase_requisitions]]
- [[relationships/purchase_requisitions-sites]]
- [[relationships/sales_orders-sites]]
- [[relationships/shipments-sites]]
- [[relationships/site_vendor_assignments-sites]]
- [[relationships/vendor_invoices-purchase_orders]]
- [[relationships/overview]]
