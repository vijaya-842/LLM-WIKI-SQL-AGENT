---
title: vendor_pricing → items (item_no)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.vendor_pricing
  - live-database:public.items
source_count: 2
---

# vendor_pricing → items

## Summary
Each `vendor_pricing` row must link to exactly one `items` record, while each `items` row can be associated with zero or many `vendor_pricing` rows, reflecting a mandatory many-to-one relationship. This structure supports the business logic where a single supply catalog item, such as "FRESH ROMAINE LETTUCE 24CT," has multiple distinct vendor price points (e.g., from vendors V00234 and V00345) tracked over time.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_pricing]] |
| Source column | `item_no` |
| Target table | [[entities/items]] |
| Target column | `item_no` |
| Constraint | `vendor_pricing_item_no_fkey` |
| Cardinality (vendor_pricing → items) | many-to-one |
| Cardinality (items → vendor_pricing) | one-to-many |
| Optionality | mandatory — item_no is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_pricing.item_no` | `items.item_no` |

## Sample Matches
| vendor_pricing.item_no | items.item_no | items.item_desc |
|---|---|---|
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-200002 | SUPC-200002 | FRESH ROMAINE LETTUCE 24CT |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-400004 | SUPC-400004 | BEEF GROUND 80/20 10LB CHUB |
| SUPC-100001 | SUPC-100001 | FROZEN CHICKEN BREAST 4OZ |

## Tensions Or Gaps
The relationship is modeled with appropriate integrity, as the non-nullable foreign key prevents orphaned pricing records while correctly capturing the one-to-many reality that a single item receives pricing from various vendors. There are no notable modeling risks or gaps evident in this specific constraint definition.

## Related
- [[entities/vendor_pricing]]
- [[entities/items]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_pricing-vendors]]
- [[relationships/overview]]
