# LUMÉA project flow audit

Reviewed 10 November 2026 from a senior development and UX perspective.

## Assessment and scope

The main weakness is the gap between what the interface promises and what the system actually records. Several complete-looking screens are interactive prototypes: they report publishing, approval, delivery, authentication, or sending a message without a corresponding verified operation. The storefront and admin also use different sources of truth for products, customers, payments, promotions, and return statuses.

This review traced the storefront and admin route inventories, shared stores, customer journeys, API handlers, schemas, and persistence models. The findings below are specific code-backed issues, not a claim that every possible runtime combination was tested. No application behavior was changed.

Validation:

- Storefront and admin production builds both passed. Both report JavaScript chunk size warnings (about 777 kB and 541 kB respectively, before gzip).
- Ten isolated backend probes reproduced pricing, inventory, status, return, and review inconsistencies using disposable in-memory SQLite. See [probe results](D:/lumea/FLOW_AUDIT_PROBE_RESULTS.json) and [reproduction script](D:/lumea/audit_flow_probes.py). These invoke route handlers and validate response models; they are not HTTP integration tests. Access-control findings were established by inspecting route dependencies and application middleware.
- The existing database was not used for the probes. Real payment processing and external communications were not exercised.
- The in-app browser could not reach the locally started storefront and timed out. Pixel layout, contrast, keyboard interaction, touch targets, responsive layouts, and real bank-app handoff therefore remain unverified. This is primarily a flow and implementation audit, not a completed visual QA pass.
- Existing journey scripts and previously saved QA results are not evidence that the present implementation satisfies the acceptance criteria below.

## Flow coverage

| Journey | Current assessment | Main findings |
| --- | --- | --- |
| Home → shop/category/search → product | Catalog and detail screens can disagree; invalid detail URLs can show a real product | 5, 6, 7 |
| Brands → brand store → product | Selected brand can show SK-II inventory | 8 |
| Best sellers/new arrivals/deals → cart | Static fixtures and independent promotion rules undermine live merchandising | 5, 12 |
| Product/size/reel quick-buy → cart | Selected size is discarded; stock checks differ by entry point | 9, 10 |
| Cart → checkout → payment → confirmation | Displayed totals, payment truth, cancellation, and retries are inconsistent | 2, 3, 4, 11, 13 |
| Guest purchase → tracking/account | Tracking leads through account login; history is inferred by supplied email rather than ownership | 1, 14 |
| Register/login/social/reset → account | Demo fallbacks and simulated recovery obscure actual authentication | 15, 16 |
| Account → orders/cancel/reorder | Mixed history, fabricated detail fallback, local success after API failure, stale reorder data | 14, 17 |
| Quiz → results → routine → profile/journal | Starts partway through; answers do not determine product recommendations | 18, 19, 20 |
| Order → return wizard → tracking | Missing eligibility checks and false success paths | 21, 22, 23 |
| Admin → returns/refund | Response contracts and status vocabulary disagree; refund is only a label change | 23, 24 |
| Customer → review → moderation/video | Reviews are automatically approved and marked verified without purchase checks | 25 |
| Admin → products/brands/categories → storefront | Some edits persist, but storefront fixtures and omitted editor fields block the intended result | 5, 8, 26 |
| Admin → banners/articles/promotions → publish | Important publish/save actions modify local arrays rather than public content | 12, 27 |
| Admin → dashboard/analytics/orders/customers | Simulated metrics, ineffective filters, and payment labels mislead operators | 4, 28, 29 |
| Contact/help/policies/returns label | Help content is reachable; key support actions do not perform the promised task | 24, 30 |
| Admin → settings/backup | Some configuration persists, but backend calculations ignore it; backup excludes commerce records | 11, 30 |

## Findings, ordered by impact

### 1. Blocker — Administrative and customer boundaries are not enforced by the API

