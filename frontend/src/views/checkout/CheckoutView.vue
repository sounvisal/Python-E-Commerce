<template>
  <div class="checkout-page-wrapper">
    <div class="checkout-container">
      <!-- 1. Hero Header Banner matching mockup -->
      <section class="checkout-hero-banner">
        <div class="hero-left-content">
          <nav class="breadcrumb-trail" aria-label="Breadcrumb">
            <router-link to="/">Home</router-link>
            <span class="bc-arrow">›</span>
            <router-link to="/cart">Shopping Bag</router-link>
            <span class="bc-arrow">›</span>
            <span class="bc-active">Checkout</span>
          </nav>
          <h1 class="hero-heading">Checkout</h1>
          <p class="hero-subheading">Review your details, choose delivery & payment, and place your order.</p>
        </div>
      </section>

      <!-- 2. Stepper Progress Bar in pill container matching mockup -->
      <div class="checkout-stepper-bar">
        <div class="stepper-item step-completed">
          <span class="stepper-bubble check"><Check :size="12" /></span>
          <span class="stepper-name">{{ localeStore.t('checkout.step_bag') || 'Bag' }}</span>
        </div>
        <div class="stepper-line line-active"></div>
        <div class="stepper-item step-active">
          <span class="stepper-bubble num">2</span>
          <span class="stepper-name">{{ localeStore.t('checkout.step_delivery') || 'Delivery & Payment' }}</span>
        </div>
        <div class="stepper-line"></div>
        <div class="stepper-item step-upcoming">
          <span class="stepper-bubble num">3</span>
          <span class="stepper-name">{{ localeStore.t('checkout.step_confirmation') || 'Confirmation' }}</span>
        </div>
      </div>

      <!-- Empty Cart State -->
      <div v-if="cartStore.items.length === 0" class="empty-bag-card">
        <p>{{ localeStore.t('cart.empty') || 'Your shopping bag is currently empty.' }}</p>
        <router-link to="/shop" class="btn-return-catalog">{{ localeStore.t('cart.return_to_catalog') || 'Return to Catalog' }}</router-link>
      </div>

      <!-- Main Checkout Form Grid -->
      <form v-else @submit.prevent="handleSubmitOrder" class="checkout-main-grid">
        <!-- LEFT COLUMN: The 3 numbered cards -->
        <div class="checkout-cards-column">
          <!-- CARD 01: Contact Information -->
          <section class="atelier-card card-contact">
            <div class="card-header-row">
              <div class="sec-badge">01</div>
              <div class="sec-title-wrap">
                <h2 class="sec-title">{{ localeStore.t('checkout.contact_info') || 'Contact Information' }}</h2>
                <p class="sec-subtitle">{{ localeStore.t('checkout.contact_sub') || "We'll use this to keep you updated about your order." }}</p>
              </div>
              <div v-if="!authStore.isAuthenticated" class="sec-login-hint">
                {{ localeStore.t('checkout.already_account') || 'Already have an account?' }} <router-link to="/login" class="link-login">{{ localeStore.t('checkout.log_in') || 'Log in' }}</router-link>
              </div>
            </div>

            <div class="form-grid-2">
              <div class="input-field-group">
                <label class="field-label" for="cName">
                  {{ localeStore.t('checkout.full_name') || 'Full Name' }} <span class="req-star">*</span>
                </label>
                <div class="input-icon-box">
                  <User :size="16" class="field-icon" />
                  <input
                    type="text"
                    id="cName"
                    v-model="form.customer_name"
                    required
                    autocomplete="name"
                    placeholder="e.g. Sreynich Chan"
                    class="form-text-input"
                  />
                </div>
              </div>

              <div class="input-field-group">
                <label class="field-label" for="cPhone">
                  {{ localeStore.t('checkout.phone_number') || 'Phone Number (Courier Contact)' }} <span class="req-star">*</span>
                </label>
                <div class="input-icon-box">
                  <Phone :size="16" class="field-icon" />
                  <input
                    type="tel"
                    id="cPhone"
                    v-model="form.customer_phone"
                    required
                    autocomplete="tel"
                    placeholder="+855 12 345 678"
                    class="form-text-input"
                  />
                </div>
              </div>
            </div>

            <div class="form-grid-2 form-grid-bottom">
              <div class="input-field-group">
                <label class="field-label" for="cEmail">
                  {{ localeStore.t('checkout.email_address') || 'Email Address' }} <span class="req-star">*</span>
                </label>
                <div class="input-icon-box">
                  <Mail :size="16" class="field-icon" />
                  <input
                    type="email"
                    id="cEmail"
                    v-model="form.customer_email"
                    required
                    autocomplete="email"
                    placeholder="sreynich.chan@example.com"
                    class="form-text-input"
                  />
                </div>
              </div>

              <div class="checkbox-field-group">
                <label class="marketing-checkbox-label">
                  <input
                    type="checkbox"
                    v-model="form.marketing_opt_in"
                    class="custom-check-input"
                  />
                  <span class="custom-check-box">
                    <Check v-if="form.marketing_opt_in" :size="12" class="check-icon-svg" />
                  </span>
                  <span class="checkbox-text">
                    {{ localeStore.t('checkout.newsletter_opt') || 'Keep me updated on exclusive offers, new arrivals, and skincare tips.' }}
                  </span>
                </label>
              </div>
            </div>
          </section>

          <!-- CARD 02: Delivery & Courier Dispatch -->
          <section class="atelier-card card-delivery">
            <div class="card-header-row">
              <div class="sec-badge">02</div>
              <div class="sec-title-wrap">
                <h2 class="sec-title">{{ localeStore.t('checkout.delivery_dispatch') || 'Delivery & Courier Dispatch' }}</h2>
                <p class="sec-subtitle">{{ localeStore.t('checkout.delivery_sub') || 'Select your address, courier, and delivery option in Cambodia.' }}</p>
              </div>
            </div>

            <!-- Subsection A: Shipping Address -->
            <div class="sub-section">
              <h3 class="sub-section-title">
                <MapPin :size="15" class="sub-icon" />
                {{ localeStore.t('checkout.shipping_address') || 'Shipping Address' }}
              </h3>

              <!-- Address Option 1: Default Address Card -->
              <div
                class="address-option-card"
                :class="{ selected: addressSelectionMode === 'default' }"
                @click="selectAddressMode('default')"
              >
                <div class="option-radio-dot" :class="{ active: addressSelectionMode === 'default' }"></div>
                <div class="address-content-wrap">
                  <div class="address-title-line">
                    <strong class="addr-name">{{ localeStore.t('checkout.default_address') || 'Home' }}</strong>
                    <span class="default-pill">({{ localeStore.t('checkout.default_address') || 'Default' }})</span>
                  </div>
                  <p class="address-body-text">
                    {{ defaultAddressText }}
                  </p>
                </div>
                <div class="address-actions-btns">
                  <button type="button" class="btn-action-sm" @click.stop="toggleEditDefaultAddress">
                    <Edit2 :size="12" />
                    <span>{{ localeStore.t('common.edit') || 'Edit' }}</span>
                  </button>
                  <button type="button" class="btn-action-sm btn-delete-sm" @click.stop="clearAddressToNew">
                    <Trash2 :size="12" />
                    <span>{{ localeStore.t('common.delete') || 'Delete' }}</span>
                  </button>
                </div>
              </div>

              <!-- Address Option 2: Add New Address Card -->
              <div
                class="address-option-card add-new-card"
                :class="{ selected: addressSelectionMode === 'new' }"
                @click="selectAddressMode('new')"
              >
                <div class="option-radio-dot" :class="{ active: addressSelectionMode === 'new' }"></div>
                <div class="address-content-wrap">
                  <strong class="addr-name">{{ localeStore.t('checkout.add_new_address') || 'Add New Address' }}</strong>
                  <p class="address-sub-text">{{ localeStore.t('checkout.add_new_address') || 'Add a new delivery address' }}</p>
                </div>
                <span class="addr-chevron">›</span>
              </div>

              <!-- Editable Address Fields (shown when editing or in 'new' mode) -->
              <div v-if="addressSelectionMode === 'new' || isEditingAddress" class="custom-address-fields">
                <div class="form-grid-2">
                  <div class="input-field-group">
                    <label class="field-label" for="sCity">
                      {{ localeStore.t('checkout.province_city') || 'Province / City' }} <span class="req-star">*</span>
                    </label>
                    <select id="sCity" v-model="form.shipping_city" required autocomplete="address-level2" class="form-select-input" @change="handleCityChange">
                      <option value="Krong Kampot (Kampot Town)">Krong Kampot (Kampot Town - Local Atelier)</option>
                      <option value="Kampot Province (Other Districts)">Kampot Province (Other Districts - Rural)</option>
                      <option value="Phnom Penh">Phnom Penh (Capital)</option>
                      <option value="Siem Reap">Siem Reap</option>
                      <option value="Battambang">Battambang</option>
                      <option value="Sihanoukville">Sihanoukville (Preah Sihanouk)</option>
                      <option value="Kandal">Kandal</option>
                      <option value="Banteay Meanchey">Banteay Meanchey</option>
                      <option value="Kampong Cham">Kampong Cham</option>
                      <option value="Kampong Chhnang">Kampong Chhnang</option>
                      <option value="Kampong Speu">Kampong Speu</option>
                      <option value="Kampong Thom">Kampong Thom</option>
                      <option value="Kep">Kep</option>
                      <option value="Koh Kong">Koh Kong</option>
                      <option value="Kratie">Kratie</option>
                      <option value="Mondulkiri">Mondulkiri</option>
                      <option value="Oddar Meanchey">Oddar Meanchey</option>
                      <option value="Pailin">Pailin</option>
                      <option value="Preah Vihear">Preah Vihear</option>
                      <option value="Prey Veng">Prey Veng</option>
                      <option value="Pursat">Pursat</option>
                      <option value="Ratanakiri">Ratanakiri</option>
                      <option value="Stung Treng">Stung Treng</option>
                      <option value="Svay Rieng">Svay Rieng</option>
                      <option value="Takeo">Takeo</option>
                      <option value="Tboung Khmum">Tboung Khmum</option>
                    </select>
                  </div>

                  <div class="input-field-group">
                    <label class="field-label" for="sAddress">
                      {{ localeStore.t('checkout.street_address') || 'Street Address, Sangkat & Khan' }} <span class="req-star">*</span>
                    </label>
                    <div class="input-icon-box">
                      <MapPin :size="16" class="field-icon" />
                      <input
                        type="text"
                        id="sAddress"
                        v-model="form.shipping_address"
                        required
                        autocomplete="street-address"
                        placeholder="e.g. Phum Ta Nguon, Sangkat Kakab 1, Khan Pou Senchey"
                        class="form-text-input"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Subsection B: Delivery Location (Fine-tune) -->
            <div class="sub-section">
              <h3 class="sub-section-title">
                <MapPin :size="15" class="sub-icon" />
                {{ localeStore.t('checkout.delivery_location_pin') || 'Delivery Location' }}
              </h3>
              <p class="sub-section-hint">{{ localeStore.t('checkout.delivery_location_hint') || 'Help our courier find you faster. Pin your exact location on the map.' }}</p>

              <!-- Integrated GPS & Leaflet Map Picker in Compact Mode matching mockup -->
              <LocationMapPicker
                :initial-lat="form.delivery_lat"
                :initial-lng="form.delivery_lng"
                :initial-notes="form.delivery_notes"
                :compact="true"
                @update:location="handleLocationUpdate"
              />
            </div>

            <!-- Subsection C: Select Cambodia Courier with authentic logos & pricing -->
            <div class="sub-section courier-sub-section">
              <div class="courier-section-header">
                <div>
                  <h3 class="sub-section-title">
                    <Truck :size="15" class="sub-icon" />
                    {{ localeStore.t('checkout.select_courier') || 'Select Cambodia Courier' }}
                  </h3>
                  <p class="sub-section-hint">{{ localeStore.t('checkout.courier_hint') || 'Direct delivery to all 25 provinces and Phnom Penh.' }}</p>
                </div>

                <!-- Dynamic Free Delivery Status Alert Pill/Banner -->
                <div v-if="cartStore.freeShippingEnabled && cartStore.freeShippingMode !== 'disabled'" class="free-shipping-promo-banner">
                  <div v-if="cartStore.freeShippingMode === 'all_orders'" class="promo-pill promo-pill-active">
                    <Sparkles :size="12" class="promo-sparkle-icon" />
                    <span><strong>Atelier Special:</strong> {{ cartStore.freeShippingPromoText || 'Free Nationwide Delivery on ALL orders!' }}</span>
                  </div>
                  <div v-else-if="cartStore.isFreeDeliveryActive" class="promo-pill promo-pill-active">
                    <Sparkles :size="12" class="promo-sparkle-icon" />
                    <span><strong>Complimentary Delivery Unlocked:</strong> Free delivery applied!</span>
                  </div>
                  <div v-else class="promo-pill promo-pill-incentive">
                    <Truck :size="12" class="promo-truck-icon" />
                    <span>Add <strong>{{ localeStore.formatPrice(cartStore.freeDeliveryRemaining) }}</strong> more for Free Delivery</span>
                  </div>
                </div>
              </div>

              <fieldset class="couriers-four-grid" role="radiogroup" aria-labelledby="courier-heading">
                <legend id="courier-heading" class="sr-only">{{ localeStore.t('checkout.select_courier') || 'Select Cambodia Courier' }}</legend>

                <!-- 1. Luméa Shop Direct Delivery (Atelier Courier) -->
                <label
                  class="courier-card"
                  :class="{ selected: form.shipping_carrier === 'lumea_concierge' }"
                >
                  <input
                    type="radio"
                    name="shipping_carrier"
                    value="lumea_concierge"
                    :checked="form.shipping_carrier === 'lumea_concierge'"
                    @change="setCarrier('lumea_concierge')"
                    class="sr-only-radio"
                  />
                  <div class="courier-top-row">
                    <span class="courier-tag tag-concierge">SHOP BEST VALUE</span>
                    <span class="courier-price" :class="{ 'free-price': cartStore.carrierQuoteMap.lumea_concierge.isFree }">
                      <span v-if="cartStore.carrierQuoteMap.lumea_concierge.isFree" class="strike-original">{{ localeStore.formatPrice(cartStore.carrierQuoteMap.lumea_concierge.baseFee) }}</span>
                      {{ cartStore.carrierQuoteMap.lumea_concierge.isFree ? localeStore.t('common.free') : localeStore.formatPrice(cartStore.carrierQuoteMap.lumea_concierge.fee) }}
                    </span>
                  </div>
                  <div class="courier-title-line">
                    <span class="courier-radio-circle" :class="{ active: form.shipping_carrier === 'lumea_concierge' }"></span>
                    <div class="courier-logo-box">
                      <Truck :size="16" style="color: #8B2E24;" />
                    </div>
                    <div class="courier-names-wrap">
                      <span class="courier-brand-name">{{ localeStore.t('checkout.concierge_name') || 'Luméa Direct' }}</span>
                      <span class="courier-sub-name">Shop Courier</span>
                    </div>
                  </div>
                  <div class="courier-eta">
                    <Clock :size="11" class="eta-icon" />
                    <span>{{ cartStore.carrierQuoteMap.lumea_concierge.transit }}</span>
                  </div>
                </label>

                <!-- 2. VET Logistics (Vireak Buntham) -->
                <label
                  class="courier-card"
                  :class="{ selected: form.shipping_carrier === 'vet_express' }"
                >
                  <input
                    type="radio"
                    name="shipping_carrier"
                    value="vet_express"
                    :checked="form.shipping_carrier === 'vet_express'"
                    @change="setCarrier('vet_express')"
                    class="sr-only-radio"
                  />
                  <div class="courier-top-row">
                    <span class="courier-tag tag-vet">NATIONWIDE #1</span>
                    <span class="courier-price" :class="{ 'free-price': cartStore.carrierQuoteMap.vet_express.isFree }">
                      <span v-if="cartStore.carrierQuoteMap.vet_express.isFree" class="strike-original">{{ localeStore.formatPrice(cartStore.carrierQuoteMap.vet_express.baseFee) }}</span>
                      {{ cartStore.carrierQuoteMap.vet_express.isFree ? localeStore.t('common.free') : localeStore.formatPrice(cartStore.carrierQuoteMap.vet_express.fee) }}
                    </span>
                  </div>
                  <div class="courier-title-line">
                    <span class="courier-radio-circle" :class="{ active: form.shipping_carrier === 'vet_express' }"></span>
                    <div class="courier-logo-box">
                      <img src="/images/couriers/vet_express.png" alt="VET Logistics" class="courier-logo-img" />
                    </div>
                    <div class="courier-names-wrap">
                      <span class="courier-brand-name">{{ localeStore.t('checkout.vet_name') || 'Vireak Buntham' }}</span>
                      <span class="courier-sub-name">{{ localeStore.t('checkout.vet_sub') || '(VET Express)' }}</span>
                    </div>
                  </div>
                  <div class="courier-eta">
                    <Clock :size="11" class="eta-icon" />
                    <span>{{ cartStore.carrierQuoteMap.vet_express.transit }}</span>
                  </div>
                </label>

                <!-- 3. J&T Express Cambodia -->
                <label
                  class="courier-card"
                  :class="{ selected: form.shipping_carrier === 'jt_express' }"
                >
                  <input
                    type="radio"
                    name="shipping_carrier"
                    value="jt_express"
                    :checked="form.shipping_carrier === 'jt_express'"
                    @change="setCarrier('jt_express')"
                    class="sr-only-radio"
                  />
                  <div class="courier-top-row">
                    <span class="courier-tag tag-jt">FAST DOMESTIC</span>
                    <span class="courier-price" :class="{ 'free-price': cartStore.carrierQuoteMap.jt_express.isFree }">
                      <span v-if="cartStore.carrierQuoteMap.jt_express.isFree" class="strike-original">{{ localeStore.formatPrice(cartStore.carrierQuoteMap.jt_express.baseFee) }}</span>
                      {{ cartStore.carrierQuoteMap.jt_express.isFree ? localeStore.t('common.free') : localeStore.formatPrice(cartStore.carrierQuoteMap.jt_express.fee) }}
                    </span>
                  </div>
                  <div class="courier-title-line">
                    <span class="courier-radio-circle" :class="{ active: form.shipping_carrier === 'jt_express' }"></span>
                    <div class="courier-logo-box">
                      <img src="/images/couriers/jt_express.png" alt="J&T Express" class="courier-logo-img" />
                    </div>
                    <div class="courier-names-wrap">
                      <span class="courier-brand-name">{{ localeStore.t('checkout.jt_name') || 'J&T Express' }}</span>
                      <span class="courier-sub-name">{{ localeStore.t('checkout.jt_sub') || 'Cambodia' }}</span>
                    </div>
                  </div>
                  <div class="courier-eta">
                    <Clock :size="11" class="eta-icon" />
                    <span>{{ cartStore.carrierQuoteMap.jt_express.transit }}</span>
                  </div>
                </label>

                <!-- 4. GrabExpress On-Demand (Distance-Based Fare) -->
                <label
                  class="courier-card"
                  :class="{
                    selected: form.shipping_carrier === 'grab_express',
                    disabled: !cartStore.carrierQuoteMap.grab_express.available
                  }"
                >
                  <input
                    type="radio"
                    name="shipping_carrier"
                    value="grab_express"
                    :disabled="!cartStore.carrierQuoteMap.grab_express.available"
                    :checked="form.shipping_carrier === 'grab_express'"
                    @change="setCarrier('grab_express')"
                    class="sr-only-radio"
                  />
                  <div class="courier-top-row">
                    <span class="courier-tag tag-grab">INSTANT EXPRESS</span>
                    <span v-if="cartStore.carrierQuoteMap.grab_express.available" class="courier-price" :class="{ 'has-subsidy': cartStore.isFreeDeliveryActive && cartStore.grabSubsidyEnabled }">
                      <span v-if="cartStore.isFreeDeliveryActive && cartStore.grabSubsidyEnabled" class="strike-original">{{ localeStore.formatPrice(cartStore.carrierQuoteMap.grab_express.baseFee) }}</span>
                      {{ localeStore.formatPrice(cartStore.carrierQuoteMap.grab_express.fee) }}
                    </span>
                    <span v-else class="courier-tag tag-pp-only">SAME CITY ONLY</span>
                  </div>
                  <div class="courier-title-line">
                    <span class="courier-radio-circle" :class="{ active: form.shipping_carrier === 'grab_express' }"></span>
                    <div class="courier-logo-box">
                      <img src="/images/couriers/grab_express.png" alt="GrabExpress" class="courier-logo-img" />
                    </div>
                    <div class="courier-names-wrap">
                      <span class="courier-brand-name">{{ localeStore.t('checkout.grab_name') || 'GrabExpress' }}</span>
                      <span class="courier-sub-name">{{ localeStore.t('checkout.grab_sub') || 'On-Demand' }}</span>
                    </div>
                  </div>
                  <div class="courier-eta" :class="{ 'eta-warn': !cartStore.carrierQuoteMap.grab_express.available }">
                    <Clock :size="11" class="eta-icon" />
                    <span>{{ cartStore.carrierQuoteMap.grab_express.transit }}</span>
                  </div>
                </label>
              </fieldset>
            </div>
          </section>

          <!-- CARD 03: Payment Selection -->
          <section class="atelier-card card-payment">
            <div class="card-header-row">
              <div class="sec-badge">03</div>
              <div class="sec-title-wrap">
                <h2 class="sec-title">{{ localeStore.t('checkout.payment_selection') || 'Payment Method' }}</h2>
                <p class="sec-subtitle">{{ localeStore.t('checkout.payment_sub') || 'Choose a secure and convenient payment method.' }}</p>
              </div>
            </div>

            <fieldset class="payment-two-grid" role="radiogroup" aria-labelledby="payment-heading">
              <legend id="payment-heading" class="sr-only">{{ localeStore.t('checkout.payment_selection') || 'Payment Selection' }}</legend>

              <!-- Option 1: Bakong KHQR (ABA Mobile) -->
              <label
                class="payment-option-card"
                :class="{ selected: form.payment_method === 'khqr' }"
                @click="form.payment_method = 'khqr'"
              >
                <input
                  type="radio"
                  name="payment_method"
                  value="khqr"
                  :checked="form.payment_method === 'khqr'"
                  class="sr-only-radio"
                />
                <div class="payment-card-header">
                  <div class="payment-radio-wrap">
                    <span class="payment-radio-circle" :class="{ active: form.payment_method === 'khqr' }"></span>
                    <QrCode :size="18" class="khqr-symbol-icon" />
                    <strong class="payment-title">{{ localeStore.t('checkout.bakong_khqr') || 'Bakong KHQR - ABA Mobile' }}</strong>
                  </div>
                  <span class="payment-badge-tag tag-instant">
                    <Zap :size="10" />
                    {{ localeStore.t('checkout.instant_clearance') || 'INSTANT CLEARANCE' }}
                  </span>
                </div>

                <p class="payment-card-desc">
                  {{ localeStore.t('checkout.khqr_desc') || 'Scan with ABA Mobile, Bakong, Wing, ACLEDA, or any Cambodian banking app.' }}
                </p>

                <div class="bank-pill-row">
                  <span class="bank-chip">ABA Mobile</span>
                  <span class="bank-chip">Bakong</span>
                  <span class="bank-chip">Wing</span>
                  <span class="bank-chip">ACLEDA</span>
                  <span class="bank-chip chip-more">{{ localeStore.t('checkout.all_banks') || '+ All Banks' }}</span>
                </div>
              </label>

              <!-- Option 2: Cash on Delivery (COD) -->
              <label
                class="payment-option-card"
                :class="{ selected: form.payment_method === 'cod' }"
                @click="form.payment_method = 'cod'"
              >
                <input
                  type="radio"
                  name="payment_method"
                  value="cod"
                  :checked="form.payment_method === 'cod'"
                  class="sr-only-radio"
                />
                <div class="payment-card-header">
                  <div class="payment-radio-wrap">
                    <span class="payment-radio-circle" :class="{ active: form.payment_method === 'cod' }"></span>
                    <Package :size="18" class="cod-box-icon-clean" />
                    <strong class="payment-title">{{ localeStore.t('checkout.cod_name') || 'Cash on Delivery (COD)' }}</strong>
                  </div>
                  <span class="payment-badge-tag tag-cod">{{ localeStore.t('checkout.doorstep_handover') || 'DOORSTEP HANDOVER' }}</span>
                </div>

                <p class="payment-card-desc">
                  {{ localeStore.t('checkout.cod_desc') || 'Pay in cash (USD $ or KHR ៛) directly to the delivery driver upon receiving your package.' }}
                </p>

                <!-- Stock reservation notice for COD -->
                <div class="cod-stock-clarification-banner">
                  <Clock :size="12" class="banner-clock-icon" />
                  <span><strong>Order Confirmation:</strong> Stock is reserved and dispatched upon confirmation call from our atelier.</span>
                </div>

                <div class="bank-pill-row">
                  <span class="bank-chip">
                    <Banknote :size="12" class="chip-icon-clean" />
                    <span>{{ localeStore.t('checkout.usd_cash') || 'USD Cash' }}</span>
                  </span>
                  <span class="bank-chip">
                    <Banknote :size="12" class="chip-icon-clean" />
                    <span>{{ localeStore.t('checkout.khr_cash') || 'KHR Cash' }}</span>
                  </span>
                  <span class="bank-chip">
                    <ShieldCheck :size="12" class="chip-icon-clean" />
                    <span>{{ localeStore.t('checkout.zero_surcharge') || 'Zero Surcharge' }}</span>
                  </span>
                </div>
              </label>
            </fieldset>
          </section>

          <!-- BOTTOM ACTION ROW: Back to Shopping Bag & Direct Order Action Button -->
          <div class="checkout-footer-row">
            <router-link to="/cart" class="btn-back-to-bag">
              {{ localeStore.t('checkout.back_to_bag') || '← Back to Shopping Bag' }}
            </router-link>

            <div class="checkout-submit-wrap">
              <button
                type="submit"
                id="btn-authorize-order"
                class="btn-review-order-main"
                :disabled="submitting || cartStore.items.length === 0"
              >
                <span v-if="!submitting">
                  {{ localeStore.currentLocale === 'km' ? `បញ្ជាទិញ · ${formattedTotal}` : localeStore.currentLocale === 'zh' ? `立即下单 · ${formattedTotal}` : `Place Order (COD) · ${formattedTotal}` }}
                </span>
                <span v-else>Processing with Atelier…</span>
              </button>
              <div class="submit-action-context">
                <span class="submit-payment-pill">
                  Payment: Cash on Delivery (COD)
                </span>
                <span class="submit-lock-hint">
                  <ShieldCheck :size="13" />
                  <span>Authorized Server Quote &amp; Instant Clearance</span>
                </span>
              </div>
            </div>
          </div>

          <!-- Error Alert Banner -->
          <div v-if="submitError" class="checkout-error-alert" role="alert">
            {{ submitError }}
          </div>
        </div>

        <!-- RIGHT COLUMN: Order Summary, Promo Code, Shop with Confidence & Help -->
        <aside class="checkout-sidebar-column">
          <!-- 1. Order Summary Card -->
          <div class="sidebar-card summary-card">
            <div class="summary-header">
              <h3 class="summary-title">{{ localeStore.t('checkout.order_summary') || 'Order Summary' }} ({{ cartStore.totalItems }} {{ cartStore.totalItems === 1 ? 'item' : 'items' }})</h3>
              <router-link to="/cart" class="link-edit-cart">{{ localeStore.t('checkout.edit_cart') || 'Edit Cart' }}</router-link>
            </div>

            <!-- Itemized List -->
            <ul class="summary-items-list">
              <li v-for="item in cartStore.items" :key="item.id" class="summary-item-row">
                <img :src="getItemImage(item)" :alt="item.name || item.title" class="item-thumb-img" @error="onThumbError" />
                <div class="item-info-col">
                  <h4 class="item-title">{{ item.name || item.title }}</h4>
                  <div class="item-meta-line">
                    <span class="item-vol">{{ item.selectedVolume || item.volume || 'Full Size' }}</span>
                    <span class="item-qty">{{ localeStore.t('common.qty') || 'Qty' }}: {{ item.quantity }}</span>
                  </div>
                </div>
                <div class="item-price-col">
                  {{ localeStore.formatPrice(item.price * item.quantity) }}
                </div>
              </li>
            </ul>

            <!-- Calculation Lines -->
            <div class="summary-breakdown">
              <div class="breakdown-row">
                <span class="bd-label">{{ localeStore.t('common.subtotal') || 'Subtotal' }}</span>
                <span class="bd-val">{{ localeStore.formatPrice(summary.subtotal) }}</span>
              </div>
              <div class="breakdown-row">
                <span class="bd-label">
                  {{ localeStore.t('common.shipping') || 'Shipping' }} ({{ selectedCarrierName }})
                  <span class="info-circle" title="Calculated based on your selected courier service">ⓘ</span>
                </span>
                <span class="bd-val" :class="{ 'free-shipping-text': summary.shipping_fee === 0 }">
                  {{ summary.shipping_fee === 0 ? localeStore.t('common.free') : localeStore.formatPrice(summary.shipping_fee) }}
                </span>
              </div>
              <div v-if="summary.discount > 0" class="breakdown-row discount-row">
                <span class="bd-label">{{ localeStore.t('common.discount') || 'Promotion Discount' }}</span>
                <span class="bd-val">-{{ Number(summary.subtotal ? summary.discount / summary.subtotal * 100 : 0).toFixed(0) }}% (-{{ localeStore.formatPrice(summary.discount) }})</span>
              </div>
              <div class="breakdown-row">
                <span class="bd-label">{{ localeStore.t('common.tax') || 'Estimated Tax' }}</span>
                <span class="bd-val">{{ localeStore.formatPrice(0) }}</span>
              </div>

              <div class="breakdown-divider"></div>

              <div class="breakdown-row total-row">
                <span class="total-label">{{ localeStore.t('common.total') || 'Total' }} <span class="currency-tag">({{ localeStore.currentCurrency }})</span></span>
                <div class="total-price-wrap">
                  <span class="total-price">{{ localeStore.formatPrice(summary.total) }}</span>
                  <span v-if="localeStore.currentCurrency !== 'USD'" class="total-usd-hint">({{ localeStore.formatPrice(summary.total, 'USD') }} USD)</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 2. Have a Promo Code? Card -->
          <div class="sidebar-card promo-card">
            <h4 class="promo-heading">
              <Tag :size="14" class="promo-title-icon" />
              <span>Have a Promo Code?</span>
            </h4>
            <div class="promo-input-row">
              <input
                type="text"
                v-model="promoInput"
                placeholder="Enter promo code"
                class="promo-text-input"
                :disabled="isApplyingPromo"
                @keydown.enter.prevent="applyPromo"
              />
              <button
                type="button"
                class="btn-apply-promo"
                :disabled="isApplyingPromo || !promoInput.trim()"
                @click="applyPromo"
              >
                {{ isApplyingPromo ? '…' : 'Apply' }}
              </button>
            </div>
            <p v-if="promoFeedback" class="promo-feedback" :class="{ success: promoSuccess, error: !promoSuccess }">
              {{ promoFeedback }}
            </p>
          </div>

          <!-- 3. Shop with Confidence Card -->
          <div class="sidebar-card confidence-card">
            <h4 class="confidence-title">Shop with Confidence</h4>
            <div class="confidence-four-grid">
              <div class="confidence-col">
                <ShieldCheck :size="24" class="conf-icon" />
                <span class="conf-text">100% Authentic Products</span>
              </div>
              <div class="confidence-col">
                <Truck :size="24" class="conf-icon" />
                <span class="conf-text">Reliable Shipping</span>
              </div>
              <div class="confidence-col">
                <RotateCcw :size="24" class="conf-icon" />
                <span class="conf-text">Easy Returns & Exchanges</span>
              </div>
              <div class="confidence-col">
                <Leaf :size="24" class="conf-icon" />
                <span class="conf-text">Better Skin for Everyone</span>
              </div>
            </div>
          </div>

          <!-- 4. Need Help? Card -->
          <div class="sidebar-card help-card">
            <div class="help-content-row">
              <div class="help-headset-wrap">
                <Headphones :size="24" class="help-headset-icon" />
              </div>
              <div class="help-text-wrap">
                <strong class="help-title">Need Help?</strong>
                <p class="help-desc">Our customer support team is here for you.</p>
              </div>
            </div>
            <router-link to="/contact" class="btn-contact-support">
              <MessageSquare :size="14" class="btn-icon-clean" />
              <span>Contact Us</span>
            </router-link>
          </div>
        </aside>
      </form>
    </div>
    <!-- KHQR Payment Modal -->
    <KHQRModal
      v-if="showKHQRModal && pendingKhqrOrder"
      :order-number="pendingKhqrOrder.order_number"
      :amount="pendingKhqrOrder.total"
      :expires-at="pendingKhqrOrder.expires_at"
      :merchant-name="'SUON VISAL'"
      @approved="handleKHQRApproved"
      @cancelled="handleKHQRCancelled"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useLocaleStore } from '@/stores/locale'
