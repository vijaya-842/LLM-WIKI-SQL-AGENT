---
title: shipment_lines → shipments (shipment_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.shipment_lines
  - live-database:public.shipments
source_count: 2
---

# shipment_lines → shipments

## Summary
Each shipments row can have zero or many shipment_lines rows attached to it; each shipment_lines row must belong to exactly one shipments. This relationship ensures that every item being shipped is associated with a specific shipment, as illustrated by the sample matches where each shipment_lines entry has a corresponding shipments record.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/shipment_lines]] |
| Source column | `shipment_id` |
| Target table | [[entities/shipments]] |
| Target column | `shipment_id` |
| Constraint | `shipment_lines_shipment_id_fkey` |
| Cardinality (shipment_lines → shipments) | many-to-one |
| Cardinality (shipments → shipment_lines) | one-to-many |
| Optionality | mandatory — shipment_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `shipment_lines.shipment_id` | `shipments.shipment_id` |

## Sample Matches
| shipment_lines.shipment_id | shipments.shipment_id | shipments.shipment_id |
|---|---|---|
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 4 | 4 |
| 5 | 5 | 5 |

## Tensions Or Gaps
There are no notable modeling risks present in this relationship, as the mandatory foreign key constraint ensures that each shipment_lines row is always linked to a valid shipments row, preventing any orphaned records.

## Related
- [[entities/shipment_lines]]
- [[entities/shipments]]
- [[relationships/shipment_lines-items]]
- [[relationships/shipments-sites]]
- [[relationships/shipments-sales_orders]]
- [[relationships/overview]]
