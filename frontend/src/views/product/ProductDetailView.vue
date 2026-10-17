<template>
  <div class="product-detail-page" v-if="product">
    <!-- Breadcrumbs matching Product Details.png -->
    <div class="container breadcrumb-container">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <router-link to="/" class="breadcrumb-link">Home</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <router-link to="/shop" class="breadcrumb-link">Shop</router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <router-link :to="`/category/${product.category || 'toners'}`" class="breadcrumb-link">
          {{ product.category_name || 'Essences' }}
        </router-link>
        <ChevronRight :size="14" class="breadcrumb-sep" />
        <span class="breadcrumb-current">{{ product.name }}</span>
      </nav>
    </div>

    <!-- 3-Column Stage Grid matching Product Details.png -->
    <section class="container stage-container">
      <div class="pdp-layout-grid">
        <!-- 1. Left Gallery Column -->
        <div class="gallery-column">
          <!-- Thumbnail rail on the left -->
          <div class="thumbnail-rail">
            <button
              v-for="(thumb, idx) in productThumbs"
              :key="idx"
              class="thumb-box-btn"
              :class="{ active: activeThumbIdx === idx }"
              @click="selectThumb(idx)"
            >
              <img :src="thumb.url" :alt="thumb.label" class="thumb-img" />
            </button>
            <button class="thumb-down-btn" @click="nextThumb">
              <ChevronDown :size="16" />
            </button>
          </div>

          <!-- Main Visual Stage Box -->
          <div class="main-stage-card">
            <div class="stage-top-badge">
              <span class="gold-best-badge">#1<br />Curated Pick<br />in {{ product.category_name || 'Beauty' }}</span>
            </div>

            <div class="stage-script-header">
              <h3 class="stage-script-title">{{ product.category_name || 'Skincare' }}<br />Care for<br />Healthier<br />Skin.</h3>
            </div>

            <div class="stage-center-img-wrap">
              <img
                :src="activeMainImage"
                :alt="product.name"
                class="stage-hero-packshot"
              />
            </div>

            <div class="stage-benefit-icons">
              <div class="st-benefit-item">
                <Droplet :size="14" />
                <span>Hydrates</span>
              </div>
              <div class="st-benefit-item">
                <Sparkles :size="14" />
                <span>Smooths</span>
              </div>
              <div class="st-benefit-item">
                <Sun :size="14" />
                <span>Brightens</span>
              </div>
              <div class="st-benefit-item">
                <ShieldCheck :size="14" />
                <span>Refines Texture</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. Center Purchasing & Info Column -->
        <div class="purchase-column">
          <div class="pdp-brand-header">
            <router-link :to="`/brand/${brandSlug}`" class="brand-link-title">
              {{ product.brand }}
            </router-link>
          </div>

          <h1 class="pdp-product-title">{{ product.name }}</h1>
          <p class="pdp-formula-sub">{{ product.formula_tag || `Clinically proven ${product.category_name || 'skincare'} formulation for balanced radiance.` }}</p>

          <!-- Ratings Row -->
          <div class="pdp-rating-row">
            <div class="rating-stars">
              <Star v-for="i in 5" :key="i" :size="14" class="star-gold" />
            </div>
            <span class="rating-score">4.8</span>
            <span class="rating-count">({{ product.reviews || '1,243' }} reviews)</span>
            <span class="pipe-sep">|</span>
            <span class="sold-count">10K+ sold</span>
          </div>

          <div class="pdp-best-seller-tag">
            <span class="tag-hash">#1 Best Seller</span>
            <span class="tag-cat">in {{ product.category_name || 'Skincare' }}</span>
          </div>

          <!-- Price -->
          <div class="pdp-price-row">
            <span class="pdp-main-price">${{ selectedSize.price.toFixed(2) }}</span>
          </div>

          <!-- Bio -->
          <p class="pdp-bio-paragraph">
            {{ product.description || 'A dermatologically tested formulation crafted with potent actives to nourish, protect, and restore your skin barrier.' }}
          </p>

          <!-- Size Selector -->
          <div class="pdp-size-section">
            <span class="size-label">Size</span>
            <div class="size-options-grid">
              <button
                v-for="(size, sIdx) in sizeOptions"
                :key="size.label"
                class="size-pill-card"
                :class="{ active: selectedSizeIdx === sIdx }"
                @click="selectedSizeIdx = sIdx"
              >
                <span class="size-name">{{ size.label }}</span>
                <span class="size-cost">${{ size.price.toFixed(2) }}</span>
              </button>
            </div>
          </div>

          <!-- Quantity Stepper -->
          <div class="pdp-qty-section">
            <span class="qty-label">Quantity</span>
            <div class="qty-stepper-box">
              <button @click="decreaseQty" class="qty-step-btn" :disabled="qty <= 1">
                <Minus :size="14" />
              </button>
              <span class="qty-value">{{ qty }}</span>
              <button @click="increaseQty" class="qty-step-btn">
                <Plus :size="14" />
              </button>
            </div>
          </div>

          <!-- Terracotta Action Buttons matching format -->
          <div class="pdp-action-buttons">
            <button
              class="btn-pdp-add-cart"
              :class="{ 'is-added': isAdded }"
              @click="handleAddToCart"
            >
              <Check v-if="isAdded" :size="16" />
              <ShoppingBag v-else :size="16" />
              <span>{{ isAdded ? 'Added to Cart' : 'Add to Cart' }}</span>
            </button>

            <button
              class="btn-pdp-wishlist"
              :class="{ active: isWishlisted }"
              @click="isWishlisted = !isWishlisted"
            >
              <Heart :size="16" />
              <span>Add to Wishlist</span>
            </button>
          </div>

          <!-- 3 Value Trust Items -->
          <div class="pdp-trust-row">
            <div class="trust-item">
              <ShieldCheck :size="16" class="trust-icon" />
              <div class="trust-text">
                <strong>100% Authentic</strong>
                <span>Guaranteed</span>
              </div>
            </div>

            <div class="trust-item">
              <RotateCcw :size="16" class="trust-icon" />
              <div class="trust-text">
                <strong>Easy Returns</strong>
                <span>Within 14 days</span>
              </div>
            </div>

            <div class="trust-item">
              <Truck :size="16" class="trust-icon" />
              <div class="trust-text">
                <strong>Fast Shipping</strong>
                <span>Nationwide</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Right Column: Brand Store & Guarantees Sidebar -->
        <aside class="sidebar-column">
          <!-- Brand Store Card -->
          <div class="brand-store-card">
            <div class="store-card-header">
              <span class="store-card-brand">{{ product.brand }}</span>
              <router-link :to="`/brand/${brandSlug}`" class="view-store-link">
                <span>View Brand Store</span>
                <ArrowRight :size="13" />
              </router-link>
            </div>

            <div class="store-card-body">
              <div class="store-badge-avatar">
                <BrandLogo :slug="brandSlug" :size="28" />
              </div>
              <div class="store-info-text">
                <span class="store-name-strong">{{ product.brand }}</span>
                <p class="store-brief">
                  Official curated atelier collection from {{ product.brand }}. Sourced directly for guaranteed authenticity and optimal freshness.
                </p>
                <div class="store-internal-links">
                  <router-link :to="`/brand/${brandSlug}`" class="s-link">About the Brand →</router-link>
                  <router-link :to="`/brand/${brandSlug}`" class="s-link">All {{ product.brand }} Products →</router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- Atelier Quality & Concierge Guarantees -->
          <div class="assurances-card">
            <div class="assurance-line">
              <ShieldCheck :size="18" class="assure-icon" />
              <div class="assure-text">
                <strong>Direct Brand Sourcing</strong>
                <span>Official {{ product.brand }} supply chain</span>
              </div>
            </div>

            <div class="assurance-line">
              <Truck :size="18" class="assure-icon" />
              <div class="assure-text">
                <strong>Temperature-Controlled Transit</strong>
                <span>Preserves botanical & active potency</span>
              </div>
            </div>

            <div class="assurance-line">
              <Headphones :size="18" class="assure-icon" />
              <div class="assure-text">
                <strong>Atelier Esthetician Concierge</strong>
                <span>Personalized routine pairing support</span>
              </div>
            </div>
          </div>

          <!-- Luméa Points Card -->
          <div class="lumea-points-card">
            <div class="points-icon-wrap">
              <Gift :size="18" />
            </div>
            <div class="points-text-wrap">
              <strong>Earn 99 Luméa Points</strong>
              <span>with this purchase</span>
            </div>
            <HelpCircle :size="15" class="points-help" />
          </div>
        </aside>
      </div>
    </section>

    <!-- Mid-Page Content Tabs matching Product Details.png -->
    <section class="container mid-tabs-container">
      <div class="mid-tabs-bar">
        <button
          v-for="tab in midTabs"
          :key="tab.id"
          class="mid-tab-btn"
          :class="{ active: activeMidTab === tab.id }"
          @click="activeMidTab = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="mid-tab-panel">
        <!-- 1. PRODUCT DETAILS TAB -->
        <div v-if="activeMidTab === 'details'" class="tab-three-cols">
          <!-- Left: Product Details Table -->
          <div class="pdp-details-table-col">
            <h3 class="panel-section-title">Product Details</h3>
            <table class="pdp-spec-table">
              <tbody>
                <tr>
                  <th>Brand</th>
                  <td>{{ product.brand }}</td>
                </tr>
                <tr>
                  <th>Product Type</th>
                  <td>{{ product.category_name || 'Essence' }}</td>
                </tr>
                <tr>
                  <th>Skin Type</th>
                  <td>{{ product.skin_type || 'All skin types' }}</td>
                </tr>
                <tr>
                  <th>Skin Concerns</th>
                  <td>{{ product.concerns || 'Dullness, Uneven texture, Aging' }}</td>
                </tr>
                <tr>
                  <th>Size</th>
                  <td>75 ml / 160 ml / 230 ml</td>
                </tr>
                <tr>
                  <th>Made In</th>
                  <td>Japan</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Center: About This Product -->
          <div class="pdp-about-col">
            <h3 class="panel-section-title">About This Product</h3>
            <p class="about-lead">
              {{ product.description || `${product.name} is a high-performance formulation designed to deliver concentrated active ingredients directly into the skin barrier.` }}
            </p>
            <p class="about-lead">
              Formulated to support the natural cellular renewal cycle, leaving your complexion visibly clearer, smoother, firmer, and more resilient with regular use.
            </p>

            <div class="checklist-items">
              <div class="check-row">
                <CheckCircle2 :size="16" class="check-icon" />
                <span>Visibly improves skin clarity</span>
              </div>
              <div class="check-row">
                <CheckCircle2 :size="16" class="check-icon" />
                <span>Helps refine skin texture</span>
              </div>
              <div class="check-row">
                <CheckCircle2 :size="16" class="check-icon" />
                <span>Boosts skin hydration</span>
              </div>
              <div class="check-row">
                <CheckCircle2 :size="16" class="check-icon" />
                <span>Promotes a more youthful, radiant complexion</span>
              </div>
            </div>
          </div>

          <!-- Right: Testimonial Card with Radiant Skin Model -->
          <div class="pdp-testimonial-col">
            <div class="testimonial-card-box">
              <div class="testimonial-text-side">
                <h4 class="test-heading">Clearer<br />Smoother<br />Brighter<br />Skin.</h4>
                <blockquote class="test-quote">
                  "My skin has never felt this smooth. It's truly a game changer!"
                </blockquote>
                <span class="test-buyer">— Verified Buyer</span>
                <div class="test-stars">
                  <Star v-for="i in 5" :key="i" :size="12" class="star-gold" />
                </div>
              </div>
              <div class="testimonial-img-side">
                <img src="/images/pdp-model-radiant.jpg" alt="Glowing Skin Testimonial" />
              </div>
            </div>
          </div>
        </div>

        <!-- 2. INGREDIENTS TAB -->
        <div v-else-if="activeMidTab === 'ingredients'" class="tab-ingredients-panel">
          <div class="tab-three-cols">
            <div class="ingredients-actives-col">
              <h3 class="panel-section-title">Key Bio-Actives</h3>
              <div class="active-item-list">
                <div class="active-item">
                  <div class="active-badge">90%+</div>
                  <div class="active-text">
                    <strong>PITERA™ (Galactomyces Ferment)</strong>
                    <span>Bio-fermented broth rich in 50+ micronutrients to condition and renew skin barrier.</span>
                  </div>
                </div>
                <div class="active-item">
                  <div class="active-badge">Active</div>
                  <div class="active-text">
                    <strong>Organic Acids &amp; Minerals</strong>
                    <span>Natural balancing elements that maintain optimal epidermal pH balance.</span>
                  </div>
                </div>
                <div class="active-item">
                  <div class="active-badge">Natural</div>
                  <div class="active-text">
                    <strong>Amino Acid Complex</strong>
                    <span>Essential moisture building blocks providing long-lasting cellular hydration.</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="ingredients-inci-col">
              <h3 class="panel-section-title">Full INCI Formulation</h3>
              <p class="inci-lead">
                Galactomyces Ferment Filtrate*, Butylene Glycol, Pentylene Glycol, Aqua (Water), Sodium Benzoate, Methylparaben, Sorbic Acid.
              </p>
              <p class="inci-footnote">*PITERA™ is the exclusive trademark of fermented bio-extract.</p>
              
              <div class="formulation-notes">
                <div class="note-pill"><Leaf :size="14" /> Botanical Origin</div>
                <div class="note-pill"><ShieldCheck :size="14" /> Non-Comedogenic</div>
                <div class="note-pill"><Sparkles :size="14" /> Unscented Pure Formula</div>
              </div>
            </div>

            <div class="ingredients-purity-col">
              <div class="purity-pledge-card">
                <Award :size="28" class="purity-icon" />
                <h4 class="purity-title">Luméa Purity Standard</h4>
                <ul class="purity-list">
                  <li><Check :size="14" /> 100% Sourced from Official Distributors</li>
                  <li><Check :size="14" /> Free of Synthetic Artificial Dyes</li>
                  <li><Check :size="14" /> No Heavy Drying Alcohols</li>
                  <li><Check :size="14" /> Dermatologist Clinically Tested</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. HOW TO USE TAB -->
        <div v-else-if="activeMidTab === 'how-to-use'" class="tab-how-to-use-panel">
          <div class="ritual-steps-grid">
            <div class="ritual-step-card">
              <div class="step-num-badge">01</div>
              <h4 class="step-name">Dispense &amp; Warm</h4>
              <p class="step-desc">
                After cleansing, pour 4 to 5 shakes of the essence into the palm of your hand or saturate a soft cotton pad.
              </p>
            </div>
            <div class="ritual-step-card">
              <div class="step-num-badge">02</div>
              <h4 class="step-name">Press &amp; Pat</h4>
              <p class="step-desc">
                Gently smooth over your face and neck, then pat gently for 1 minute until completely absorbed into the skin.
              </p>
            </div>
            <div class="ritual-step-card">
              <div class="step-num-badge">03</div>
              <h4 class="step-name">Layer &amp; Lock</h4>
              <p class="step-desc">
                Follow with your favorite Luméa serum and moisturizing cream to lock in the concentrated active bio-nutrients.
              </p>
            </div>
          </div>

          <div class="ritual-pro-tip-box">
            <div class="tip-icon-col">
              <Sparkles :size="22" class="tip-icon" />
            </div>
            <div class="tip-content">
              <strong>Atelier Esthetician Tip</strong>
              <p>For an intensive soothing treatment after travel or sun exposure, soak two pure cotton pads in essence and place them over your cheeks for 5 minutes as a restorative sheet mask.</p>
            </div>
          </div>
        </div>

        <!-- 4. BENEFITS TAB -->
        <div v-else-if="activeMidTab === 'benefits'" class="tab-benefits-panel">
          <div class="benefits-metric-grid">
            <div class="benefit-kpi-card">
              <div class="kpi-num">98%</div>
              <div class="kpi-label">Refined Texture</div>
              <p class="kpi-sub">Patrons reported visibly smoother, refined surface clarity within 14 days of daily ritual.</p>
            </div>
            <div class="benefit-kpi-card">
              <div class="kpi-num">95%</div>
              <div class="kpi-label">Radiant Luminosity</div>
              <p class="kpi-sub">Observed a lit-from-within morning glow and significant reduction in visible dullness.</p>
            </div>
            <div class="benefit-kpi-card">
              <div class="kpi-num">24h</div>
              <div class="kpi-label">Continuous Moisture</div>
              <p class="kpi-sub">Clinical measurements demonstrated sustained stratum corneum hydration throughout the day.</p>
            </div>
            <div class="benefit-kpi-card">
              <div class="kpi-num">92%</div>
              <div class="kpi-label">Barrier Firmness</div>
              <p class="kpi-sub">Skin felt more resilient, plump, and prepared to defend against city pollution and fatigue.</p>
            </div>
          </div>
        </div>

        <!-- 5. REVIEWS TAB -->
        <div v-else-if="activeMidTab === 'reviews'" class="tab-reviews-panel">
          <!-- Top Summary Card -->
          <div class="reviews-summary-card">
            <div class="overall-rating-block">
              <span class="big-score">{{ reviewMetrics.average_rating || '4.8' }}</span>
              <div class="stars-gold-row">
                <Star v-for="i in 5" :key="i" :size="18" class="star-gold" />
              </div>
              <span class="total-rev-caption">Based on {{ reviewMetrics.total_reviews || productReviews.length }} verified reviews</span>
            </div>

            <div class="rating-breakdown-bars">
              <div v-for="star in [5, 4, 3, 2, 1]" :key="star" class="star-bar-row">
                <span class="star-num">{{ star }} Star</span>
                <div class="bar-track">
                  <div
                    class="bar-fill"
                    :style="{ width: (reviewMetrics.distribution?.[star]?.percentage || 0) + '%' }"
                  ></div>
                </div>
                <span class="bar-count">{{ reviewMetrics.distribution?.[star]?.count || 0 }}</span>
              </div>
            </div>

            <div class="write-review-cta-col">
              <h4>Share Your Ritual</h4>
              <p>Help other atelier clientele choose the ideal formulation for their skin journey.</p>
              <button class="btn-write-review" @click="openWriteReview">
                <Edit3 :size="16" />
                <span>Write a Review</span>
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="loadingReviews" class="reviews-loading">
            <div class="spinner-atelier"></div>
            <span>Fetching reviews from atelier database...</span>
          </div>

          <!-- Empty State -->
          <div v-else-if="productReviews.length === 0" class="empty-reviews-card">
            <MessageSquare :size="32" class="empty-rev-icon" />
            <h3>No Reviews Yet</h3>
            <p>Be the first customer to share your thoughts on this formulation.</p>
            <button class="btn-write-review-clean" @click="openWriteReview">
              Write the First Review
            </button>
          </div>

          <!-- Reviews Feed -->
          <div v-else class="reviews-list-grid">
            <div v-for="rev in productReviews" :key="rev.id" class="review-item-card">
              <div class="review-header-row">
                <div class="reviewer-meta">
                  <img
                    :src="rev.customer_avatar || '/images/avatar-sreynich.jpg'"
                    :alt="rev.customer_name"
                    class="reviewer-avatar"
                  />
                  <div>
                    <div class="reviewer-name-row">
                      <strong>{{ rev.customer_name }}</strong>
                      <span v-if="rev.verified_purchase" class="badge-verified">
                        <Check :size="12" />
                        Verified Purchase
                      </span>
                    </div>
                    <span class="review-date">
                      {{ rev.created_at ? new Date(rev.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'Aug 24, 2025' }}
                    </span>
                  </div>
                </div>

                <div class="review-stars-row">
                  <Star
                    v-for="i in 5"
                    :key="i"
                    :size="14"
                    :class="i <= rev.rating ? 'star-gold' : 'star-muted'"
                  />
                </div>
              </div>

              <h4 class="review-title">{{ rev.title }}</h4>
              <p class="review-comment">{{ rev.comment }}</p>

              <!-- Atelier Curator Reply -->
              <div v-if="rev.admin_reply" class="curator-reply-box">
                <div class="reply-header">
                  <Sparkles :size="14" class="reply-icon" />
                  <strong>Response from Luméa Atelier</strong>
                  <span class="reply-date">{{ rev.admin_replied_at || 'Recent' }}</span>
                </div>
                <p class="reply-text">{{ rev.admin_reply }}</p>
              </div>

              <div class="review-footer-row">
                <button
                  class="btn-helpful"
                  :class="{ voted: helpfulVoted[rev.id] }"
                  @click="voteHelpful(rev)"
                >
                  <ThumbsUp :size="13" />
                  <span>Helpful ({{ rev.helpful_count || 0 }})</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 6. Q&A TAB -->
        <div v-else-if="activeMidTab === 'qa'" class="tab-qa-panel">
          <div class="qa-list">
            <div class="qa-item">
              <h4 class="qa-question">Q: Can I use this essence together with Vitamin C or Retinol?</h4>
              <p class="qa-answer">A: Yes. Because this formula is lightweight, water-based, and pH-balanced, it acts as an optimal prep step. Apply the essence immediately after cleansing, let it absorb for 60 seconds, and proceed with your active serum.</p>
            </div>
            <div class="qa-item">
              <h4 class="qa-question">Q: How long does one bottle typically last?</h4>
              <p class="qa-answer">A: With twice-daily application (4–5 drops per ritual), the 160 ml bottle provides approximately 3 to 4 months of continuous care.</p>
            </div>
            <div class="qa-item">
              <h4 class="qa-question">Q: Is this essence suitable for reactive or sensitive skin?</h4>
              <p class="qa-answer">A: Yes. Our formulation has undergone rigorous dermatological hypoallergenic testing and contains zero synthetic fragrances or drying alcohols.</p>
            </div>
            <div class="qa-item">
              <h4 class="qa-question">Q: Should I apply this with my hands or a cotton pad?</h4>
              <p class="qa-answer">A: Both methods work wonderfully. Applying directly with clean palms minimizes product waste and allows the natural warmth of your hands to facilitate rapid absorption.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Bottom: "You May Also Like" Carousel matching Product Details.png -->
    <section class="container also-like-container">
      <div class="also-like-header">
        <h2 class="also-like-title">You May Also Like</h2>
        <router-link :to="`/brand/${brandSlug}`" class="see-more-link">
          <span>See More</span>
          <ArrowRight :size="14" />
        </router-link>
      </div>

      <div class="also-like-grid">
        <ProductCard
          v-for="item in youMayAlsoLike"
          :key="item.id"
          :product="item"
        />
      </div>
    </section>

    <!-- Write a Review Modal -->
    <div v-if="showReviewModal" class="modal-backdrop" @click="showReviewModal = false">
      <div class="review-modal-card" @click.stop>
        <div class="modal-header">
          <div>
            <h3 class="modal-title">Write a Customer Review</h3>
            <p class="modal-subtitle">Reviewing: {{ product.name }}</p>
          </div>
          <button class="btn-close-modal" @click="showReviewModal = false">
            <X :size="18" />
          </button>
        </div>

        <form @submit.prevent="submitReview" class="review-modal-form">
          <!-- Star Rating Selector -->
          <div class="form-group">
            <label class="form-label">Overall Rating *</label>
            <div class="star-rating-selector">
              <button
                v-for="s in 5"
                :key="s"
                type="button"
                class="star-pick-btn"
                @mouseenter="hoverStar = s"
                @mouseleave="hoverStar = 0"
                @click="reviewForm.rating = s"
              >
                <Star
                  :size="26"
                  :class="(hoverStar || reviewForm.rating) >= s ? 'star-gold-active' : 'star-inactive'"
                />
              </button>
              <span class="star-rating-label">
                {{ ['Poor', 'Fair', 'Good', 'Very Good', 'Exceptional'][reviewForm.rating - 1] }}
              </span>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label" for="revTitle">Review Headline / Title *</label>
            <input
              id="revTitle"
              v-model="reviewForm.title"
              type="text"
              placeholder="e.g. Visible glow within two weeks"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="revComment">Your Experience / Review *</label>
            <textarea
              id="revComment"
              v-model="reviewForm.comment"
              rows="4"
              placeholder="Tell others how this product worked with your skin, the texture, and any tips..."
              class="form-textarea"
              required
            ></textarea>
          </div>

          <div class="form-row-2">
            <div class="form-group">
              <label class="form-label" for="revName">Your Name</label>
              <input
                id="revName"
                v-model="reviewForm.customer_name"
                type="text"
                placeholder="e.g. Sreynich Chan"
                class="form-input"
              />
            </div>
            <div class="form-group">
              <label class="form-label" for="revEmail">Your Email</label>
              <input
                id="revEmail"
                v-model="reviewForm.customer_email"
                type="email"
                placeholder="e.g. patron@example.com"
                class="form-input"
              />
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="showReviewModal = false">
              Cancel
            </button>
            <button type="submit" class="btn-submit-review" :disabled="submittingReview">
              <span v-if="!submittingReview">Submit Review to Atelier</span>
              <span v-else>Recording Review...</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import {
  ChevronRight,
  ChevronDown,
  Star,
  Minus,
  Plus,
  ShoppingBag,
  Heart,
  Check,
  ShieldCheck,
  RotateCcw,
  Truck,
  Droplet,
  Sparkles,
  Sun,
  ArrowRight,
  Headphones,
  Gift,
  HelpCircle,
  CheckCircle2,
  ThumbsUp,
  MessageSquare,
  Edit3,
  X,
  Leaf,
  Clock,
  Award,
} from 'lucide-vue-next'
import BrandLogo from '@/components/BrandLogo.vue'
import ProductCard from '@/components/ProductCard.vue'
import { useProductStore } from '@/stores/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notification'

const route = useRoute()
const productStore = useProductStore()
const cartStore = useCartStore()
const authStore = useAuthStore()
const notificationStore = useNotificationStore()

const qty = ref(1)
const isAdded = ref(false)
const isWishlisted = ref(false)
const activeThumbIdx = ref(0)
const addedItemMap = ref({})
const wishlistItemMap = ref({})

// Reviews & Ratings state
const productReviews = ref([])
const reviewMetrics = ref({
  total_reviews: 0,
  average_rating: 4.8,
  distribution: {
    '5': { count: 0, percentage: 0 },
    '4': { count: 0, percentage: 0 },
    '3': { count: 0, percentage: 0 },
    '2': { count: 0, percentage: 0 },
    '1': { count: 0, percentage: 0 },
  }
})
const loadingReviews = ref(false)
const showReviewModal = ref(false)
const submittingReview = ref(false)
const hoverStar = ref(0)
const helpfulVoted = ref({})

const reviewForm = reactive({
  rating: 5,
  title: '',
  comment: '',
  customer_name: '',
  customer_email: '',
})

function loadProduct() {
  const slug = route.params.slug || 'sk-ii-facial-treatment-essence'
  productStore.fetchProductBySlug(slug)
}

async function fetchReviews(productId) {
  if (!productId) return
  loadingReviews.value = true
  try {
    const res = await axios.get('/api/reviews', { params: { product_id: productId } })
    if (res.data?.status === 'success') {
      productReviews.value = res.data.data || []
      if (res.data.metrics) {
        reviewMetrics.value = res.data.metrics
      }
    }
  } catch (err) {
    console.error('Failed to load reviews:', err)
  } finally {
    loadingReviews.value = false
  }
}

onMounted(() => {
  loadProduct()
})

watch(() => route.params.slug, () => {
  loadProduct()
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

const product = computed(() => productStore.currentProduct)

watch(() => product.value?.id, (newId) => {
  if (newId) {
    fetchReviews(newId)
  }
}, { immediate: true })

const brandSlug = computed(() => {
  if (!product.value) return 'sk-ii'
  return product.value.brand.toLowerCase().replace(/[^a-z0-9]/g, '-')
})

// Thumbnails rail dynamically including product packshot
const productThumbs = computed(() => {
  const mainImg = product.value?.image_url || '/images/pdp-stage-sk2-hero.jpg'
  return [
    { url: mainImg, label: 'Main Formulation' },
    { url: '/images/pdp-model-radiant.jpg', label: 'Radiant Skin' },
    { url: '/images/search-droplet-macro.jpg', label: 'Texture Macro' },
    { url: '/images/brand-store-sk2-hero.jpg', label: 'Atelier Ritual' },
  ]
})

const activeMainImage = computed(() => {
  const thumbs = productThumbs.value
  return thumbs[activeThumbIdx.value]?.url || thumbs[0]?.url || '/images/pdp-stage-sk2-hero.jpg'
})

function selectThumb(idx) {
  activeThumbIdx.value = idx
}

function nextThumb() {
  activeThumbIdx.value = (activeThumbIdx.value + 1) % productThumbs.value.length
}

// Size options matching real product price
const selectedSizeIdx = ref(0)
const sizeOptions = computed(() => {
  const base = Number(product.value?.price || 45)
  return [
    { label: 'Standard (Full Size)', price: base },
    { label: 'Deluxe Atelier Edition', price: Math.round(base * 1.6) },
    { label: 'Travel Size', price: Math.max(10, Math.round(base * 0.6)) },
  ]
})
const selectedSize = computed(() => sizeOptions.value[selectedSizeIdx.value] || sizeOptions.value[0])

function increaseQty() {
  qty.value++
}
function decreaseQty() {
  if (qty.value > 1) qty.value--
}

function handleAddToCart() {
  if (!product.value) return
  cartStore.addItem({
    ...product.value,
    price: selectedSize.value.price,
    selectedSize: selectedSize.value.label,
  }, qty.value)

  isAdded.value = true
  setTimeout(() => {
    isAdded.value = false
  }, 2000)
}

// Mid-tabs
const activeMidTab = ref('details')

const midTabs = computed(() => [
  { id: 'details', label: 'Product Details' },
  { id: 'ingredients', label: 'Ingredients' },
  { id: 'how-to-use', label: 'How to Use' },
  { id: 'benefits', label: 'Benefits' },
  { id: 'reviews', label: `Reviews (${reviewMetrics.value.total_reviews || product.value?.reviews || '7'})` },
  { id: 'qa', label: 'Q&A (28)' },
])

function openWriteReview() {
  if (authStore.user) {
    reviewForm.customer_name = authStore.userName || 'Sreynich Chan'
    reviewForm.customer_email = authStore.userEmail || 'sreynich.chan@example.com'
  } else {
    reviewForm.customer_name = 'Luméa Patron'
    reviewForm.customer_email = 'patron@example.com'
  }
  showReviewModal.value = true
}

async function submitReview() {
  if (!reviewForm.title || !reviewForm.comment) {
    notificationStore.addToast('Please enter both a title and review comment.', 'error')
    return
  }
  submittingReview.value = true
  try {
    const payload = {
      product_id: product.value?.id || 201,
      rating: reviewForm.rating,
      title: reviewForm.title,
      comment: reviewForm.comment,
      customer_name: reviewForm.customer_name || 'Luméa Patron',
      customer_email: reviewForm.customer_email || 'patron@example.com',
      customer_avatar: authStore.user?.avatar || '/images/avatar-sreynich.jpg'
    }
    const res = await axios.post('/api/reviews', payload)
    if (res.data?.status === 'success') {
      notificationStore.addToast('Thank you! Your review has been recorded.', 'success')
      showReviewModal.value = false
      reviewForm.title = ''
      reviewForm.comment = ''
      if (product.value?.id) {
        await fetchReviews(product.value.id)
      }
    }
  } catch (err) {
    notificationStore.addToast('Failed to submit review. Please try again.', 'error')
  } finally {
    submittingReview.value = false
  }
}

async function voteHelpful(rev) {
  if (helpfulVoted.value[rev.id]) return
  try {
    helpfulVoted.value[rev.id] = true
    rev.helpful_count = (rev.helpful_count || 0) + 1
    await axios.post(`/api/reviews/${rev.id}/helpful`)
    notificationStore.addToast('Marked review as helpful', 'success')
  } catch (err) {
    // Optimistically updated
  }
}

// You May Also Like matching Product Details.png
const youMayAlsoLike = computed(() => {
  return productStore.allCatalogProducts
    .filter((p) => p.brand === 'SK-II' && p.id !== product.value?.id)
    .slice(0, 6)
})

function isItemAdded(id) {
  return !!addedItemMap.value[id]
}
function handleAddToCartItem(item) {
  cartStore.addItem(item)
  addedItemMap.value[item.id] = true
  setTimeout(() => {
    addedItemMap.value[item.id] = false
  }, 2000)
}

function isWishlistedItem(id) {
  return !!wishlistItemMap.value[id]
}
function toggleItemWishlist(id) {
  wishlistItemMap.value[id] = !wishlistItemMap.value[id]
}
</script>

<style scoped>
.product-detail-page {
  padding-bottom: 5rem;
  background-color: #FAF8F5;
  min-height: 100vh;
}

/* Breadcrumbs */
.breadcrumb-container {
  padding-top: 1rem;
  padding-bottom: 1rem;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
}

.breadcrumb-link {
  color: #8E4A3E;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s ease;
}

.breadcrumb-link:hover {
  color: #73382E;
  text-decoration: underline;
}

.breadcrumb-sep {
  color: #8E4A3E;
}

.breadcrumb-current {
  color: #1C1917;
  font-weight: 600;
}

/* 3-Column Stage Grid */
.stage-container {
  margin-bottom: 3rem;
}

.pdp-layout-grid {
  display: grid;
  grid-template-columns: 460px 1fr 340px;
  gap: 2.25rem;
  align-items: start;
}

/* Gallery Column */
.gallery-column {
  display: flex;
  gap: 1rem;
}

.thumbnail-rail {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  width: 65px;
  flex-shrink: 0;
}

.thumb-box-btn {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 8px;
  padding: 0.25rem;
  height: 65px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  transition: all 0.15s ease;
}

.thumb-box-btn:hover {
  border-color: #8E4A3E;
}

.thumb-box-btn.active {
  border-color: #8E4A3E;
  box-shadow: 0 0 0 1px #8E4A3E;
}

.thumb-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.thumb-down-btn {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 8px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #78716C;
  cursor: pointer;
}

.main-stage-card {
  flex: 1;
  background: linear-gradient(135deg, #FBF2EC 0%, #F5E8DE 100%);
  border: 1px solid rgba(196, 98, 60, 0.15);
  border-radius: 18px;
  padding: 1.75rem;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 480px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
}

.stage-top-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 2;
}

.gold-best-badge {
  display: inline-block;
  background: #D97706;
  color: #FFFFFF;
  font-size: 0.68rem;
  font-weight: 700;
  padding: 0.35rem 0.65rem;
  border-radius: 50%;
  text-align: center;
  line-height: 1.15;
}

.stage-script-header {
  position: absolute;
  top: 24px;
  left: 20px;
  z-index: 2;
}

.stage-script-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-style: italic;
  font-size: 1.35rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.25;
}

.stage-center-img-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 340px;
  margin: auto 0;
}

.stage-hero-packshot {
  max-width: 90%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 12px;
}

.stage-benefit-icons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  position: absolute;
  bottom: 24px;
  left: 20px;
}

