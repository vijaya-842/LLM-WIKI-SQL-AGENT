---
title: source_vendor_pricing → source_vendors (source_vendor_id)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.source_vendor_pricing
  - live-database:public.source_vendors
source_count: 2
---

# source_vendor_pricing → source_vendors

## Summary
This foreign key establishes that each source_vendor_pricing row must belong to exactly one source_vendors entity, while a single source_vendors row can have zero or many source_vendor_pricing rows attached to it. This reflects a real-world scenario where specific pricing records for items (such as SUPC-200002 for Central Supply Network) are strictly tied to a mandatory vendor definition. The samples illustrate this many-to-one dependency, showing how multiple distinct price entries link back to unique vendor identifiers like SV00567 or SV00890.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/source_vendor_pricing]] |
| Source column | `source_vendor_id` |
| Target table | [[entities/source_vendors]] |
| Target column | `source_vendor_id` |
| Constraint | `source_vendor_pricing_source_vendor_id_fkey` |
| Cardinality (source_vendor_pricing → source_vendors) | many-to-one |
| Cardinality (source_vendors → source_vendor_pricing) | one-to-many |
| Optionality | mandatory — source_vendor_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `source_vendor_pricing.source_vendor_id` | `source_vendors.source_vendor_id` |

## Sample Matches
| source_vendor_pricing.source_vendor_id | source_vendors.source_vendor_id | source_vendors.source_vendor_name |
|---|---|---|
| SV00567 | SV00567 | Central Supply Network |
| SV00890 | SV00890 | Northern Protein Co |
| SV00321 | SV00321 | Eastern Fresh Goods Ltd |
| SV00456 | SV00456 | Western Food Supply Co |
| SV00678 | SV00678 | Pacific Dairy Group |

## Tensions Or Gaps
The source column is defined as non-nullable, ensuring that no pricing record can exist without a valid parent vendor, which eliminates the risk of orphaned data in this direction. Given the clear many-to-one cardinality and mandatory linkage, there are no notable modeling risks or gaps evident from the provided schema details and sample data.

## Related
- [[entities/source_vendor_pricing]]
- [[entities/source_vendors]]
- [[relationships/source_vendor_pricing-items]]
- [[relationships/vendor_contracts-source_vendors]]
- [[relationships/overview]]