import { useNotificationStore } from '@/stores/notification'
import axios from 'axios'
import { rememberOrderAccess } from '@/utils/orderAccess'
import LocationMapPicker from '@/components/checkout/LocationMapPicker.vue'
import KHQRModal from '@/components/checkout/KHQRModal.vue'
import {
  User,
  Phone,
  Mail,
  MapPin,
  Truck,
  QrCode,
  ShieldCheck,
  Check,
  Edit2,
  Trash2,
  RotateCcw,
  Leaf,
  Headphones,
  Clock,
  Sparkles,
  Zap,
  Package,
  Banknote,
  Tag,
  MessageSquare,
  AlertCircle
} from 'lucide-vue-next'

const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()
const localeStore = useLocaleStore()
const notificationStore = useNotificationStore()

// Address Selection Mode
const addressSelectionMode = ref('new')
const defaultAddressText = ref('No saved delivery address')
const isEditingAddress = ref(false)

const form = reactive({
  customer_name: '',
  customer_phone: '',
  customer_email: '',
  shipping_address: '',
  shipping_city: 'Krong Kampot (Kampot Town)',
  shipping_carrier: 'lumea_concierge',
  payment_method: 'khqr',
  delivery_lat: null,
  delivery_lng: null,
  delivery_notes: '',
  marketing_opt_in: true
})