.st-benefit-item {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.76rem;
  font-weight: 600;
  color: #1C1917;
}

/* Center Purchase Column */
.purchase-column {
  display: flex;
  flex-direction: column;
}

.pdp-brand-header {
  margin-bottom: 0.35rem;
}

.brand-link-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.45rem;
  font-weight: 900;
  color: #B91C1C;
  text-decoration: none;
  letter-spacing: 0.05em;
}

.pdp-product-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.15rem;
  font-weight: 700;
  color: #1C1917;
  line-height: 1.2;
  margin-bottom: 0.35rem;
}

.pdp-formula-sub {
  font-size: 0.9rem;
  color: #78716C;
  margin-bottom: 0.85rem;
}

.pdp-rating-row {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  margin-bottom: 0.85rem;
}

.rating-stars {
  display: flex;
  gap: 0.15rem;
}

.star-gold {
  color: #F59E0B;
  fill: #F59E0B;
}

.rating-score {
  font-weight: 700;
  color: #1C1917;
}

.rating-count {
  color: #78716C;
}

.pipe-sep {
  color: #C4B5AA;
}

.sold-count {
  font-weight: 600;
  color: #1C1917;
}

.pdp-best-seller-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
}

.tag-hash {
  background: #8E4A3E;
  color: #FFFFFF;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
}

