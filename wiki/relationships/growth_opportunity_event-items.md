---
title: growth_opportunity_event → items (item_no)
type: concept
status: active
created: 2026-07-31
updated: 2026-08-03
source_paths:
  - live-database:public.growth_opportunity_event
  - live-database:public.items
source_count: 2
---

# growth_opportunity_event → items

## Summary
Each items row can have zero or many growth_opportunity_event rows attached to it; each growth_opportunity_event row must belong to exactly one items. This relationship facilitates linking specific growth opportunity events to their respective items, allowing for better tracking of product management and vendor interactions, as illustrated by the sample matches.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/growth_opportunity_event]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `fk_goe_item_no` |
| Cardinality (growth_opportunity_event → items) | many-to-one |
| Cardinality (items → growth_opportunity_event) | one-to-many |
| Optionality | optional — item_no is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `growth_opportunity_event.item_no` | `items.item_no` |

## Sample Matches
| growth_opportunity_event.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-300003 | SUPC-300003 | CANOLA OIL 35LB JUG |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-500005 | SUPC-500005 | SHREDDED MOZZARELLA CHEESE 5LB |

## Tensions Or Gaps
The nullable foreign key on growth_opportunity_event.item_no introduces the possibility that some growth_opportunity_event rows may not be associated with any items, potentially leading to orphaned records by design. There are no other notable modeling risks identified.

## Related
- [[entities/growth_opportunity_event]]
- [[entities/items]]
- [[relationships/growth_opportunity_event-sites]]
- [[relationships/growth_opportunity_event-vendors]]
- [[relationships/growth_opportunity_event-source_vendors]]
- [[relationships/po_receipt_lines-items]]
- [[relationships/purchase_order_lines-items]]
- [[relationships/purchase_requisition_lines-items]]
- [[relationships/sales_invoice_lines-items]]
- [[relationships/sales_order_lines-items]]
- [[relationships/sales_return_lines-items]]
- [[relationships/shipment_lines-items]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_invoice_lines-items]]
- [[relationships/vendor_pricing-items]]
- [[relationships/overview]]
