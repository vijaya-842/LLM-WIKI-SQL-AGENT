---
title: site_vendor_assignments → sites (site)
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
  - live-database:public.site_vendor_assignments
  - live-database:public.sites
source_count: 2
---

# site_vendor_assignments → sites

## Summary
This foreign key establishes a mandatory many-to-one relationship where each `site_vendor_assignments` row must belong to exactly one `sites` record, representing a specific vendor assignment to a distinct distribution center. Conversely, each `sites` row can have zero or many `site_vendor_assignments` rows attached to it, allowing a single facility to host multiple vendor relationships. The sample data confirms that these assignments are linked to specific sites identified by codes like "0091" and "0055" across various regions.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/site_vendor_assignments]] |
| Source column | `site` |
| Target table | [[entities/sites]] |
| Target column | `site` |
| Constraint | `site_vendor_assignments_site_fkey` |
| Cardinality (site_vendor_assignments → sites) | many-to-one |
| Cardinality (sites → site_vendor_assignments) | one-to-many |
| Optionality | mandatory — site is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `site_vendor_assignments.site` | `sites.site` |

## Sample Matches
| site_vendor_assignments.site | sites.site | sites.site_name |
|---|---|---|
| 0091 | 0091 | Site 0091 - Distribution Center |
| 0055 | 0055 | Site 0055 - Distribution Center |
| 0019 | 0019 | Site 0019 - Distribution Center |
| 0078 | 0078 | Site 0078 - Distribution Center |
| 0042 | 0042 | Site 0042 - Distribution Center |

## Tensions Or Gaps
The tight coupling is reinforced by the non-nullable constraint on the source column, ensuring no orphaned assignment records exist by design. No notable modeling risks, such as optional relationships or ambiguous cardinalities, are present in this configuration.

## Related
- [[entities/site_vendor_assignments]]
- [[entities/sites]]
- [[relationships/site_vendor_assignments-vendors]]
- [[relationships/overview]]