.tag-cat {
  font-size: 0.78rem;
  color: #78716C;
}

.pdp-price-row {
  margin-bottom: 1rem;
}

.pdp-main-price {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: #1C1917;
}

.pdp-bio-paragraph {
  font-size: 0.88rem;
  line-height: 1.6;
  color: #78716C;
  margin-bottom: 1.5rem;
}

/* Size Pills */
.pdp-size-section {
  margin-bottom: 1.25rem;
}

.size-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.5rem;
}

.size-options-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.75rem;
}

.size-pill-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 8px;
  padding: 0.75rem 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.size-pill-card.active {
  border-color: #1C1917;
  border-width: 1.5px;
  background: #FAF8F5;
}

.size-name {
  font-size: 0.8rem;
  font-weight: 700;
  color: #1C1917;
}

.size-cost {
  font-size: 0.76rem;
  color: #78716C;
}

/* Quantity */
.pdp-qty-section {
  margin-bottom: 1.5rem;
}

.qty-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.5rem;
}

.qty-stepper-box {
  display: inline-flex;
  align-items: center;
  border: 1px solid #EAE5DF;
  border-radius: 6px;
  background: #FFFFFF;
}

.qty-step-btn {
  background: none;
  border: none;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1C1917;
  cursor: pointer;
}

