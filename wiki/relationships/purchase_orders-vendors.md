---
title: purchase_orders → vendors (vendor_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.purchase_orders
  - live-database:public.vendors
source_count: 2
---

# purchase_orders → vendors

## Summary
Each vendors row can have zero or many purchase_orders rows attached to it; each purchase_orders row must belong to exactly one vendors. This relationship ensures that every purchase order is linked to a specific vendor, as demonstrated by the sample matches where each purchase order references a unique vendor.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/purchase_orders]] |
| Source column | `vendor_id` |
| Target table | [[entities/vendors]] |
| Target column | `vendor_id` |
| Constraint | `purchase_orders_vendor_id_fkey` |
| Cardinality (purchase_orders → vendors) | many-to-one |
| Cardinality (vendors → purchase_orders) | one-to-many |
| Optionality | mandatory — vendor_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `purchase_orders.vendor_id` | `vendors.vendor_id` |

## Sample Matches
| purchase_orders.vendor_id | vendors.vendor_id | vendors.vendor_name |
|---|---|---|
| V00234 | V00234 | National Dry Goods Corp |
| V00345 | V00345 | Sunrise Dairy Cooperative |
| V00567 | V00567 | Premium Meat Solutions Inc |
| V00789 | V00789 | Global Produce Partners LLC |
| V00123 | V00123 | ABC Food Distributors Inc |

## Tensions Or Gaps
There are no notable modeling risks in this relationship, as the foreign key constraint ensures that every purchase_orders row is required to have a valid corresponding vendors entry, eliminating the possibility of orphaned purchase orders.

## Related
- [[entities/purchase_orders]]
- [[entities/vendors]]
- [[relationships/growth_opportunity_event-vendors]]
- [[relationships/po_receipts-purchase_orders]]
- [[relationships/purchase_order_lines-purchase_orders]]
- [[relationships/purchase_orders-purchase_requisitions]]
- [[relationships/purchase_orders-sites]]
- [[relationships/site_vendor_assignments-vendors]]
- [[relationships/vendor_contracts-vendors]]
- [[relationships/vendor_invoices-purchase_orders]]
- [[relationships/vendor_invoices-vendors]]
- [[relationships/vendor_performance-vendors]]
- [[relationships/vendor_pricing-vendors]]
- [[relationships/vendor_shipping_points-vendors]]
- [[relationships/overview]]
