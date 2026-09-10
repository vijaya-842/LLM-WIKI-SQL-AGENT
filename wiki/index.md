# Wiki Index

Navigation catalog. See [[overview]] for context and `log.md` for history.

## Entities
- [[entities/items]] — The `items` table serves as the master catalog for food service supply chain products, likely tracking grocery or restaurant inventory based on the sample data.
- [[entities/llm_scraped_books]] — The `llm_scraped_books` table appears to store bibliographic and commercial data for books, likely extracted from online retail sources via scraping or LLM-assisted parsing.
- [[entities/scraped_web_elements]] — This table serves as a structured repository for content extracted from web-based book catalogs, specifically capturing hierarchical page elements.
- [[entities/site_vendor_assignments]] — The `site_vendor_assignments` table manages the relationship between physical sites and their associated vendors.
- [[entities/sites]] — The `sites` table serves as a master reference for physical locations within the organization, specifically capturing distribution centers.
- [[entities/source_vendor_pricing]] — The `source_vendor_pricing` table stores the current price details for specific catalog items as supplied by various vendors.
- [[entities/source_vendors]] — The `source_vendors` table stores reference data for external supply partners, identifying them by a unique vendor ID and name.
- [[entities/users]] — The `users` table serves as the primary registry for individual user accounts within the system, identified by a unique integer `id`.
- [[entities/vendor_contracts]] — The `vendor_contracts` table tracks active and historical agreements between the organization and its external vendors.
- [[entities/vendor_performance]] — The `vendor_performance` table stores monthly KPI metrics for individual vendors, tracking delivery reliability and quality.
- [[entities/vendor_pricing]] — The `vendor_pricing` table stores historical and current price points for specific items sourced from specific vendors.
- [[entities/vendor_shipping_points]] — The `vendor_shipping_points` table defines the specific shipping destinations or locations associated with a given vendor.
- [[entities/vendors]] — The `vendors` table stores master data regarding the organization's external vendors, capturing both identity details and operational status.
- [[entities/website_content]] — The `website_content` table stores textual components of a website, likely for simple static site generation or content management.

## Relationships
- [[relationships/overview]] — schema-wide FK relationship catalog.
- [[relationships/site_vendor_assignments-sites]] — `site_vendor_assignments.site` → `sites.site`
- [[relationships/site_vendor_assignments-vendors]] — `site_vendor_assignments.vendor_id` → `vendors.vendor_id`
- [[relationships/source_vendor_pricing-items]] — `source_vendor_pricing.item_no` → `items.item_no`
- [[relationships/source_vendor_pricing-source_vendors]] — `source_vendor_pricing.source_vendor_id` → `source_vendors.source_vendor_id`
- [[relationships/vendor_contracts-source_vendors]] — `vendor_contracts.source_vendor_id` → `source_vendors.source_vendor_id`
- [[relationships/vendor_contracts-vendors]] — `vendor_contracts.vendor_id` → `vendors.vendor_id`
- [[relationships/vendor_performance-vendors]] — `vendor_performance.vendor_id` → `vendors.vendor_id`
- [[relationships/vendor_pricing-items]] — `vendor_pricing.item_no` → `items.item_no`
- [[relationships/vendor_pricing-vendors]] — `vendor_pricing.vendor_id` → `vendors.vendor_id`
- [[relationships/vendor_shipping_points-vendors]] — `vendor_shipping_points.vendor_id` → `vendors.vendor_id`

## Domains
- [[domains/vendor-management]] — Core vendor records, contractual agreements, performance metrics, and logistics information including shipping points.
- [[domains/pricing-procurement]] — Pricing data for both internal vendors and upstream source vendors, linked to inventory items.
- [[domains/site-merchant-operations]] — Definitions for retail sites or marketplaces and the assignment of vendors to specific sites.
- [[domains/product-catalog]] — Core product definitions and master data for items, including brand, size, and packaging details.
- [[domains/web-data-user-access]] — User accounts and data captured from web scraping, including structured web elements, site content, and scraped book data.

## Enums
- [[enums/active_flag]]
- [[enums/element_type]]
- [[enums/is_primary]]
- [[enums/price_unit]]
- [[enums/product_type]]
- [[enums/site]]
- [[enums/source_vendor_group]]
- [[enums/type]]
- [[enums/vendor_type]]

## Queries
- [[queries/site-vendor-contract-details]] — Site vendor contract details
- [[queries/site-vendor-performance-metrics]] — Site vendor performance metrics
- [[queries/site-vendor-pricing-snapshot]] — Site vendor pricing snapshot
- [[queries/site-vendor-shipping-addresses]] — Site vendor shipping addresses

## Reference
- [[erd]] — full schema entity-relationship diagram.
- [[glossary]] — business terms mapped to schema columns.
- [[conventions]] — naming/timestamp/soft-delete patterns observed across the schema.