.qty-step-btn:disabled {
  color: #C4B5AA;
}

.qty-value {
  width: 38px;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 700;
}

/* Terracotta Buttons */
.pdp-action-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.75rem;
}

.btn-pdp-add-cart {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  border-radius: 6px;
  padding: 0.85rem;
  font-size: 0.92rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-pdp-add-cart:hover {
  background: #7A3B30;
}

.btn-pdp-add-cart.is-added {
  background: #2E7D32;
}

.btn-pdp-wishlist {
  background: #FFFFFF;
  color: #1C1917;
  border: 1px solid #EAE5DF;
  border-radius: 6px;
  padding: 0.75rem;
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  cursor: pointer;
}

.btn-pdp-wishlist.active {
  color: #DC2626;
}

/* Trust Row */
.pdp-trust-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 1.25rem;
  border-top: 1px solid #EAE5DF;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.trust-icon {
  color: #8E4A3E;
}

.trust-text {
  display: flex;
  flex-direction: column;
}

.trust-text strong {
  font-size: 0.74rem;
  color: #1C1917;
}

.trust-text span {
  font-size: 0.68rem;
  color: #78716C;
}

/* Right Sidebar Column */
.sidebar-column {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.brand-store-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.25rem;
}

.store-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.store-card-brand {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #1C1917;
}

