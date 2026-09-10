---
title: Site vendor contract details
type: analysis
status: active
created: 2026-09-10
updated: 2026-09-10
source_paths:
source_count: 0
---

# Site vendor contract details

## Prompt
What are the contract details for vendors assigned to each site?

## Conclusion
Canonical query grounded in the current live schema — see [[erd]] for the full relationship context.

## Evidence
```sql
SELECT 
    sva.site,
    v.vendor_name,
    vc.contract_id,
    vc.contract_start,
    vc.contract_end,
    vc.payment_terms
FROM 
    site_vendor_assignments sva
JOIN 
    vendors v ON sva.vendor_id = v.vendor_id
JOIN 
    vendor_contracts vc ON v.vendor_id = vc.vendor_id;

```

Tables involved:
- [[entities/site_vendor_assignments]]
- [[entities/vendors]]
- [[entities/vendor_contracts]]

## Follow-ups
None noted.

## Related
- [[index]]
- [[glossary]]
