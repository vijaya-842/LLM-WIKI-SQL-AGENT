---
title: Site vendor performance metrics
type: analysis
status: active
created: 2026-09-10
updated: 2026-09-10
source_paths:
source_count: 0
---

# Site vendor performance metrics

## Prompt
What is the performance history of vendors assigned to each site?

## Conclusion
Canonical query grounded in the current live schema — see [[erd]] for the full relationship context.

## Evidence
```sql
SELECT 
    sva.site,
    v.vendor_name,
    vp.period_month,
    vp.on_time_rate,
    vp.quality_score,
    vp.fill_rate
FROM 
    site_vendor_assignments sva
JOIN 
    vendors v ON sva.vendor_id = v.vendor_id
JOIN 
    vendor_performance vp ON v.vendor_id = vp.vendor_id;

```

Tables involved:
- [[entities/site_vendor_assignments]]
- [[entities/vendors]]
- [[entities/vendor_performance]]

## Follow-ups
None noted.

## Related
- [[index]]
- [[glossary]]
