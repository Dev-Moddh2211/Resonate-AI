# PII handling

The pipeline detects obvious emails, phone numbers, and `Name:`/`Customer:` labels. Matches are recorded as findings and replaced with typed markers before chunks are indexed. The synthetic form demonstrates this path; no real customer information is included. Detection is intentionally conservative and is not a compliance certification.
