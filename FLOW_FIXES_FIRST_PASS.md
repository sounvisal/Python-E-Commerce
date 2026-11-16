# Selected flow fixes — 10 November 2026

Implemented the seven areas selected from the audit:

- Order prices and names resolve from database products. Missing products, invalid quantities, insufficient listed stock, and invented coupon codes are rejected. Order creation requires the displayed expected total; a changed quote requires customer review. Order and lines save in one transaction.
- New KHQR orders await payment; COD remains Unpaid. Unimplemented card and Apple Pay checkout are disabled and rejected by the API. Admin/customer payment labels use payment state. Demo approval is disabled by default and requires an authenticated administrator when explicitly enabled. Paid orders cannot be regenerated as Pending or rewound by simulation. QR amounts must equal the stored total.
- Storefront catalog grids, home bestsellers, deal product lists, and brand product lists use fetched products. Empty responses stay empty; missing product URLs no longer substitute another product. Catalog loads on app mount and the shop refreshes it on entry.
- Removed invented deluxe/travel variants. Products currently offer their single standard size, so checkout cannot silently discard a different selected size. Real multi-SKU variants remain a separate feature requiring inventory/schema support.
- Backend and frontend use the same pre-discount free-shipping threshold, configurable threshold value, standard fee, and exact supported coupon codes. Checkout verifies a server quote before submitting. Prices are treated as tax-inclusive; no extra tax is added.
- Return submission requires authentication, a delivered/paid order belonging to that customer, a purchased line, a valid return window, and remaining returnable quantity. Refund unit value comes from the original discounted purchase. Only the supported refund resolution is offered. Failed submissions retain input and display errors. Status lookup has loading/error states with no sample-approved fallback. Return pages require login and load the customer's orders before offering items.
- Fresh/retaken quizzes begin at question one with empty answers. Required steps validate answers; formulation preferences are optional. Result/routine routes require completion. Recommendations select distinct in-stock live catalog products using skin type, concerns, goals, and routine length; morning/evening differ. Results show actual selected concerns/goals and disclose the limits of the matching rules.

Validation completed:

- 14 backend regression tests in `test_flow_regressions.py`, using disposable in-memory SQLite.
- 5 recommendation regression tests in `test_recommendations.mjs`.
- Storefront and admin production builds passed; existing bundle-size warnings remain.
- Python application modules compile.

Limits and follow-up:

- Live bank settlement, browser journeys, and mobile layouts were not verified. Existing payment records were not reclassified; previously incorrect Paid values require an evidence-based reconciliation.
- Return eligibility currently uses 30 days from purchase because the order model has no delivered-at timestamp. The UI states this rule. Delivery-based policy needs an actual recorded delivery event before it can be applied accurately.
- Recommendations are deterministic catalog-attribute suggestions, not an ingredient-verification engine; formulation preferences, lifestyle, and environment do not yet determine verified product eligibility. The admin quiz editor is still a separate follow-up from the wider audit.
- Real variant inventory, payment-attempt idempotency/expiry, inventory reservation across concurrent orders, comprehensive role/ownership enforcement, persisted campaign management, and the other unselected audit findings remain outstanding. Do not interpret this change as a production-readiness sign-off.
- `PROJECT_FLOW_AUDIT.md` and its probe results are the original audit snapshot. Its demonstration script intentionally reproduced the old bugs and is superseded for validation by the regression tests above.