The admin router has no authentication/role dependency. Order listing, order lookup, fulfillment updates, return listing, and return updates also lack ownership enforcement. The application does not install a global authentication middleware that compensates for this. A browser login guard cannot protect these endpoints. Admin login further overwrites the returned user role with `Master Curator / Admin`.

**Why the flow fails:** an unauthenticated caller can reach customer information and operational actions; a customer account can appear to become an administrator. Order references and submitted email addresses act as access keys.

**Correction:** enforce roles and ownership in backend dependencies. Give guests a scoped, unguessable tracking credential. Separate staff fulfillment actions from customer cancellation requests.

Evidence: [admin router](D:/lumea/python-backend/app/api/admin.py:19), [orders](D:/lumea/python-backend/app/api/orders.py:117), [returns](D:/lumea/python-backend/app/api/returns.py:32), [app registration](D:/lumea/python-backend/app/main.py), [admin login](D:/lumea/admin/src/stores/auth.js:24).

### 2. Blocker — A caller can choose the purchase price

Order creation trusts `item.price` when supplied, accepts missing/unknown products through fallback values, and does not require a positive authoritative catalog price. The isolated probe purchased a catalog product priced at $50 with a submitted subtotal of $0.01.

**Correction:** accept product/variant IDs and validated quantities only; resolve price, availability, and promotions on the server. Reject missing products and malformed lines before creating an order.

Evidence: [price selection](D:/lumea/python-backend/app/api/orders.py:35), [request schema](D:/lumea/python-backend/app/schemas/order.py:5).

### 3. Blocker — Public demo approval can declare an order paid and reset its fulfillment

`simulate-approve` has no environment gate or authentication requirement. It sets payment to Paid and fulfillment to Confirmed. The probe moved a Delivered order back to Confirmed through this endpoint.

**Correction:** isolate academic simulation behind an explicit demo environment and authorized staff action. Real payment settlement must be verified server-side and must not rewind fulfillment. Repeated callbacks must be idempotent.

Evidence: [simulation endpoint](D:/lumea/python-backend/app/api/payments.py:79).

### 4. High — Card, Apple Pay, COD, and admin payment labels do not represent actual settlement

All new orders inherit `payment_status="Paid"`. Non-KHQR checkout clears the cart and opens success after order creation; the card fields never enter a gateway transaction, and Apple Pay does not invoke a wallet authorization. COD is consequently also marked Paid. Admin serialization omits payment status and its screen derives Paid from the payment method; it compares uppercase `COD` while checkout sends lowercase `cod`.

**Correction:** separate order acceptance, payment authorization, payment collection, and fulfillment. COD starts Unpaid/Collect on delivery. Expose only implemented gateways and derive every payment badge from server payment state.

Evidence: [payment default](D:/lumea/python-backend/app/models/order.py:25), [checkout standard flow](D:/lumea/frontend/src/views/checkout/CheckoutView.vue:428), [admin serializer](D:/lumea/python-backend/app/api/admin.py:111), [admin labels](D:/lumea/admin/src/views/OrdersView.vue:587).

### 5. High — Updating the real catalog does not reliably update the shop

The product store initializes `allCatalogProducts` with fixtures. A successful fetch updates `products` only. Shop and category grids filter `allCatalogProducts`, so backend edits, new products, deletions, prices, and stock can fail to appear there even while detail/search screens use API data.

**Correction:** maintain a canonical API catalog, with explicit loading, empty, and unavailable states. Keep fixtures inside a clearly separated demo mode.

Evidence: [store state/fetch](D:/lumea/frontend/src/stores/products.js:676), [shop grid](D:/lumea/frontend/src/views/shop/ShopView.vue:622), [category grid](D:/lumea/frontend/src/views/category/CategoryView.vue:550).

### 6. High — A nonexistent product URL can silently display another product

If lookup fails and no fixture slug matches, the detail store chooses the first catalog product. A deleted link can therefore look valid and offer the wrong item for purchase.

**Correction:** distinguish 404 from network failure. Show Product unavailable with a useful route back to the catalog; never substitute an unrelated purchasable item.