.view-store-link {
  font-size: 0.76rem;
  font-weight: 700;
  color: #8E4A3E;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.store-card-body {
  display: flex;
  gap: 0.85rem;
  align-items: flex-start;
}

.store-badge-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.store-info-text {
  display: flex;
  flex-direction: column;
}

.store-name-strong {
  font-size: 0.85rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.store-brief {
  font-size: 0.75rem;
  line-height: 1.45;
  color: #78716C;
  margin-bottom: 0.65rem;
}

.store-internal-links {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.s-link {
  font-size: 0.74rem;
  font-weight: 600;
  color: #8E4A3E;
  text-decoration: none;
}

/* Assurances Card */
.assurances-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.assurance-line {
  display: flex;
  gap: 0.65rem;
  align-items: flex-start;
}

.assure-icon {
  color: #8E4A3E;
  flex-shrink: 0;
  margin-top: 0.15rem;
}

.assure-text {
  display: flex;
  flex-direction: column;
}

.assure-text strong {
  font-size: 0.78rem;
  color: #1C1917;
}

.assure-text span {
  font-size: 0.7rem;
  color: #78716C;
}

/* Points Card */
.lumea-points-card {
  background: #FAF3EE;
  border: 1px solid rgba(196, 98, 60, 0.2);
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.points-icon-wrap {
  color: #8E4A3E;
}

.points-text-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.points-text-wrap strong {
  font-size: 0.8rem;
  color: #1C1917;
}

.points-text-wrap span {
  font-size: 0.72rem;
  color: #78716C;
}

.points-help {
  color: #9C948B;
}

/* Mid-Page Tabs Section */
.mid-tabs-container {
  margin-bottom: 3.5rem;
}

.mid-tabs-bar {
  display: flex;
  border-bottom: 1px solid #EAE5DF;
  margin-bottom: 2rem;
  overflow-x: auto;
}

.mid-tab-btn {
  background: none;
  border: none;
  padding: 0.85rem 1.5rem;
  font-size: 0.88rem;
  font-weight: 600;
  color: #78716C;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  transition: all 0.15s ease;
}

.mid-tab-btn:hover {
  color: #8E4A3E;
}

.mid-tab-btn.active {
  color: #1C1917;
  font-weight: 700;
  border-bottom-color: #8E4A3E;
}

.tab-three-cols {
  display: grid;
  grid-template-columns: 280px 1fr 340px;
  gap: 2.5rem;
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2rem;
}

.panel-section-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 1.25rem;
}

.pdp-spec-table {
  width: 100%;
  border-collapse: collapse;
}

.pdp-spec-table th,
.pdp-spec-table td {
  padding: 0.6rem 0;
  font-size: 0.82rem;
  border-bottom: 1px solid #F4EFEB;
  text-align: left;
}

.pdp-spec-table th {
  color: #1C1917;
  font-weight: 700;
  width: 110px;
}

.pdp-spec-table td {
  color: #78716C;
}

.about-lead {
  font-size: 0.85rem;
  line-height: 1.6;
  color: #78716C;
  margin-bottom: 1rem;
}

.checklist-items {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-top: 1.25rem;
}

.check-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
  color: #1C1917;
}

.check-icon {
  color: #8E4A3E;
  flex-shrink: 0;
}

/* Testimonial Card */
.testimonial-card-box {
  background: linear-gradient(135deg, #FDF4F0 0%, #F8E8E0 100%);
  border: 1px solid rgba(196, 98, 60, 0.15);
  border-radius: 12px;
  display: flex;
  overflow: hidden;
  height: 100%;
}

.testimonial-text-side {
  flex: 1;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.test-heading {
  font-family: 'Playfair Display', Georgia, serif;
  font-style: italic;
  font-size: 1.2rem;
  font-weight: 700;
  color: #8E4A3E;
  line-height: 1.2;
}

.test-quote {
  font-size: 0.78rem;
  line-height: 1.45;
  color: #1C1917;
  margin: 0.5rem 0;
  font-weight: 500;
}

.test-buyer {
  font-size: 0.72rem;
  color: #78716C;
}

.test-stars {
  display: flex;
  gap: 0.15rem;
  margin-top: 0.25rem;
}

.testimonial-img-side {
  width: 140px;
  overflow: hidden;
}

.testimonial-img-side img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* You May Also Like matching Product Details.png */
.also-like-container {
  margin-bottom: 4rem;
}

.also-like-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.also-like-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.65rem;
  font-weight: 700;
  color: #1C1917;
}

.see-more-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: #8E4A3E;
  text-decoration: none;
}

.also-like-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 1rem;
}

