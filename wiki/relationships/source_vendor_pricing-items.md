---
title: source_vendor_pricing → items (item_no)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.source_vendor_pricing
  - live-database:public.items
source_count: 2
---

# source_vendor_pricing → items

## Summary
Each `source_vendor_pricing` row must belong to exactly one `items` row, establishing that every vendor price record is tied to a specific product catalog entry, such as linking a price for "FRESH ROMAINE LETTUCE 24CT" to its item number. This many-to-one relationship allows a single `items` row to have zero or many `source_vendor_pricing` rows attached to it, reflecting that various vendors can supply pricing for the same item.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/source_vendor_pricing]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `source_vendor_pricing_item_no_fkey` |
| Cardinality (source_vendor_pricing → items) | many-to-one |
| Cardinality (items → source_vendor_pricing) | one-to-many |
| Optionality | mandatory — item_no is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `source_vendor_pricing.item_no` | `items.item_no` |

## Sample Matches
| source_vendor_pricing.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |
| SUPC-500005 | SUPC-500005 | SHREDDED MOZZARELLA CHEESE 5LB |
| SUPC-300003 | SUPC-300003 | CANOLA OIL 35LB JUG |

## Tensions Or Gaps
The schema enforces a mandatory link via a non-nullable foreign key, meaning `source_vendor_pricing` rows cannot exist without a corresponding `items` record, thereby preventing orphaned pricing data but creating a dependency that requires the `items` table to be populated before pricing records can be inserted.

## Related
- [[entities/source_vendor_pricing]]
- [[entities/items]]
- [[relationships/source_vendor_pricing-source_vendors]]
- [[relationships/vendor_pricing-items]]
- [[relationships/overview]]