Evidence: [detail fallback](D:/lumea/frontend/src/stores/products.js:845).

### 7. Medium — Catalog filter contracts differ between frontend and backend

The store sends camelCase keys such as `minPrice`, `skinType`, and `skinConcern`, and brand arrays. The API expects `min_price`, `skin_type`, `skin_concern`, and a comma-separated brand string. Several advertised filters have no corresponding API parameter. Empty API results trigger fixture fallback rather than preserving a true empty result. Skin filtering in the backend also runs after pagination, allowing short/empty pages despite later matches.

**Correction:** define one filter contract, encode it explicitly, filter before pagination, and preserve zero-result states. Test the URL, visible chips, count, sort, and displayed products together.

Evidence: [request params](D:/lumea/frontend/src/stores/products.js:809), [API filters](D:/lumea/python-backend/app/api/products.py:12).

### 8. High — Brand stores can sell a different brand's products

The current brand heading follows the slug, but `displayedBestsellers` always filters for `SK-II`. Unknown slugs also fall back to SK-II, and most brand film selections fall back to the SK-II film. Admin-managed brand data is not the source of the directory used here.

**Correction:** load the selected active brand and its associated products from the backend. Missing brand stories/videos should have an honest empty state.

Evidence: [brand selection](D:/lumea/frontend/src/views/brands/BrandStoreView.vue:317), [product filter](D:/lumea/frontend/src/views/brands/BrandStoreView.vue:397).

### 9. High — Size selection is offered but discarded before fulfillment

Every product gets invented full, deluxe, and travel options with calculated prices. Cart storage drops `selectedSize`, merges lines by product ID, and checkout submits only product ID and quantity. The backend then uses the base price. Two selected sizes can merge into one line, change price, and arrive at fulfillment with no size information.

**Correction:** implement real variants with SKU, size, stock, and price throughout product → cart → order → admin → return. Until then, offer the single actual product size.

Evidence: [size generation](D:/lumea/frontend/src/views/product/ProductDetailView.vue:1303), [cart lines](D:/lumea/frontend/src/stores/cart.js:65), [checkout payload](D:/lumea/frontend/src/views/checkout/CheckoutView.vue:396).

### 10. High — Stock is advisory rather than enforced

Product cards disable adding when stock is zero, but shared cart actions and other purchase entry points do not enforce limits. Order creation checks neither availability nor requested quantity and never decrements/reserves stock. The isolated probe ordered three units of a zero-stock product successfully.

**Correction:** validate quantities at every UI entry point for feedback, then enforce and reserve inventory atomically on the server. Define release behavior for expiry, failed payment, and cancellation.

Evidence: [card behavior](D:/lumea/frontend/src/components/ProductCard.vue:93), [cart actions](D:/lumea/frontend/src/stores/cart.js:65), [order loop](D:/lumea/python-backend/app/api/orders.py:34).

### 11. High — The authorized amount can differ from the final order total

The cart grants free shipping using the pre-discount subtotal; the backend uses the post-discount subtotal. With $50 of products and 20% off, the customer sees $40 but the order total is $55. The button says “Authorize Order” using the smaller amount. Admin shipping-threshold settings affect the cart while order creation hardcodes $50/$15. A tax rate is configurable and a tax getter exists, but checkout totals do not apply it.

**Correction:** return an authoritative quote before final authorization, including discount, tax policy, delivery fee, and total. Use the same configuration service for quote and placement. Explicitly decide whether tax is included, excluded, or disabled.

Evidence: [cart calculations](D:/lumea/frontend/src/stores/cart.js:31), [backend calculations](D:/lumea/python-backend/app/api/orders.py:69), [authorize button](D:/lumea/frontend/src/views/checkout/CheckoutView.vue:315).

### 12. High — Promotions management does not control checkout discounts