// Canonical town check for local carriers
const CANONICAL_LOCAL_TOWNS = ['krong kampot', 'krong kampot (kampot town)', 'kampot town', 'kampot city']
const isLocalCodEligible = computed(() => true)

function handleCityChange() {
  // Cash on Delivery is enabled nationwide
}

// Keep cartStore delivery destination in sync with form
watch(
  () => form.shipping_city,
  (newCity) => {
    cartStore.setDeliveryDestination({
      city: newCity,
      lat: form.delivery_lat,
      lng: form.delivery_lng
    })
    // Auto-switch away from GrabExpress if user selects non-Kampot destination
    const isLocal = CANONICAL_LOCAL_TOWNS.includes((newCity || '').trim().toLowerCase())
    if (form.shipping_carrier === 'grab_express' && !isLocal) {
      form.shipping_carrier = 'lumea_concierge'
    }
  }
)

const submitting = ref(false)
const submitError = ref('')
const showKHQRModal = ref(false)
const pendingKhqrOrder = ref(null)
const khqrAvailable = ref(true)
const reviewedQuote = ref(null)
const checkoutInput = computed(() => ({
  customer_name: form.customer_name.trim(),
  customer_email: form.customer_email.trim(),
  customer_phone: form.customer_phone.trim(),
  shipping_address: form.shipping_address.trim(),
  shipping_city: form.shipping_city,
  shipping_carrier: form.shipping_carrier,
  delivery_lat: form.delivery_lat,
  delivery_lng: form.delivery_lng,
  delivery_notes: form.delivery_notes,
  payment_method: form.payment_method,
  discount_code: cartStore.discountCode || null,
  items: cartStore.items.map(item => ({ product_id: item.id, quantity: item.quantity }))
}))
const checkoutSignature = computed(() => JSON.stringify([authStore.user?.id, checkoutInput.value]))
const summary = computed(() => reviewedQuote.value?.signature === checkoutSignature.value
  ? reviewedQuote.value.quote
  : {
      subtotal: cartStore.subtotal,
      shipping_fee: cartStore.shippingFee,
      discount: cartStore.discountAmount,
      total: cartStore.grandTotal
    })

