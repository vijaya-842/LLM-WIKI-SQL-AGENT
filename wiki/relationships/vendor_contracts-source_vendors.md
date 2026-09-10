---
title: vendor_contracts → source_vendors (source_vendor_id)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.vendor_contracts
  - live-database:public.source_vendors
source_count: 2
---

# vendor_contracts → source_vendors

## Summary
This foreign key establishes a many-to-one relationship where each vendor_contracts row has an optional link to a source_vendors row, meaning a contract may or may not have an associated master vendor record. From the perspective of the source table, each source_vendors row can have zero or many vendor_contracts rows attached to it. The sample data illustrates this by showing specific contracts (e.g., contract_id 1 involving "V00234") linked to distinct master vendor profiles such as "Central Supply Network" (SV00567).

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/vendor_contracts]] |
| Source column | `source_vendor_id` |
| Target table | [[entities/source_vendors]] |
| Target column | `source_vendor_id` |
| Constraint | `vendor_contracts_source_vendor_id_fkey` |
| Cardinality (vendor_contracts → source_vendors) | many-to-one |
| Cardinality (source_vendors → vendor_contracts) | one-to-many |
| Optionality | optional — source_vendor_id is nullable |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `vendor_contracts.source_vendor_id` | `source_vendors.source_vendor_id` |

## Sample Matches
| vendor_contracts.source_vendor_id | source_vendors.source_vendor_id | source_vendors.source_vendor_name |
|---|---|---|
| SV00567 | SV00567 | Central Supply Network |
| SV00890 | SV00890 | Northern Protein Co |
| SV00321 | SV00321 | Eastern Fresh Goods Ltd |
| SV00456 | SV00456 | Western Food Supply Co |
| SV00678 | SV00678 | Pacific Dairy Group |

## Tensions Or Gaps
Because the foreign key is nullable, vendor_contracts rows are permitted to exist without a corresponding source_vendors entry, which introduces the risk of orphaned contract records if the link is not considered mandatory by the business process. This design choice suggests that some contracts may originate from internal sources or other vendor tables not represented by the source_vendors entity.

## Related
- [[entities/vendor_contracts]]
- [[entities/source_vendors]]
- [[relationships/source_vendor_pricing-source_vendors]]
- [[relationships/vendor_contracts-vendors]]
- [[relationships/overview]]