Admin campaigns exist in a component-local list. Saving or deleting one does not update checkout. Both cart and backend infer discounts from whether any supplied text contains `10`, `15`, or `20`; invented `NOTREAL20` worked in the probe. Expiry, eligibility, usage caps, gift, shipping, and brand restrictions are not enforced. The two parsers also choose different precedence for a string containing both `10` and `20`.

**Correction:** persist promotions centrally and validate exact codes, dates, scope, limits, and eligibility on the server. The cart should preview the same quote the order will use.

Evidence: [admin campaign save](D:/lumea/admin/src/views/PromotionsView.vue:364), [cart parser](D:/lumea/frontend/src/stores/cart.js:112), [backend parser](D:/lumea/python-backend/app/api/orders.py:58).

### 13. High — Abandoning KHQR leaves confirmed orders; retries can create duplicates

An order is created before the QR opens. Closing cancels only the monitoring session, leaving the order intact. Submitting again creates another order rather than resuming the attempt. There is no request idempotency key. QR generation accepts an independent amount without comparing it to the order total, can reset an existing paid order to Pending, and the countdown reaching zero only stops the timer while polling continues.

**Correction:** create one pending checkout/payment attempt, bind its amount to the server quote, reuse it for retry, and implement expiry/cancellation/reconciliation. Recover late settlement without creating a duplicate order.

Evidence: [checkout initiation/cancel](D:/lumea/frontend/src/views/checkout/CheckoutView.vue:411), [QR generation](D:/lumea/python-backend/app/api/payments.py:28), [countdown](D:/lumea/frontend/src/components/checkout/KHQRModal.vue:274).

### 14. High — Order history mixes customers, demos, and fabricated records

Orders start with sample purchases under one shared localStorage key. Fetching a user's history merges it with existing records rather than replacing/scoping them; an empty result leaves old orders visible. Logout does not clear this store. Unknown order references return a fabricated Confirmed order. Backend creation does not assign the available `user_id`, relying on supplied customer email instead. Guest confirmation's tracking CTA leads to an authenticated account route, with no explicit guest claim/verification flow.

**Correction:** scope cached data by authenticated user, replace the history with authoritative results, clear private state on account change, and show genuine not-found/access-denied states. Define a guest tracking/claim flow using verified ownership.

Evidence: [history and synthetic fallback](D:/lumea/frontend/src/stores/orders.js:338), [merge](D:/lumea/frontend/src/stores/orders.js:450), [creation](D:/lumea/python-backend/app/api/orders.py:74), [tracking CTA](D:/lumea/frontend/src/views/checkout/OrderSuccessView.vue:108).

### 15. High — Backend outages appear as successful authentication

Login failures other than 400/401 and registration failures other than 400 enter a demo success fallback and generate a fake token. A server outage or some validation errors can therefore become “Welcome back” instead of a recoverable error. “Remember me” unchecked keeps auth only in memory, while route guards read localStorage, causing successful sign-in to fail protected navigation on a fresh session.

**Correction:** fail visibly on authentication/registration errors; provide a separately labeled demo action if required. Use one reactive authentication source with defined session persistence and startup validation.

Evidence: [fallbacks/persistence](D:/lumea/frontend/src/stores/auth.js:108), [route guard](D:/lumea/frontend/src/router/index.js:392).

### 16. High — Accounts inherit another person's details; social login and reset are simulated

New users receive demo addresses and saved payment methods, and guest checkout is prefilled with the demo customer's identity/address/card. Social-provider buttons log into the same demo account. Password reset reports an email sent without a reset request. Profile/address/payment edits are local only, with shared browser storage; quiz and journal entries also have no per-account namespace.

**Correction:** begin with honest empty states, load each customer's records, provide real persistence, and clear private state on logout. Implement the named authentication/recovery methods or disable them with an explicit explanation. Keep intentional guest cart persistence separate from private profile state.