const formattedTotal = computed(() => {
  return localeStore.formatPrice(summary.value?.total ?? cartStore.grandTotal)
})

// Promo code states
const promoInput = ref('')
const isApplyingPromo = ref(false)
const promoFeedback = ref('')
const promoSuccess = ref(false)

// Product thumbnail images with automatic high-res fallbacks
function getItemImage(item) {
  if (item.image_url && !item.image_url.includes('undefined')) return item.image_url
  if (item.image && !item.image.includes('undefined')) return item.image
  const name = (item.name || item.title || '').toLowerCase()
  if (name.includes('sk-ii') || name.includes('essence')) {
    return 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=200&q=80'
  }
  if (name.includes('ordinary') || name.includes('niacinamide')) {
    return 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?auto=format&fit=crop&w=200&q=80'
  }
  if (name.includes('laneige') || name.includes('sleeping')) {
    return 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?auto=format&fit=crop&w=200&q=80'
  }
  if (name.includes('cerave') || name.includes('cleanser')) {
    return 'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=200&q=80'
  }
  return 'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=200&q=80'
}

function onThumbError(e) {
  e.target.src = 'https://images.unsplash.com/photo-1556228720-195a672e8a03?auto=format&fit=crop&w=200&q=80'
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    notificationStore.addToast('Please sign in or create an account to proceed with checkout.', 'info')
    router.replace({ path: '/login', query: { redirect: '/checkout' } })
    return
  }
  await cartStore.fetchSettings()

  // Pre-fill from logged-in user profile
  if (authStore.user) {
    form.customer_name = authStore.user.name || authStore.user.full_name || ''
    form.customer_email = authStore.user.email || ''
    if (authStore.user.phone) form.customer_phone = authStore.user.phone
    if (authStore.defaultAddress?.street) selectAddressMode('default')
  }

  cartStore.setDeliveryDestination({
    city: form.shipping_city,
    lat: form.delivery_lat,
    lng: form.delivery_lng
  })

  restorePendingPayment()
})

