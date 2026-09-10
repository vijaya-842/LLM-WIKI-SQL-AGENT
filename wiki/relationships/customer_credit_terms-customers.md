---
title: customer_credit_terms → customers (customer_id)
type: concept
status: active
created: 2026-08-03
updated: 2026-08-03
source_paths:
  - live-database:public.customer_credit_terms
  - live-database:public.customers
source_count: 2
---

# customer_credit_terms → customers

## Summary
Each customers row can have exactly one customer_credit_terms row attached to it, and each customer_credit_terms row must belong to exactly one customers. This relationship ensures that the credit terms associated with each customer are mandatory and directly linked, as evidenced by the matched samples where each customer_id in customer_credit_terms corresponds to a customer in the customers table.

## Relationship Definition
| Attribute | Value |
|---|---|
| Source table | [[entities/customer_credit_terms]] |
| Source column | `customer_id` |
| Target table | [[entities/customers]] |
| Target column | `customer_id` |
| Constraint | `customer_credit_terms_customer_id_fkey` |
| Cardinality (customer_credit_terms → customers) | one-to-one |
| Cardinality (customers → customer_credit_terms) | one-to-one |
| Optionality | mandatory — customer_id is NOT NULL |

## Field Mapping
| Source Field | Target Field |
|---|---|
| `customer_credit_terms.customer_id` | `customers.customer_id` |

## Sample Matches
| customer_credit_terms.customer_id | customers.customer_id | customers.customer_name |
|---|---|---|
| C00101 | C00101 | Riverside Diner Group |
| C00102 | C00102 | Metro School District |
| C00103 | C00103 | Harborview Hotel Chain |
| C00104 | C00104 | Summit Health System |
| C00105 | C00105 | Lonestar Cafe Group |

## Tensions Or Gaps
There are no notable modeling risks present; the one-to-one relationship and non-nullable foreign key ensure that every customer has defined credit terms, eliminating the potential for orphaned records.

## Related
- [[entities/customer_credit_terms]]
- [[entities/customers]]
- [[relationships/customers-sites]]
- [[relationships/sales_orders-customers]]
- [[relationships/overview]]