Evidence: [default identity/account data](D:/lumea/frontend/src/stores/auth.js:6), [guest defaults](D:/lumea/frontend/src/views/checkout/CheckoutView.vue:376), [social/reset](D:/lumea/frontend/src/views/auth/LoginRegisterView.vue:455), [local profile save](D:/lumea/frontend/src/stores/auth.js:240), [journal storage](D:/lumea/frontend/src/stores/journal.js:5).

### 17. High — Customer tracking can change fulfillment; cancellation can falsely succeed

The account tracking modal exposes an action that advances courier status, backed by a public update endpoint. Both cancellation and progression update local state after an API failure. Transitions are arbitrary server-side strings with no payment/fulfillment guards. Reorder copies historical prices and adds each line once, dropping the original quantity; product slugs are guessed from names.

**Correction:** make customer tracking read-only, implement a guarded cancellation action with authoritative acknowledgement and payment handling, and resolve reorders against current product/variant IDs, prices, stock, and quantities.

Evidence: [customer courier action](D:/lumea/frontend/src/views/account/OrderDetailsView.vue:360), [progress/cancel/reorder](D:/lumea/frontend/src/stores/orders.js:574), [unguarded update](D:/lumea/python-backend/app/api/orders.py:129).

### 18. High — “Start Skin Quiz” begins at question three

The questions view initializes `currentStep` to 3 to match a mockup. The store starts with filled answers and `completed=true`; `initialData?.completed || true` also turns a saved false value back into true. Starting or retaking uses a route link rather than resetting or explicitly resuming a session. Next-step navigation does not validate required answers.

**Correction:** distinguish Start, Resume, and Retake. Begin new quizzes at step one with empty answers; reset on retake, validate each required step, and gate results on completion.

Evidence: [initial step](D:/lumea/frontend/src/views/quiz/SkinQuizQuestionsView.vue:393), [initial profile](D:/lumea/frontend/src/stores/quiz.js:13), [next step](D:/lumea/frontend/src/views/quiz/SkinQuizQuestionsView.vue:555).

### 19. High — “Personalized” recommendations do not depend on answers or admin rules

The routine and submitted recommended IDs are fixed. Skin type, concerns, preferences, and desired routine size do not select different products. The view fetches an active quiz, but still renders hardcoded steps/options; completion only increments a counter in the backend. Pausing all quizzes can still return the first quiz as the active fallback.

**Correction:** define a recommendation engine using the published quiz version, validated answers, product attributes, availability, and desired routine size. Preserve the result with the user profile and explain why each item was selected. Respect the absence of an active quiz.

Evidence: [fixed routine/IDs](D:/lumea/frontend/src/stores/quiz.js:92), [hardcoded questions](D:/lumea/frontend/src/views/quiz/SkinQuizQuestionsView.vue:57), [active fallback/completion](D:/lumea/python-backend/app/api/quizzes.py:25).

### 20. Medium — Saved skin profile/journal promises exceed persistence

Profile and journal data live in browser storage with sample starting content. A new customer can see a pre-existing diagnostic and diary; account switching can retain it, while another device has none of the edits. This is especially confusing beside authenticated account pages that imply account-owned records.

**Correction:** persist these records under the authenticated user, use empty onboarding states, and disclose any intentionally local-only feature. Handle malformed storage without breaking account pages.

Evidence: [quiz persistence](D:/lumea/frontend/src/stores/quiz.js:7), [journal state](D:/lumea/frontend/src/stores/journal.js:5), [local profile update](D:/lumea/frontend/src/stores/auth.js:240).

### 21. High — Failed return submission opens an approved sample return

Both HTTP failure and exceptions redirect to `RR24081234`. The status screen begins with sample Approved data and keeps it when lookup fails. Submission also hardcodes the demo customer and attaches sample evidence by default.

**Correction:** preserve the draft, show the actual error, and allow retry. Navigate only after a real request is created. Status pages must show loading, not-found, access-denied, and unavailable states rather than sample approvals.