function selectAddressMode(mode) {
  const saved = authStore.defaultAddress
  if (mode === 'default' && saved?.street) {
    addressSelectionMode.value = 'default'
    form.shipping_address = saved.street
    form.shipping_city = saved.city || 'Phnom Penh'
    form.delivery_lat = null
    form.delivery_lng = null
    defaultAddressText.value = [saved.street, saved.city].filter(Boolean).join(', ')
    isEditingAddress.value = false
    cartStore.setDeliveryDestination({ city: form.shipping_city, lat: null, lng: null })
  } else {
    addressSelectionMode.value = 'new'
    isEditingAddress.value = true
  }
}

function toggleEditDefaultAddress() {
  isEditingAddress.value = !isEditingAddress.value
  addressSelectionMode.value = 'default'
}

function clearAddressToNew() {
  addressSelectionMode.value = 'new'
  form.shipping_address = ''
  form.delivery_lat = null
  form.delivery_lng = null
  cartStore.setDeliveryDestination({ lat: null, lng: null })
  isEditingAddress.value = true
}

function setCarrier(carrierId) {
  if (carrierId === 'grab_express' && !cartStore.carrierQuoteMap.grab_express.available) {
    notificationStore.addToast('GrabExpress motorbike delivery is available within Kampot province only. For other provinces, please select Luméa Shop Direct ($1.00), Vireak Buntham (VET), or J&T Express.', 'info')
    return
  }
  form.shipping_carrier = carrierId
  cartStore.setCarrier(carrierId)
}

function handleLocationUpdate({ lat, lng, notes, auto_address, auto_city }) {
  form.delivery_lat = lat
  form.delivery_lng = lng
  form.delivery_notes = notes
  if (auto_address) {
    form.shipping_address = auto_address
    defaultAddressText.value = `${auto_address}, ${auto_city || form.shipping_city}, Cambodia`
  }
  if (auto_city) {
    form.shipping_city = auto_city
  }
  cartStore.setDeliveryDestination({
    city: auto_city || form.shipping_city,
    lat,
    lng
  })
}

const selectedCarrierName = computed(() => {
  const map = {
    lumea_concierge: 'Luméa Shop Direct ($1.00)',
    vet_express: 'VET Logistics ($1.50)',
    jt_express: 'J&T Express ($1.75)',
    grab_express: 'GrabExpress'
  }
  return map[form.shipping_carrier] || 'Domestic Courier'
})

async function applyPromo() {
  const code = promoInput.value.trim()
  if (!code) return
  isApplyingPromo.value = true
  promoFeedback.value = ''
  try {
    const res = await cartStore.applyPromoCode(code)
    promoSuccess.value = res.success
    promoFeedback.value = res.message
    if (res.success) {
      promoInput.value = ''
    }
  } catch (err) {
    promoSuccess.value = false
    promoFeedback.value = 'Invalid promo code'
  } finally {
    isApplyingPromo.value = false
  }
}

const attemptStorageKey = 'lumea_checkout_attempt'
const pendingPaymentKey = 'lumea_pending_khqr'

function restorePendingPayment() {
  try {
    const saved = JSON.parse(sessionStorage.getItem(pendingPaymentKey))
    if (!saved || saved.accountId !== (authStore.user?.id ?? null)) return
    if (!saved.order?.order_number || !Number.isFinite(saved.order.total) || !saved.order.expires_at) return
    pendingKhqrOrder.value = saved.order
    showKHQRModal.value = true
  } catch {
    sessionStorage.removeItem(pendingPaymentKey)
  }
}

async function getCheckoutKey(signature) {
  const fingerprint = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(signature))
  const digest = Array.from(new Uint8Array(fingerprint), byte => byte.toString(16).padStart(2, '0')).join('')
  const previous = sessionStorage.getItem(attemptStorageKey)?.split(':')
  if (previous?.[0] === digest && previous[1]) return previous[1]
  const key = crypto.randomUUID()
  sessionStorage.setItem(attemptStorageKey, `${digest}:${key}`)
  return key
}

