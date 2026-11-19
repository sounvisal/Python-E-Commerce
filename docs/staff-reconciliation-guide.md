# Luméa Atelier — Staff Refund & Payment Reconciliation Workflow

This document provides official standard operating procedures (SOP) for Luméa Atelier operations staff, customer support specialists, and store administrators to reconcile payments, handle late bank approvals, and process customer refunds.

---

## 🏛️ 1. Architecture Overview

In Luméa's high-integrity checkout system, payment processing and inventory reservation follow strict state-machine rules:
1. **Server-Priced Order Creation**: All orders are persisted and priced on the server before QR issuance or payment handoff.
2. **Stock Reservation**: When an order is placed, stock is atomically decremented.
3. **Session Expiry**: KHQR orders have a 15-minute payment window. If unpaid after 15 minutes, `expire_pending_orders()` atomically releases reserved stock and sets `status = 'Expired'`, `payment_status = 'Expired'`.
4. **Idempotent Settlement**: Repeated bank webhooks or polling events cannot rewind fulfilled orders or duplicate credits.

---

## ⚡ 2. Handling Late Bank Payments (`Payment Review`)

### Scenario:
A customer completes payment in their banking app (Bakong / ABA Mobile) after the 15-minute checkout window has closed, or right after the order was automatically expired.

### Automated System Behavior:
- When the payment notification arrives (via ABA PayWay webhook `/api/payments/khqr/callback` or polling `/api/payments/khqr/check`):
- `settle_payment()` detects that `order.expires_at <= utcnow()` or `order.status != 'Pending'`.
- The system **safely records the funds**:
  - `payment_status = 'Paid'`
  - `transaction_ref = 'PAYWAY-{TRAN_ID}'` or `'BAKONG-{ID}'`
  - `status = 'Payment Review'`
- **Crucial Safety Guard**: The system deliberately **does not** automatically re-reserve stock. This prevents over-selling inventory if another customer purchased the last unit while the first order was expired.

### Staff Action Checklist:
1. **Navigate to Admin Console**: Go to `Admin Atelier` -> `Orders` (`http://localhost:5174/orders`).
2. **Filter by Status**: Filter the orders table by `Payment Review`.
3. **Inspect Order Details**:
   - Click the order to open the Order Inspector modal.
   - Note the `transaction_ref` and `total` amount paid in USD.
   - Verify the clearance in the ABA Merchant Portal (or Bakong settlement report).
4. **Determine Fulfillment Path**:
   - **Case A: Inventory Available**:
     - Check current stock for each line item in `Products` (`/products`).
     - Click **Reconcile & Confirm (Re-reserve Stock)**. The backend executes an atomic row-locked transaction (`with_for_update()`), verifies stock, decrements inventory, and advances the status from `Payment Review` to `Confirmed`.
     - The order then proceeds through the standard fulfillment pipeline (`Confirmed -> Processing -> Shipped -> Out for Delivery -> Delivered`).
   - **Case B: Inventory Sold Out or Customer Requests Cancellation**:
     - If an item sold out during the expiry window, attempting to confirm will raise `HTTP 409 Conflict` ("Insufficient inventory").
     - Contact the customer via email or phone (`+855 ...`).
     - Click **Cancel Order** in the inspector. The system sets `status = 'Cancelled'` and `payment_status = 'Refund Pending'`, recording the cancellation event.
     - Staff then issues the refund via the ABA PayWay merchant portal using the order's `transaction_ref`.

---

## 🔄 3. Return & Refund Workflow

Luméa guarantees a 30-day dermatological return window for eligible products.

### Return Lifecycle Timeline:
```
1. Submitted -> 2. Under Review -> 3. Approved -> 4. In Transit -> 5. Item Received -> 6. Refund Processing -> 7. Refund Completed
```

### Return Quantity Guard:
- The system enforces atomic return verification (`with_for_update()` and `SUM(quantity)`).
- A customer cannot request a return quantity greater than what was purchased (`requested_qty + prior_returned <= purchased_qty`).
- Duplicate return submissions are automatically blocked with `HTTP 400 Bad Request`.

### Step-by-Step Staff Guide:
1. **Review Pending Requests**:
   - Open `Admin Atelier` -> `Returns` (`/returns`).
   - Click on the return ticket (e.g. `#RR2611...`).
   - Verify:
     - Order was delivered within the last 30 days.
     - Photos provided show genuine defect, allergic reaction, or intact seal.
2. **Approve Return**:
   - Change status to `Approved`.
   - The customer receives instructions to dispatch the item to:
     > **Luméa Returns Center**
     > #12 Street 271, Sangkat Toul Tom Poung, Phnom Penh, Cambodia 120801
     > Contact: +855 12 345 678
3. **Warehouse Receipt**:
   - Once courier (VET / J&T) delivers the package to the atelier:
   - Update return ticket to `Item Received`.
   - Inspect physical packaging:
     - Unopened/unbroken: Restockable into inventory.
     - Damaged/opened: Dispose according to cosmetic hygiene guidelines (do not restock).
4. **Issue Payment Reversal (ABA PayWay / Bank)**:
   - Copy the original order's `transaction_ref` from the ticket.
   - Open ABA PayWay Merchant Portal -> `Transactions` -> `Refund / Reversal`.
   - Enter `tran_id` and refund the item total.
   - Update ticket status to `Refund Processing`, then `Refund Completed`.

---

## 🛡️ 4. Daily Settlement Checklist

At the end of each business day (18:00 ICT):
1. **Zero Unreviewed Payments**: Ensure the count of `Payment Review` orders is **0**.
2. **Unclaimed Guest Orders**: Verify that no guest orders remain stuck without an associated access token.
3. **Storage & Backups**: In `Settings` (`/settings`), verify the **Media & Upload Storage** indicator displays green (`Persistent Storage` or `Local Storage`).