Evidence: [submission fallback/identity](D:/lumea/frontend/src/views/returns/ReturnRequestView.vue:518), [status defaults](D:/lumea/frontend/src/views/returns/ReturnStatusView.vue:220).

### 22. High — Returns do not establish eligibility or tie amounts to a purchase

The wizard offers all cached orders, with no delivered/window/remaining-quantity filtering. The server does not look up the order or purchased item, verify ownership, calculate refundable amount, or prevent repeated returns. The probe successfully requested $999 against a nonexistent order. The wizard always submits quantity one.

**Correction:** select eligible order-line IDs, enforce policy and previously returned quantities on the server, and compute refundable value from the original paid line. Give explicit reasons for ineligible items and allow valid partial quantities.

Evidence: [wizard selection](D:/lumea/frontend/src/views/returns/ReturnRequestView.vue:379), [return creation](D:/lumea/python-backend/app/api/returns.py:70), [return schema](D:/lumea/python-backend/app/schemas/return_request.py:5).

### 23. High — Admin return updates and customer timelines disagree

Admin create/update handlers test `res.data.success`, but those endpoints return a plain return object without that field. The database can update while the admin UI stays unchanged, encouraging retries. Admin tabs use Pending/Refunded while the API creates Under Review and the timeline ends with Refund Completed. Changing `status` does not derive timeline/current_step. The probe produced Refunded with step two still active.

**Correction:** share a typed response contract and canonical status enum. Make allowed transitions update status, event history, and derived timeline together. Base UI success on the actual agreed response.

Evidence: [admin update](D:/lumea/admin/src/views/ReturnsView.vue:147), [API transition](D:/lumea/python-backend/app/api/returns.py:117), [response model](D:/lumea/python-backend/app/schemas/return_request.py:25).

### 24. High — Refund, replacement, credit, and shipping-label actions are not coherent

“Replacement (same product)” describes store credit, while “Exchange” promises an immediate replacement. All resolutions use the same refund timeline. Admin marking a return Refunded only changes a string; there is no linked money movement, credit ledger, or replacement shipment. Download return label only opens an alert.

**Correction:** define distinct refund, replacement, and store-credit workflows. Derive the correct next action and timeline for each; generate a real label or provide manual return instructions. A manual refund must be explicitly recorded with evidence and reference rather than implying an integrated bank refund.

Evidence: [resolution options](D:/lumea/frontend/src/views/returns/ReturnRequestView.vue:442), [label action](D:/lumea/frontend/src/views/returns/ReturnStatusView.vue:263), [status-only endpoint](D:/lumea/python-backend/app/api/returns.py:138).

### 25. High — Reviews are called verified and moderated without either check

Anonymous submissions are assigned `verified_purchase=True` and immediately approved. A missing product can still receive a review under a generic name. Helpful votes can be repeated without identity/deduplication. This undermines the trust signals and the admin moderation workflow.

**Correction:** derive verification from the authenticated purchaser and order line, require an existing product, use the intended moderation state, and deduplicate helpful votes. Display authentic rating/count aggregates consistently across cards and detail pages.

Evidence: [review creation](D:/lumea/python-backend/app/api/reviews.py:91), [helpful action](D:/lumea/python-backend/app/api/reviews.py:132).

### 26. High — Product editor exposes fields it does not save and changes unrelated state

The save payload omits the selected skin types, concerns, subcategory, and secondary images. Backend product DTOs omit these attributes too. Every save sends `is_featured:false`, so editing another field can remove a featured product. Creating a zero-stock product uses `payload.stock or 20`, replacing zero with 20. Category reorder only shows a success toast.

**Correction:** align editor, DTO, model, and returned product fields; preserve fields the operator did not change. Treat zero as a valid value. Persist category ordering and visibility or remove the unsupported controls.

Evidence: [product payload](D:/lumea/admin/src/views/ProductsView.vue:298), [product DTOs](D:/lumea/python-backend/app/api/admin.py:25), [stock default](D:/lumea/python-backend/app/api/admin.py:306), [category reorder](D:/lumea/admin/src/views/CategoriesView.vue:194).