async function handleSubmitOrder() {
  if (!authStore.isAuthenticated) {
    notificationStore.addToast('Please sign in or create an account to place your order.', 'error')
    router.push({ path: '/login', query: { redirect: '/checkout' } })
    return
  }
  if (submitting.value || showKHQRModal.value || !cartStore.items.length) return
  const details = checkoutInput.value
  if (!details.customer_name || !details.customer_email || !details.customer_phone || !details.shipping_address) {
    submitError.value = 'Please complete all required fields.'
    return
  }

  submitting.value = true
  submitError.value = ''
  const signature = checkoutSignature.value
  try {
    const checkout_key = await getCheckoutKey(signature)
    const { data } = await axios.post('/api/orders/quote', { ...details, checkout_key })
    if (checkoutSignature.value !== signature) return
    const quote = data.data
    if (Math.abs(quote.total - summary.value.total) > 0.009) {
      reviewedQuote.value = { signature, quote }
      submitError.value = 'The order total changed. Review the updated summary before placing your order.'
      return
    }

    const response = await axios.post('/api/orders', { ...details, payment_method: form.payment_method, checkout_key, expected_total: quote.total })
    const order = response.data.data
    rememberOrderAccess(order)
    if (form.payment_method === 'khqr') {
      pendingKhqrOrder.value = order
      sessionStorage.setItem(pendingPaymentKey, JSON.stringify({ accountId: authStore.user?.id ?? null, order }))
      showKHQRModal.value = true
    } else {
      completeCheckout(order.order_number)
    }
  } catch (err) {
    const detail = err.response?.data?.detail
    if (detail?.quote && checkoutSignature.value === signature) {
      reviewedQuote.value = { signature, quote: detail.quote }
    }
    if (typeof detail === 'string' && /expired|cancelled/i.test(detail)) sessionStorage.removeItem(attemptStorageKey)
    submitError.value = typeof detail === 'string' ? detail : detail?.message || 'Unable to place the order. Please try again.'
  } finally {
    submitting.value = false
  }
}

function completeCheckout(orderNumber) {
  sessionStorage.removeItem(attemptStorageKey)
  sessionStorage.removeItem(pendingPaymentKey)
  cartStore.clearCart()
  router.push({ name: 'order-success', params: { orderNumber } })
}

function handleKHQRApproved({ orderNumber }) {
  showKHQRModal.value = false
  completeCheckout(orderNumber)
}

function handleKHQRCancelled({ closed, message } = {}) {
  if (closed) sessionStorage.removeItem(attemptStorageKey)
  sessionStorage.removeItem(pendingPaymentKey)
  if (message) submitError.value = message
  showKHQRModal.value = false
  pendingKhqrOrder.value = null
}

</script>

<style scoped>
/* Page Layout */
.checkout-page-wrapper {
  background-color: #FAF8F5;
  min-height: 100vh;
  padding-bottom: 80px;
}

.checkout-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 20px 0;
  box-sizing: border-box;
}

/* 1. Hero Header Banner matching mockup */
.checkout-hero-banner {
  background-color: #F7EEE9;
  background-image: url('/images/checkout_hero_feathered.png');
  background-repeat: no-repeat;
  background-position: right center;
  background-size: auto 100%;
  border-radius: 14px;
  padding: 22px 32px;
  min-height: 114px;
  display: flex;
  align-items: center;
  margin-bottom: 18px;
  box-sizing: border-box;
}

.hero-left-content {
  max-width: 54%;
}

.breadcrumb-trail {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  color: #78716C;
  margin-bottom: 6px;
}

.breadcrumb-trail a {
  color: #78716C;
  text-decoration: none;
  transition: color 0.15s;
}

.breadcrumb-trail a:hover {
  color: #8B2E24;
}

.bc-arrow {
  color: #A8A29E;
  font-size: 13px;
}

.bc-active {
  color: #8B2E24;
  font-weight: 700;
}

.hero-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 34px;
  font-weight: 700;
  color: #2D1810;
  margin: 0 0 4px;
  line-height: 1.15;
}

.hero-subheading {
  font-size: 13.5px;
  color: #6B5E57;
  margin: 0;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .checkout-hero-banner {
    background-image: none;
    padding: 18px 20px;
  }
  .hero-left-content {
    max-width: 100%;
  }
}

/* 2. Stepper Progress Bar */
.checkout-stepper-bar {
  background: #FFFFFF;
  border: 1px solid #EFEAE4;
  border-radius: 9999px;
  padding: 9px 36px;
  margin: 0 auto 22px auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
  box-sizing: border-box;
  max-width: 100%;
}

.stepper-item {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 1;
  min-width: 0;
}

.stepper-bubble {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.step-completed .stepper-bubble.check {
  background: #FDF1EF;
  color: #8B2E24;
}

.step-completed .stepper-name {
  color: #1C1917;
  font-weight: 700;
  font-size: 13.5px;
}

.step-active .stepper-bubble.num {
  background: #8B2E24;
  color: #FFFFFF;
}

.step-active .stepper-name {
  color: #8B2E24;
  font-weight: 700;
  font-size: 13.5px;
}

.step-upcoming .stepper-bubble.num {
  background: #F3F4F6;
  color: #9CA3AF;
}

.step-upcoming .stepper-name {
  color: #9CA3AF;
  font-weight: 500;
  font-size: 13.5px;
}

.stepper-line {
  flex: 1 1 20px;
  min-width: 8px;
  max-width: 140px;
  height: 2px;
  background: #E5E7EB;
  border-radius: 1px;
}

.stepper-line.line-active {
  background: #8B2E24;
}

@media (max-width: 640px) {
  .checkout-container {
    padding: 12px 10px 0;
  }
  .checkout-stepper-bar {
    padding: 8px 12px;
    gap: 6px;
    border-radius: 12px;
  }
  .stepper-line {
    min-width: 6px;
    max-width: 24px;
  }
  .stepper-name {
    font-size: 11px;
    white-space: normal;
    text-align: center;
  }
  .atelier-card {
    padding: 16px 14px;
  }
  .card-header-row {
    flex-wrap: wrap;
    gap: 8px;
  }
  .sec-login-hint {
    white-space: normal;
    width: 100%;
    margin-top: 4px;
  }
  .form-text-input, .form-select-input, .promo-text-input {
    font-size: 16px !important;
  }
}

@media (max-width: 360px) {
  .checkout-container {
    padding: 10px 6px 0;
  }
  .checkout-stepper-bar {
    padding: 6px 8px;
    gap: 4px;
  }
  .stepper-line {
    min-width: 4px;
    max-width: 12px;
  }
  .stepper-name {
    font-size: 10px;
  }
  .atelier-card {
    padding: 14px 10px;
  }
}

/* Empty Bag */
.empty-bag-card {
  background: #fff;
  border-radius: 16px;
  padding: 48px;
  text-align: center;
  border: 1px solid #E5E7EB;
}

.btn-return-catalog {
  display: inline-block;
  margin-top: 16px;
  background: #8B2E24;
  color: #fff;
  padding: 10px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
}

/* Main Two-Column Grid */
.checkout-main-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 380px;
  gap: 24px;
  align-items: start;
}

@media (max-width: 1180px) {
  .checkout-main-grid {
    grid-template-columns: minmax(0, 1fr) 350px;
    gap: 18px;
  }
}

@media (max-width: 980px) {
  .checkout-main-grid {
    grid-template-columns: 1fr;
  }
}

/* Left Column Cards */
.checkout-cards-column {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.atelier-card {
  background: #FFFFFF;
  border: 1px solid #EBE5DF;
  border-radius: 14px;
  padding: 22px 26px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

/* Card Header with 01, 02, 03 Badge */
.card-header-row {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 18px;
  position: relative;
}

.sec-badge {
  width: 28px;
  height: 28px;
  border: 1.5px solid #8B2E24;
  color: #8B2E24;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12.5px;
  font-weight: 700;
  flex-shrink: 0;
  margin-top: 2px;
}

.sec-title-wrap {
  flex: 1;
}

.sec-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 18px;
  font-weight: 700;
  color: #1C1917;
  margin: 0 0 3px;
}

.sec-subtitle {
  font-size: 12.5px;
  color: #78716C;
  margin: 0;
}

.sec-login-hint {
  font-size: 12.5px;
  color: #57534E;
  white-space: nowrap;
}

.link-login {
  color: #8B2E24;
  text-decoration: underline;
  font-weight: 700;
}

/* Form Fields */
.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

@media (max-width: 640px) {
  .form-grid-2 {
    grid-template-columns: 1fr;
  }
}

.form-grid-bottom {
  margin-top: 14px;
  align-items: center;
}

.input-field-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.field-label {
  font-size: 12.5px;
  font-weight: 600;
  color: #292524;
}

.req-star {
  color: #DC2626;
}

.input-icon-box {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 12px;
  color: #9CA3AF;
  pointer-events: none;
}

.form-text-input, .form-select-input {
  width: 100%;
  padding: 9px 12px 9px 36px;
  background: #FFFFFF;
  border: 1px solid #D6D3D1;
  border-radius: 8px;
  font-size: 13px;
  color: #1C1917;
  transition: border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
}

.form-text-input:focus, .form-select-input:focus {
  outline: none;
  border-color: #8B2E24;
  box-shadow: 0 0 0 3px rgba(139, 46, 36, 0.08);
}

.form-select-input {
  padding-left: 12px;
}

/* Marketing Checkbox */
.checkbox-field-group {
  display: flex;
  align-items: center;
  padding-top: 16px;
}

.marketing-checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
  user-select: none;
}

