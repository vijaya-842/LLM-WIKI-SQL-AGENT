---
title: vendor_invoices → vendors (vendor_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.vendor_invoices
  - live-database:public.vendors
source_count: 2
---

# vendor_invoices → vendors

## Summary
Each vendors row can have zero or many vendor_invoices rows attached to it; each vendor_invoices row must belong to exactly one vendors. This relationship ensures that invoices are always tied to a specific vendor, as evidenced by the sample matched rows showing multiple invoices linked to individual vendors.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_invoices]] |
| Source column | `vendor_id` |
| Target table | [[entities/vendors]] |
| Target column | `vendor_id` |
| Constraint | `vendor_invoices_vendor_id_fkey` |
| Cardinality (vendor_invoices → vendors) | many-to-one |
| Cardinality (vendors → vendor_invoices) | one-to-many |
| Optionality | mandatory — vendor_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_invoices.vendor_id` | `vendors.vendor_id` |

## Sample Matches
| vendor_invoices.vendor_id | vendors.vendor_id | vendors.vendor_name |
|---|---|---|
| V00234 | V00234 | National Dry Goods Corp |
| V00345 | V00345 | Sunrise Dairy Cooperative |
| V00567 | V00567 | Premium Meat Solutions Inc |
| V00789 | V00789 | Global Produce Partners LLC |
| V00123 | V00123 | ABC Food Distributors Inc |

## Tensions Or Gaps
There appear to be no modeling risks or notable gaps in the current foreign key relationship, as the constraints and cardinality are clear and logical in the context of the business rules.

## Related
- [[entities/vendor_invoices]]
- [[entities/vendors]]
- [[relationships/growth_opportunity_event-vendors]]
- [[relationships/payment_transactions-vendor_invoices]]
- [[relationships/purchase_orders-vendors]]
- [[relationships/site_vendor_assignments-vendors]]
- [[relationships/vendor_contracts-vendors]]
- [[relationships/vendor_invoice_lines-vendor_invoices]]
- [[relationships/vendor_invoices-purchase_orders]]
- [[relationships/vendor_performance-vendors]]
- [[relationships/vendor_pricing-vendors]]
- [[relationships/vendor_shipping_points-vendors]]
- [[relationships/overview]]