### 27. High — CMS publish buttons do not publish the content

Banner save/toggle/publish only modify component state and a displayed timestamp. Article draft/publish modifies a local form/list, without writing the article body to the available backend. A refresh loses changes; the storefront never receives the advertised publication. The Article model also has no draft/scheduled/archived status to support the editor's lifecycle.

**Correction:** persist full content and publication state, return the stored version, and verify the public endpoint before reporting published. Distinguish Save draft, Preview, Publish, Unpublish, and Schedule with unsaved-change handling.

Evidence: [banner actions](D:/lumea/admin/src/views/BannersView.vue:176), [article actions](D:/lumea/admin/src/views/ArticlesView.vue:417), [article model](D:/lumea/python-backend/app/models/article.py:5).

### 28. Medium — Operational metrics fabricate activity and misstate revenue

Order/return counts use `actualCount || sampleCount`, turning real zero values into invented activity. Revenue sums all non-cancelled orders without testing payment collection, and the backend daily chart distributes the aggregate using a formula instead of grouping transactions by date. Average order value uses a different population in numerator and denominator. These displays cannot support business decisions.

**Correction:** show valid zero/empty/error states; define paid revenue versus order value and report them separately. Group real events by date/timezone and apply one explicit population and date range per metric.

Evidence: [return counts](D:/lumea/admin/src/views/ReturnsView.vue:118), [order counts](D:/lumea/admin/src/views/OrdersView.vue:160), [revenue/chart](D:/lumea/python-backend/app/api/admin.py:151).

### 29. Medium — Admin filters appear functional but do not affect the result set

Orders has payment, delivery, and date controls, but `filteredOrders` applies only tab, search, and order-status filtering. Returns declares a date filter but does not apply it; its Pending tab also misses the actual Under Review status. This can hide work or leave staff believing the displayed list meets a selection it does not.

**Correction:** implement each visible filter against real data, make selected criteria explicit, reset pagination after filtering, and distinguish zero matches from loading failure. Remove decorative controls until implemented.

Evidence: [order filtering](D:/lumea/admin/src/views/OrdersView.vue:133), [return filtering](D:/lumea/admin/src/views/ReturnsView.vue:83).

### 30. Medium — Support and maintenance actions promise outcomes they do not deliver

Contact submission only toggles a success state and then erases the message; there is no send request. Order “write review” only shows a toast rather than opening a form. Several customer/admin actions and exports only show alerts. “Store database backup” exports settings and metadata, without orders, customers, inventory, or uploaded assets. The public footer's admin link is hardcoded to localhost, which points visitors to their own computer after deployment.

**Correction:** wire supported actions end-to-end with useful confirmation/reference numbers. Preserve input on failure. Disable incomplete actions explicitly. Rename the settings export accurately or implement a real restorable backup. Configure deployment URLs rather than embedding localhost in public navigation.

Evidence: [contact action](D:/lumea/frontend/src/views/contact/ContactView.vue:273), [order review action](D:/lumea/frontend/src/views/account/OrderDetailsView.vue:443), [backup](D:/lumea/admin/src/views/SettingsView.vue:179), [footer link](D:/lumea/frontend/src/components/Footer.vue:73).

## Recommended coherent flows

### Purchase and fulfillment

Browse live catalog → choose a real available variant → add quantity → receive authoritative server quote → enter/confirm delivery details → create one pending checkout attempt → authorize payment or choose COD → record verified payment state → create/confirm fulfillment → display confirmation with the correct payment wording → read-only tracking.

Use separate payment states (Unpaid, Pending, Authorized where supported, Paid, Failed, Expired, Partially Refunded, Refunded) and fulfillment states (Unfulfilled/Confirmed, Processing, Shipped, Out for Delivery, Delivered, Cancelled). Specify allowed transitions and who can perform each. COD may proceed to fulfillment while remaining uncollected; online payment usually requires verified authorization/collection according to the chosen policy.

