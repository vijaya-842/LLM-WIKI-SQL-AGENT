---
title: Site vendor pricing snapshot
type: analysis
status: active
created: 2026-09-10
updated: 2026-09-10
source_paths:
source_count: 0
---

# Site vendor pricing snapshot

## Prompt
What prices do site-assigned vendors offer for their items?

## Conclusion
Canonical query grounded in the current live schema — see [[erd]] for the full relationship context.

## Evidence
```sql
SELECT 
    sva.site,
    v.vendor_name,
    vp.item_no,
    vp.vendor_price,
    vp.price_unit,
    vp.price_effective_date
FROM 
    site_vendor_assignments sva
JOIN 
    vendors v ON sva.vendor_id = v.vendor_id
JOIN 
    vendor_pricing vp ON v.vendor_id = vp.vendor_id;

```

Tables involved:
- [[entities/site_vendor_assignments]]
- [[entities/vendors]]
- [[entities/vendor_pricing]]

## Follow-ups
None noted.

## Related
- [[index]]
- [[glossary]]
