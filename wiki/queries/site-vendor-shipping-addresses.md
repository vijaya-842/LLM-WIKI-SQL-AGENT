---
title: Site vendor shipping addresses
type: analysis
status: active
created: 2026-09-10
updated: 2026-09-10
source_paths:
source_count: 0
---

# Site vendor shipping addresses

## Prompt
Where do site-assigned vendors ship from?

## Conclusion
Canonical query grounded in the current live schema — see [[erd]] for the full relationship context.

## Evidence
```sql
SELECT 
    sva.site,
    v.vendor_name,
    vsp.ship_point,
    vsp.ship_point_address
FROM 
    site_vendor_assignments sva
JOIN 
    vendors v ON sva.vendor_id = v.vendor_id
JOIN 
    vendor_shipping_points vsp ON v.vendor_id = vsp.vendor_id;

```

Tables involved:
- [[entities/site_vendor_assignments]]
- [[entities/vendors]]
- [[entities/vendor_shipping_points]]

## Follow-ups
None noted.

## Related
- [[index]]
- [[glossary]]