### Returns and refunds

Verify ownership → choose eligible purchased lines and quantities → calculate refundable amount → choose reason and a supported resolution → submit once → review → approve/reject with explanation → provide label/instructions if physical return is required → receive/inspect if applicable → perform and reconcile refund, credit, or replacement → confirm the actual resolution. Some missing/damaged-item cases may need a branch that does not require shipping an item back.

### Personalization

Start a new quiz or resume a saved one → answer validated questions from a published quiz version → calculate an explainable result → select in-stock products using the answers and desired routine size → show AM/PM steps and current prices → optionally save to the authenticated account → add actual variant IDs to the bag. Retake should ask for a new result without silently treating sample answers as the user's answers.

### Administration and publishing

Authenticate as authorized staff → load real records → edit with accurate field values → validate → save on the server → show acknowledgement → preview the stored draft → publish a version → verify the storefront consumes that version. Leaving with unsaved changes should preserve or explicitly discard them.

## Suggested implementation order

1. **Protect data and money:** findings 1–4; remove false payment/auth success paths and isolate demo mode.
2. **Establish transaction truth:** findings 5, 9–14, 17; canonical products, variants, stock, quotes, identities, states, and idempotent checkout.
3. **Repair after-sales operations:** findings 21–25; eligible returns, matching contracts, honest timelines, actual resolution, and verified reviews.
4. **Make admin controls real:** findings 12, 26–29; persisted campaigns/content, complete editor contracts, accurate metrics, and working filters.
5. **Complete onboarding and assistance:** findings 6–8, 15–20, 30; honest empty/error states, account persistence, personalization, recovery, and support.

## Acceptance scenarios before declaring the project complete

- A new account starts with zero orders and no borrowed address, payment method, quiz result, or diary. Switching accounts exposes none of the previous customer's private records.
- Login/register with the backend unavailable stays signed out and retains the form. Unchecking Remember me still allows protected navigation during the active session.
- A customer token cannot call staff actions; anonymous users cannot list private orders/returns or mutate fulfillment; guest tracking requires an appropriate scoped credential.
- Creating/editing/deleting a product in admin changes shop, category, search, detail, and quick-buy consistently. An unknown slug shows unavailable, never a different product.
- Two variants remain separate lines through cart, checkout, invoice, fulfillment, reorder, and return. No invented variant is offered.
- Displayed and charged totals match across threshold crossings, promotions, shipping configuration, and the chosen tax policy. Caller-supplied prices do not change the authoritative quote.
- Concurrent purchases cannot oversell. Unpaid expiry/cancellation releases reservations according to policy.
- Card/wallet success requires gateway confirmation; COD is visibly uncollected; simulation is unavailable outside its intended demo environment.
- Cancelling, expiring, reloading, or retrying QR checkout does not create duplicate fulfillable orders, reset paid state, or change the order amount. Late confirmations reconcile safely.
- Failed cancellation/return submission remains an error with input preserved. Invalid references never display synthetic confirmations or approved sample returns.
- A non-eligible or nonexistent order cannot be returned; partial returns are bounded by purchased/previously returned quantities. Each resolution follows its own valid timeline.
- Admin return changes update the list and customer timeline immediately from the acknowledged server response. Refunded means a recorded completed refund or explicitly evidenced manual resolution.
- Starting and retaking the quiz begin correctly. Different materially relevant answers produce explainably different recommendations, and paused quizzes are not offered.
- Publishing a campaign, banner, or article survives refresh and changes the intended public content; drafts remain private. Zero metrics remain zero and filters truly constrain rows.
- Contact submission creates a real support record or sends through the implemented channel. Downloads contain the promised content, and a backup can be restored in a disposable environment.
- Perform a separate desktop/mobile visual and keyboard QA pass once the browser can reach the services. In particular check checkout/QR on a phone, form errors, modal focus, navigation back/forward, 404s, empty states, and long content.