.also-like-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  position: relative;
  transition: all 0.2s ease;
}

.also-like-card:hover {
  border-color: #8E4A3E;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(40, 20, 10, 0.06);
}

.also-wishlist-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  color: #9C948B;
  cursor: pointer;
  z-index: 2;
}

.also-wishlist-btn.active {
  color: #DC2626;
  fill: #DC2626;
}

.also-img-wrap {
  height: 125px;
  background: #FAF8F5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  padding: 0.4rem;
}

.also-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.also-body {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.also-brand {
  font-size: 0.72rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.also-name-link {
  text-decoration: none;
  color: inherit;
  margin-bottom: 0.35rem;
}

.also-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: #1C1917;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 2.1rem;
}

.also-rating {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.72rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.5rem;
}

.also-revs {
  color: #78716C;
  font-weight: 400;
}

.also-bottom-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 0.5rem;
  border-top: 1px solid #F4EFEB;
}

.also-price {
  font-size: 0.95rem;
  font-weight: 800;
  color: #1C1917;
}

.also-cart-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s ease;
}

.also-cart-btn:hover {
  background: #7A3B30;
}

.also-cart-btn.is-added {
  background: #2E7D32;
}

/* Tab 2: Ingredients */
.tab-ingredients-panel {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2rem;
}

