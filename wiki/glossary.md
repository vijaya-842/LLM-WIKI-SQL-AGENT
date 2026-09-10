---
title: Glossary
type: concept
status: active
created: 2026-07-31
updated: 2026-09-10
source_paths:
source_count: 0
---

# Glossary

## Summary
Business terms mapped to their schema representation, aggregated from column descriptions across all 14 entity pages.

## Evidence
| Column | Tables | Description |
|---|---|---|
| `active_flag` | [[entities/vendors]] | Boolean indicator showing whether the vendor is currently active or inactive in the system. |
| `assigned_date` | [[entities/site_vendor_assignments]] | Date when the vendor was assigned to the site. |
| `availability` | [[entities/llm_scraped_books]] | Inventory status indicating stock presence and available quantity. |
| `brand` | [[entities/items]] | Name of the supplier or manufacturer for the item. |
| `content` | [[entities/website_content]] | The actual text data associated with the specific content type. |
| `contract_end` | [[entities/vendor_contracts]] | Date when this vendor contract expires or is terminated. |
| `contract_id` | [[entities/vendor_contracts]] | Unique identifier for the vendor contract record. |
| `contract_start` | [[entities/vendor_contracts]] | Date when this vendor contract became active. |
| `created_timestamp` | [[entities/source_vendors]], [[entities/vendors]] | Date and time the vendor record was created in the system. |
| `element_type` | [[entities/scraped_web_elements]] | The category of the scraped element, such as text or image_url. |
| `email` | [[entities/users]] | The unique email address used for authentication and communication. |
| `fill_rate` | [[entities/vendor_performance]] | Percentage of requested order quantity successfully fulfilled by the vendor. |
| `id` | [[entities/users]] | Unique auto-generated integer identifier for each user record in the system. |
| `is_primary` | [[entities/site_vendor_assignments]] | Flag indicating if this vendor is the main assigned partner. |
| `item_desc` | [[entities/items]] | Human-readable description of the product details. |
| `item_no` | [[entities/items]], [[entities/source_vendor_pricing]], [[entities/vendor_pricing]] | Unique identifier for the inventory item or product. |
| `item_size` | [[entities/items]] | Unit size or quantity specification of the product. |
| `market` | [[entities/sites]] | Specific local market or city associated with the site's operations. |
| `name` | [[entities/users]] | The user's full display name, such as first and last name. |
| `on_time_rate` | [[entities/vendor_performance]] | Percentage of orders delivered on or before the promised date. |
| `onboarded_date` | [[entities/vendors]] | The specific date the vendor was first registered and approved in the system. |
| `pack` | [[entities/items]] | Number of units per pack for inventory tracking. |
| `parent_section` | [[entities/scraped_web_elements]] | The logical section or area of the page from which the element originates. |
| `payment_terms` | [[entities/vendor_contracts]] | Invoice payment schedule and terms agreed upon with the vendor. |
| `period_month` | [[entities/vendor_performance]] | Specific month for which the vendor performance metrics are reported. |
| `price` | [[entities/llm_scraped_books]] | The current selling cost of the item, including currency symbol. |
| `price_effective_date` | [[entities/source_vendor_pricing]], [[entities/vendor_pricing]] | Calendar date when this specific price agreement applies to orders. |
| `price_unit` | [[entities/source_vendor_pricing]], [[entities/vendor_pricing]] | Measurement or packaging basis (e.g., Case) for the quoted price. |
| `pricing_id` | [[entities/source_vendor_pricing]], [[entities/vendor_pricing]] | Unique system-generated identifier for each specific vendor pricing record. |
| `primary_content` | [[entities/scraped_web_elements]] | The main extracted data, such as a title, description, or direct image URL. |
| `quality_score` | [[entities/vendor_performance]] | Measure of product quality based on defect rates or inspections. |
| `region` | [[entities/sites]], [[entities/source_vendors]] | Broad geographic area designation where the site is located. |
| `secondary_content` | [[entities/scraped_web_elements]] | Supplementary information associated with the element, like an image caption or 'N/A'. |
| `ship_point` | [[entities/vendor_shipping_points]] | Code identifying a specific shipping location or dock. |
| `ship_point_address` | [[entities/vendor_shipping_points]] | Physical address or description of the shipping point. |
| `site` | [[entities/site_vendor_assignments]], [[entities/sites]] | Unique code identifying the specific business location or branch. |
| `site_name` | [[entities/sites]] | Human-readable description of the site, including its function or type. |
| `source_price` | [[entities/source_vendor_pricing]] | Unit price charged by the vendor for the specified item. |
| `source_vendor_group` | [[entities/source_vendors]] | Categorical grouping assigned to the vendor for organizational management. |
| `source_vendor_id` | [[entities/source_vendor_pricing]], [[entities/source_vendors]], [[entities/vendor_contracts]] | Primary key reference to the supplier providing this item quotation. |
| `source_vendor_name` | [[entities/source_vendors]] | The official business name of the source vendor. |
| `title` | [[entities/llm_scraped_books]] | The full name or heading of the book product. |
| `type` | [[entities/website_content]] | Categorical label indicating the HTML element or content format of the row. |
| `upc` | [[entities/llm_scraped_books]] | Unique identifier code for the specific book product. |
| `vendor_id` | [[entities/site_vendor_assignments]], [[entities/vendor_contracts]], [[entities/vendor_performance]], [[entities/vendor_pricing]], [[entities/vendor_shipping_points]], [[entities/vendors]] | Unique identifier for the service provider assigned to the site. |
| `vendor_name` | [[entities/vendors]] | The full legal or trading name of the vendor entity. |
| `vendor_price` | [[entities/vendor_pricing]] | The monetary amount charged by the vendor for the specified product unit. |
| `vendor_type` | [[entities/vendors]] | Categorizes the vendor relationship, such as Primary or Secondary, for reporting purposes. |

## Tensions Or Gaps
Where a column name is reused across tables, the description shown is from its first occurrence; wording may vary slightly per table — see the individual entity page for the exact text. See [[enums]] pages for columns whose valid values are also documented.

## Related
- [[index]]
- [[conventions]]