.custom-check-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.custom-check-box {
  width: 17px;
  height: 17px;
  border: 1.5px solid #8B2E24;
  border-radius: 4px;
  background: #8B2E24;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.15s;
}

.check-icon-svg {
  color: #FFFFFF;
}

.checkbox-text {
  font-size: 12px;
  line-height: 1.35;
  color: #44403C;
}

/* Card 02: Subsections */
.sub-section {
  margin-top: 18px;
  padding-top: 16px;
  border-top: 1px solid #F3F0EC;
}

.sub-section-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 14.5px;
  font-weight: 700;
  color: #1C1917;
  display: flex;
  align-items: center;
  gap: 6px;
  margin: 0 0 4px;
}

.sub-fine-tune {
  font-family: system-ui, -apple-system, sans-serif;
  font-size: 12.5px;
  font-weight: 400;
  color: #78716C;
}

.sub-icon {
  color: #8B2E24;
}

.sub-section-hint {
  font-size: 12px;
  color: #78716C;
  margin: 0 0 10px;
}

/* Address Cards matching mockup */
.address-option-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  margin-bottom: 9px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.address-option-card.selected {
  background: #FFF7F5;
  border-color: #F3D5CF;
}

.option-radio-dot {
  width: 16px;
  height: 16px;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.15s;
}

.option-radio-dot.active {
  border-color: #8B2E24;
}

.option-radio-dot.active::after {
  content: '';
  width: 8px;
  height: 8px;
  background: #8B2E24;
  border-radius: 50%;
}

.address-content-wrap {
  flex: 1;
}

.address-title-line {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 2px;
}

.addr-name {
  font-size: 13px;
  color: #1C1917;
}

.default-pill {
  font-size: 11px;
  font-weight: 600;
  color: #78716C;
}

.address-body-text {
  font-size: 12px;
  color: #57534E;
  margin: 0;
  line-height: 1.35;
}

.address-sub-text {
  font-size: 12px;
  color: #78716C;
  margin: 0;
}

.address-actions-btns {
  display: flex;
  align-items: center;
  gap: 6px;
}

.btn-action-sm {
  background: none;
  border: none;
  color: #78716C;
  font-size: 11.5px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background 0.15s, color 0.15s;
}

.btn-action-sm:hover {
  background: #F3F4F6;
  color: #1C1917;
}

.btn-delete-sm:hover {
  color: #DC2626;
}

.addr-chevron {
  font-size: 18px;
  color: #9CA3AF;
  font-weight: 700;
}

.custom-address-fields {
  margin-top: 10px;
  padding: 12px;
  background: #FAF8F5;
  border-radius: 8px;
  border: 1px solid #EAE5DF;
}

/* Couriers Section Header & Dynamic Free Delivery Banner */
.courier-section-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.free-shipping-promo-banner {
  display: flex;
  align-items: center;
}

.promo-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
  line-height: 1.2;
}

.promo-pill-active {
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  color: #065F46;
}

.promo-sparkle-icon {
  color: #10B981;
  flex-shrink: 0;
}

.promo-pill-incentive {
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  color: #92400E;
}

.promo-truck-icon {
  color: #D97706;
  flex-shrink: 0;
}

.strike-original {
  text-decoration: line-through;
  color: #9CA3AF;
  font-size: 10px;
  font-weight: 500;
  margin-right: 3px;
}

/* Couriers 2-Grid: Generous layout matching Payment Methods & mockup proportions */
.couriers-four-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

@media (max-width: 620px) {
  .couriers-four-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
}

.courier-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  padding: 12px 14px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 104px;
  box-sizing: border-box;
  overflow: hidden;
}

.courier-card:hover:not(.disabled) {
  border-color: #D1D5DB;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.courier-card.selected {
  border-color: #8B2E24;
  background: #FFF8F6;
  box-shadow: 0 0 0 1px #8B2E24;
}

.courier-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: #FAFAFA;
  border-color: #E5E7EB;
}

.courier-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}

.courier-tag {
  font-size: 9.5px;
  font-weight: 800;
  padding: 2.5px 7px;
  border-radius: 4px;
  letter-spacing: 0.3px;
  white-space: nowrap;
  flex-shrink: 0;
}