.active-item-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.active-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.active-badge {
  background: #FAF3EE;
  color: #8E4A3E;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  white-space: nowrap;
}

.active-text strong {
  display: block;
  font-size: 0.82rem;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.active-text span {
  font-size: 0.76rem;
  color: #78716C;
  line-height: 1.45;
}

.inci-lead {
  font-size: 0.84rem;
  line-height: 1.6;
  color: #44403C;
  margin-bottom: 0.5rem;
  font-family: monospace;
  background: #FAF8F5;
  padding: 0.75rem;
  border-radius: 8px;
  border: 1px solid #EFEAE4;
}

.inci-footnote {
  font-size: 0.72rem;
  color: #78716C;
  font-style: italic;
  margin-bottom: 1.25rem;
}

.formulation-notes {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.note-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: #FAF3EE;
  color: #8E4A3E;
  font-size: 0.74rem;
  font-weight: 600;
  padding: 0.35rem 0.65rem;
  border-radius: 20px;
}

.purity-pledge-card {
  background: linear-gradient(135deg, #FBF2EC 0%, #F5E8DE 100%);
  border: 1px solid rgba(196, 98, 60, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
}

.purity-icon {
  color: #8E4A3E;
  margin-bottom: 0.5rem;
}

.purity-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #8E4A3E;
  margin-bottom: 0.75rem;
}

.purity-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.purity-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  color: #1C1917;
  font-weight: 500;
}

.purity-list li svg {
  color: #8E4A3E;
}

/* Tab 3: How to Use */
.tab-how-to-use-panel {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2.25rem;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.ritual-steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.ritual-step-card {
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.5rem;
  position: relative;
}

.step-num-badge {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.4rem;
  font-weight: 700;
  color: #8E4A3E;
  margin-bottom: 0.5rem;
}

.step-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.5rem;
}

.step-desc {
  font-size: 0.8rem;
  line-height: 1.5;
  color: #78716C;
}

.ritual-pro-tip-box {
  background: #FAF3EE;
  border-left: 3px solid #8E4A3E;
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.tip-icon-col {
  color: #8E4A3E;
  margin-top: 0.2rem;
}

.tip-content strong {
  display: block;
  font-size: 0.85rem;
  color: #8E4A3E;
  margin-bottom: 0.25rem;
}

.tip-content p {
  font-size: 0.8rem;
  color: #44403C;
  line-height: 1.5;
  margin: 0;
}

/* Tab 4: Benefits */
.tab-benefits-panel {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2rem;
}

.benefits-metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
}

.benefit-kpi-card {
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.5rem 1.25rem;
  text-align: center;
  transition: all 0.2s ease;
}

.benefit-kpi-card:hover {
  border-color: #8E4A3E;
  transform: translateY(-2px);
}

.kpi-num {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 2.2rem;
  font-weight: 700;
  color: #8E4A3E;
  margin-bottom: 0.35rem;
}

.kpi-label {
  font-size: 0.88rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.5rem;
}

.kpi-sub {
  font-size: 0.76rem;
  line-height: 1.45;
  color: #78716C;
  margin: 0;
}

/* Tab 5: Reviews */
.tab-reviews-panel {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.reviews-summary-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2rem;
  display: grid;
  grid-template-columns: 240px 1fr 260px;
  gap: 2rem;
  align-items: center;
}

.overall-rating-block {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-right: 1px solid #EAE5DF;
  padding-right: 1.5rem;
}

.big-score {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 3.5rem;
  font-weight: 800;
  color: #1C1917;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stars-gold-row {
  display: flex;
  gap: 0.2rem;
  margin-bottom: 0.5rem;
}

.total-rev-caption {
  font-size: 0.78rem;
  color: #78716C;
}

.rating-breakdown-bars {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.star-bar-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.76rem;
}

.star-num {
  width: 50px;
  font-weight: 600;
  color: #1C1917;
}

.bar-track {
  flex: 1;
  height: 8px;
  background: #F0ECE7;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: #8E4A3E;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.bar-count {
  width: 30px;
  text-align: right;
  color: #78716C;
}

.write-review-cta-col {
  border-left: 1px solid #EAE5DF;
  padding-left: 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.write-review-cta-col h4 {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.1rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.35rem;
}

.write-review-cta-col p {
  font-size: 0.76rem;
  color: #78716C;
  line-height: 1.4;
  margin-bottom: 1rem;
}

.btn-write-review {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-write-review:hover {
  background: #73382E;
}

.reviews-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 3rem;
  color: #78716C;
  font-size: 0.85rem;
}

.spinner-atelier {
  width: 20px;
  height: 20px;
  border: 2px solid #EAE5DF;
  border-top-color: #8E4A3E;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-reviews-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 3rem 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.empty-rev-icon {
  color: #C4B5AA;
  margin-bottom: 0.5rem;
}

.btn-write-review-clean {
  background: #8E4A3E;
  color: #FFFFFF;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  margin-top: 0.75rem;
}

.reviews-list-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-item-card {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.review-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.reviewer-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.reviewer-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #EAE5DF;
}

.reviewer-name-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.reviewer-name-row strong {
  font-size: 0.85rem;
  color: #1C1917;
}

.badge-verified {
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  background: #ECFDF5;
  color: #065F46;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

.review-date {
  font-size: 0.72rem;
  color: #9C948B;
}

.review-stars-row {
  display: flex;
  gap: 0.15rem;
}

.star-muted {
  color: #E5E7EB;
  fill: #E5E7EB;
}

.review-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1rem;
  font-weight: 700;
  color: #1C1917;
  margin: 0;
}

.review-comment {
  font-size: 0.82rem;
  line-height: 1.6;
  color: #57534E;
  margin: 0;
}

.curator-reply-box {
  background: #FAF3EE;
  border-left: 3px solid #8E4A3E;
  border-radius: 6px;
  padding: 0.85rem 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.75rem;
}

.reply-icon {
  color: #8E4A3E;
}

.reply-header strong {
  color: #8E4A3E;
}

.reply-date {
  color: #9C948B;
  font-size: 0.7rem;
  margin-left: auto;
}

.reply-text {
  font-size: 0.78rem;
  line-height: 1.5;
  color: #44403C;
  margin: 0;
}

.review-footer-row {
  display: flex;
  align-items: center;
  padding-top: 0.5rem;
  border-top: 1px solid #FAF8F5;
}

.btn-helpful {
  background: none;
  border: 1px solid #EAE5DF;
  border-radius: 6px;
  padding: 0.3rem 0.65rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.72rem;
  font-weight: 600;
  color: #78716C;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-helpful:hover {
  border-color: #8E4A3E;
  color: #8E4A3E;
}

.btn-helpful.voted {
  background: #FAF3EE;
  border-color: #8E4A3E;
  color: #8E4A3E;
}

/* Tab 6: Q&A */
.tab-qa-panel {
  background: #FFFFFF;
  border: 1px solid #EAE5DF;
  border-radius: 14px;
  padding: 2rem;
}

.qa-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.qa-item {
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
}

.qa-question {
  font-size: 0.88rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.5rem;
}

.qa-answer {
  font-size: 0.8rem;
  line-height: 1.55;
  color: #57534E;
  margin: 0;
}

/* Modal Backdrop & Review Form */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(28, 25, 23, 0.6);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.review-modal-card {
  background: #FFFFFF;
  border-radius: 16px;
  width: 100%;
  max-width: 540px;
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.modal-title {
  font-family: 'Playfair Display', Georgia, serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #1C1917;
  margin-bottom: 0.2rem;
}

.modal-subtitle {
  font-size: 0.78rem;
  color: #78716C;
}

.btn-close-modal {
  background: none;
  border: none;
  color: #9C948B;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 6px;
  transition: color 0.15s ease;
}

.btn-close-modal:hover {
  color: #1C1917;
}

.review-modal-form {
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: #1C1917;
}

.star-rating-selector {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.star-pick-btn {
  background: none;
  border: none;
  padding: 0.15rem;
  cursor: pointer;
}

.star-gold-active {
  color: #F59E0B;
  fill: #F59E0B;
}

.star-inactive {
  color: #E5E7EB;
  fill: #E5E7EB;
}

.star-rating-label {
  margin-left: 0.75rem;
  font-size: 0.82rem;
  font-weight: 700;
  color: #8E4A3E;
}

.form-input,
.form-textarea {
  width: 100%;
  background: #FAF8F5;
  border: 1px solid #EAE5DF;
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  font-size: 0.82rem;
  color: #1C1917;
  outline: none;
  transition: border-color 0.15s ease;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #8E4A3E;
  background: #FFFFFF;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.btn-cancel {
  background: #F4EFEB;
  border: none;
  padding: 0.65rem 1.25rem;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #78716C;
  cursor: pointer;
}

.btn-submit-review {
  background: #8E4A3E;
  border: none;
  padding: 0.65rem 1.5rem;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  color: #FFFFFF;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-submit-review:hover {
  background: #73382E;
}

/* Responsive */
@media (max-width: 1200px) {
  .pdp-layout-grid {
    grid-template-columns: 380px 1fr;
  }
  .sidebar-column {
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
  }
  .tab-three-cols {
    grid-template-columns: 1fr;
  }
  .also-like-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 800px) {
  .pdp-layout-grid {
    grid-template-columns: 1fr;
  }
  .gallery-column {
    flex-direction: column-reverse;
  }
  .thumbnail-rail {
    flex-direction: row;
    width: 100%;
  }
  .sidebar-column {
    grid-template-columns: 1fr;
  }
  .also-like-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