.tag-vet { background: #FEE2E2; color: #991B1B; }
.tag-jt { background: #FFEDD5; color: #C2410C; }
.tag-grab { background: #DCFCE7; color: #15803D; }
.tag-concierge { background: #FEF9C3; color: #854D0E; }
.tag-pp-only { background: #FEE2E2; color: #DC2626; font-size: 9px; font-weight: 700; }

.courier-price {
  font-size: 13.5px;
  font-weight: 800;
  color: #1C1917;
  display: inline-flex;
  align-items: baseline;
  gap: 5px;
  white-space: nowrap;
  flex-shrink: 0;
}

.courier-price .strike-original {
  text-decoration: line-through;
  color: #9CA3AF;
  font-size: 11px;
  font-weight: 500;
  margin-right: 0;
}

.courier-price.free-price {
  color: #16A34A !important;
  font-weight: 800;
}

.courier-title-line {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.courier-logo-box {
  height: 20px;
  max-width: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.courier-logo-img {
  max-height: 20px;
  max-width: 55px;
  object-fit: contain;
  display: block;
}

.courier-radio-circle {
  width: 15px;
  height: 15px;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.courier-radio-circle.active {
  border-color: #8B2E24;
}

.courier-radio-circle.active::after {
  content: '';
  width: 7px;
  height: 7px;
  background: #8B2E24;
  border-radius: 50%;
}

.courier-names-wrap {
  display: flex;
  flex-direction: column;
  line-height: 1.25;
  min-width: 0;
  flex: 1;
}

.courier-brand-name {
  font-size: 12px;
  font-weight: 700;
  color: #1C1917;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.courier-sub-name {
  font-size: 10.5px;
  color: #6B7280;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.courier-eta {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  font-weight: 500;
  color: #4B5563;
  padding-top: 6px;
  border-top: 1px dashed #E5E7EB;
  margin-top: auto;
}

.courier-eta.eta-warn {
  color: #DC2626 !important;
  font-weight: 600;
}

.eta-icon {
  color: #78716C;
  flex-shrink: 0;
}

/* Card 03: Payment Methods 2-Grid */
.payment-two-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.payment-two-grid.single-option {
  grid-template-columns: 1fr;
}

@media (max-width: 680px) {
  .payment-two-grid {
    grid-template-columns: 1fr;
  }
}

.payment-option-card {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: all 0.15s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  box-sizing: border-box;
}

.payment-option-card.selected {
  border-color: #8B2E24;
  background: #FFF8F6;
  box-shadow: 0 0 0 1px #8B2E24;
}

.payment-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 6px;
  flex-wrap: wrap;
}

.payment-radio-wrap {
  display: flex;
  align-items: center;
  gap: 7px;
}

.payment-radio-circle {
  width: 15px;
  height: 15px;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.payment-radio-circle.active {
  border-color: #8B2E24;
}

.payment-radio-circle.active::after {
  content: '';
  width: 7px;
  height: 7px;
  background: #8B2E24;
  border-radius: 50%;
}

.khqr-symbol-icon {
  color: #DC2626;
}

.cod-box-icon {
  font-size: 15px;
}

.payment-title {
  font-size: 13px;
  color: #1C1917;
}

.payment-badge-tag {
  font-size: 9px;
  font-weight: 800;
  padding: 2px 7px;
  border-radius: 10px;
  letter-spacing: 0.3px;
  white-space: nowrap;
}

.tag-instant {
  background: #DC2626;
  color: #FFFFFF;
}

.tag-cod {
  background: #FDF1EC;
  color: #9C4135;
}

.payment-option-card.disabled {
  opacity: 0.65;
  background: #FAFAF9;
  border-color: #E7E5E4;
  cursor: not-allowed;
}

.payment-radio-circle.disabled {
  border-color: #E5E7EB;
  background: #F3F4F6;
}

.tag-restricted {
  background: #F5F5F4;
  color: #78716C;
  border: 1px solid #E7E5E4;
}

.text-restricted-warning {
  color: #B45309;
  font-size: 11px;
  line-height: 1.35;
  display: block;
}

.cod-stock-clarification-banner {
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  border-radius: 6px;
  padding: 6px 9px;
  margin-bottom: 9px;
  font-size: 11px;
  color: #92400E;
  display: flex;
  align-items: center;
  gap: 6px;
  line-height: 1.3;
}

.banner-clock-icon {
  color: #D97706;
  flex-shrink: 0;
}

.remote-payment-blocked-banner {
  grid-column: 1 / -1;
  background: #FEF2F2;
  border: 1px solid #FECACA;
  border-radius: 8px;
  padding: 10px 14px;
  color: #991B1B;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

.payment-card-desc {
  font-size: 11px;
  color: #6B7280;
  margin: 0 0 10px;
  line-height: 1.35;
  flex: 1;
}

.bank-pill-row {
  display: flex;
  align-items: center;
  gap: 5px;
  flex-wrap: wrap;
}

.bank-chip {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  font-size: 9.5px;
  font-weight: 600;
  color: #374151;
  padding: 2px 7px;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.badge-icon-clean,
.chip-icon-clean,
.promo-title-icon,
.btn-icon-clean {
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
}

.cod-box-icon-clean {
  color: #8B2E24;
  margin-right: 4px;
}

.tag-instant {
  display: inline-flex;
  align-items: center;
  gap: 3px;
}

.chip-more {
  background: #F3F4F6;
  color: #4B5563;
}

/* Fieldset accessible radio group resets */
fieldset.couriers-four-grid,
fieldset.payment-two-grid {
  border: none;
  padding: 0;
  margin: 0;
  min-inline-size: min-content;
}

.sr-only,
.sr-only-radio {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  white-space: nowrap !important;
  border-width: 0 !important;
}

.courier-card:focus-within,
.payment-option-card:focus-within {
  outline: 2px solid #8B2E24;
  outline-offset: 2px;
}

/* Bottom Action Row */
.checkout-footer-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 8px;
  gap: 16px;
}

.btn-back-to-bag {
  color: #8B2E24;
  font-size: 13.5px;
  font-weight: 700;
  text-decoration: none;
  transition: opacity 0.15s;
}

.btn-back-to-bag:hover {
  opacity: 0.85;
  text-decoration: underline;
}

.checkout-submit-wrap {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.submit-action-context {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11.5px;
  color: #78716C;
}

.submit-payment-pill {
  background: #F5EFEB;
  color: #8B2E24;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
}

.submit-lock-hint {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #059669;
  font-size: 11px;
}

.btn-review-order-main {
  background: #8B2E24;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 12px 34px;
  font-size: 14.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(139, 46, 36, 0.25);
  box-sizing: border-box;
}

.btn-review-order-main:hover:not(:disabled) {
  background: #732219;
  transform: translateY(-1px);
  box-shadow: 0 4px 10px rgba(139, 46, 36, 0.35);
}

.btn-review-order-main:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 640px) {
  .checkout-footer-row {
    flex-direction: column-reverse;
    align-items: stretch;
    gap: 12px;
  }
  .checkout-submit-wrap {
    align-items: stretch;
    width: 100%;
  }
  .btn-review-order-main {
    width: 100%;
    min-height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
  }
  .submit-action-context {
    justify-content: center;
    flex-wrap: wrap;
    text-align: center;
  }
  .btn-back-to-bag {
    text-align: center;
    padding: 8px 0;
  }
}

.checkout-error-alert {
  padding: 12px 16px;
  background: #FEF2F2;
  border: 1px solid #FECACA;
  border-radius: 8px;
  color: #B91C1C;
  font-size: 13px;
  margin-top: 10px;
}

/* RIGHT COLUMN: Sidebar Cards */
.checkout-sidebar-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 90px;
}

.sidebar-card {
  background: #FFFFFF;
  border: 1px solid #EBE5DF;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  box-sizing: border-box;
}

/* 1. Summary Card */
.summary-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid #F3F0EC;
}

.summary-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 15px;
  font-weight: 700;
  color: #1C1917;
  margin: 0;
}

.link-edit-cart {
  font-size: 12px;
  font-weight: 600;
  color: #8B2E24;
  text-decoration: underline;
}

.summary-items-list {
  list-style: none;
  padding: 0;
  margin: 0 0 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 240px;
  overflow-y: auto;
}

.summary-item-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.item-thumb-img {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  border: 1px solid #E5E7EB;
  object-fit: cover;
  flex-shrink: 0;
  background: #FAF8F5;
}

.item-info-col {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 12px;
  font-weight: 700;
  color: #1C1917;
  margin: 0 0 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-meta-line {
  display: flex;
  gap: 8px;
  font-size: 11px;
  color: #6B7280;
}

.item-price-col {
  font-size: 13.5px;
  font-weight: 700;
  color: #1C1917;
  white-space: nowrap;
}

.summary-breakdown {
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding-top: 10px;
  border-top: 1px solid #F3F0EC;
}

.breakdown-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12.5px;
  color: #44403C;
}

.info-circle {
  font-size: 11px;
  color: #9CA3AF;
  cursor: help;
  margin-left: 2px;
}

.free-shipping-text {
  color: #16A34A;
  font-weight: 700;
}

.discount-row {
  color: #16A34A;
  font-weight: 600;
}

.breakdown-divider {
  height: 1px;
  background: #E5E7EB;
  margin: 6px 0;
}

.total-row {
  font-size: 13.5px;
  font-weight: 700;
  color: #1C1917;
}

.currency-tag {
  font-size: 11px;
  font-weight: 500;
  color: #78716C;
}

.total-price-wrap {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.total-price {
  font-size: 22px;
  font-weight: 800;
  color: #B91C1C;
}

.total-usd-hint {
  font-size: 0.78rem;
  color: #78716C;
  font-weight: 500;
  margin-top: 2px;
}

/* 2. Promo Card */
.promo-heading {
  font-size: 13px;
  font-weight: 700;
  color: #1C1917;
  margin: 0 0 8px;
}

.promo-input-row {
  display: flex;
  gap: 8px;
}

.promo-text-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #D6D3D1;
  border-radius: 6px;
  font-size: 12px;
  color: #1C1917;
}

.promo-text-input:focus {
  outline: none;
  border-color: #8B2E24;
}

.btn-apply-promo {
  background: #8B2E24;
  color: #FFFFFF;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s;
}

.btn-apply-promo:hover:not(:disabled) {
  opacity: 0.9;
}

.promo-feedback {
  margin: 6px 0 0;
  font-size: 11px;
}

.promo-feedback.success { color: #16A34A; font-weight: 600; }
.promo-feedback.error { color: #DC2626; }

/* 3. Shop with Confidence Card */
.confidence-card {
  background: linear-gradient(180deg, #FDF4F2 0%, #FAF6F3 100%);
  border: 1px solid #F3D5CF;
  border-radius: 14px;
  padding: 16px 14px;
}

.confidence-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 15px;
  font-weight: 700;
  color: #8B2E24;
  text-align: center;
  margin: 0 0 12px;
}

.confidence-four-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  text-align: center;
}

.confidence-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.conf-icon {
  color: #8B2E24;
}

.conf-text {
  font-size: 9.5px;
  line-height: 1.2;
  color: #44403C;
  font-weight: 500;
}

/* 4. Need Help? Card */
.help-content-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.help-headset-wrap {
  width: 38px;
  height: 38px;
  border: 1.5px solid #F3D5CF;
  background: #FFF8F6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.help-headset-icon {
  color: #8B2E24;
}

.help-title {
  display: block;
  font-size: 13.5px;
  color: #1C1917;
}

.help-desc {
  font-size: 11.5px;
  color: #78716C;
  margin: 2px 0 0;
}

.btn-contact-support {
  display: block;
  width: 100%;
  text-align: center;
  padding: 8px 16px;
  border: 1.5px solid #8B2E24;
  border-radius: 8px;
  color: #8B2E24;
  background: #FFFFFF;
  text-decoration: none;
  font-size: 12.5px;
  font-weight: 700;
  box-sizing: border-box;
  transition: all 0.15s ease;
}

.btn-contact-support:hover {
  background: #FFF8F6;
}
</style>
