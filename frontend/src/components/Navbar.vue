<template>
  <header class="lumea-beauty-header" ref="headerRef">
    <!-- Format-matching Single-Row Header Bar -->
    <div class="header-main-row">
      <div class="container-fluid header-inner">
        <!-- Left: Mobile Menu Toggle & Brand Logo -->
        <div class="header-left">
          <button
            class="mobile-toggle"
            @click="mobileMenuOpen = !mobileMenuOpen"
            aria-label="Toggle Navigation Menu"
          >
            <Menu v-if="!mobileMenuOpen" :size="22" />
            <X v-else :size="22" />
          </button>

          <router-link to="/" class="brand-logo" aria-label="Luméa - Beauty Lives Here">
            <img src="/images/logo-lumea.png" alt="Luméa - Beauty Lives Here" class="brand-logo-img" />
          </router-link>
        </div>

        <!-- Center: Primary Navigation Links matching Format -->
        <nav class="desktop-nav-links">
          <!-- Shop Dropdown -->
          <div
            class="nav-dropdown-item"
            @mouseenter="activeDropdown = 'shop'"
            @mouseleave="activeDropdown = null"
          >
            <router-link
              to="/shop"
              class="nav-link"
              :class="{ 'is-active': isShopActive }"
              @click="closeMenu"
            >
              <span>{{ localeStore.t('nav.shop') }}</span>
              <ChevronDown :size="13" class="caret-icon" />
            </router-link>
            <div v-show="activeDropdown === 'shop'" class="dropdown-menu">
              <router-link to="/shop" class="dropdown-link featured-link" @click="closeMenu">
                {{ localeStore.t('nav.all_products') }}
              </router-link>
              <router-link to="/category/cleansers" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.cleansers') }}
              </router-link>
              <router-link to="/category/toners" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.toners') }}
              </router-link>
              <router-link to="/category/serums" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.serums') }}
              </router-link>
              <router-link to="/category/moisturizers" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.moisturizers') }}
              </router-link>
              <router-link to="/category/sunscreens" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.sunscreens') }}
              </router-link>
              <router-link to="/category/masks" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.masks') }}
              </router-link>
              <router-link to="/category/treatments" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.treatments') }}
              </router-link>
              <router-link to="/category/kits" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.kits') }}
              </router-link>
            </div>
          </div>

          <!-- Brands Dropdown -->
          <div
            class="nav-dropdown-item"
            @mouseenter="activeDropdown = 'brands'"
            @mouseleave="activeDropdown = null"
          >
            <router-link
              to="/brands"
              class="nav-link"
              :class="{ 'is-active': isBrandsActive }"
              @click="closeMenu"
            >
              <span>{{ localeStore.t('nav.brands') }}</span>
              <ChevronDown :size="13" class="caret-icon" />
            </router-link>
            <div v-show="activeDropdown === 'brands'" class="dropdown-menu">
              <router-link to="/brands" class="dropdown-link featured-link" @click="closeMenu">
                {{ localeStore.t('nav.browse_brands') }}
              </router-link>
              <router-link to="/brand/sk-ii" class="dropdown-link" @click="closeMenu">SK-II Official Store</router-link>
              <router-link to="/brand/innisfree" class="dropdown-link" @click="closeMenu">Innisfree Official Store</router-link>
              <router-link to="/brand/the-ordinary" class="dropdown-link" @click="closeMenu">The Ordinary</router-link>
              <router-link to="/brand/laneige" class="dropdown-link" @click="closeMenu">LANEIGE</router-link>
              <router-link to="/brand/cerave" class="dropdown-link" @click="closeMenu">CeraVe</router-link>
              <router-link to="/brand/la-roche-posay" class="dropdown-link" @click="closeMenu">La Roche-Posay</router-link>
              <router-link to="/brand/bioderma" class="dropdown-link" @click="closeMenu">Bioderma</router-link>
              <router-link to="/brand/cosrx" class="dropdown-link" @click="closeMenu">COSRX</router-link>
              <router-link to="/brand/beauty-of-joseon" class="dropdown-link" @click="closeMenu">Beauty of Joseon</router-link>
            </div>
          </div>

          <!-- Skin Concerns & Types Dropdown -->
          <div
            class="nav-dropdown-item"
            @mouseenter="activeDropdown = 'concerns'"
            @mouseleave="activeDropdown = null"
          >
            <router-link
              to="/concerns"
              class="nav-link"
              :class="{ 'is-active': route.path === '/concerns' }"
              @click="closeMenu"
            >
              <span>{{ localeStore.t('nav.concerns') }}</span>
              <ChevronDown :size="13" class="caret-icon" />
            </router-link>
            <div v-show="activeDropdown === 'concerns'" class="dropdown-menu">
              <router-link to="/concerns" class="dropdown-link featured-link" @click="closeMenu">
                {{ localeStore.t('nav.explore_concerns') }}
              </router-link>
              <div class="dropdown-section-label">{{ localeStore.t('nav.by_concern') }}</div>
              <router-link to="/concerns?concern=dryness" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.dryness') }}
              </router-link>
              <router-link to="/concerns?concern=dark-spots" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.dark_spots') }}
              </router-link>
              <router-link to="/concerns?concern=aging" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.aging') }}
              </router-link>
              <router-link to="/concerns?concern=acne" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.acne') }}
              </router-link>
              <router-link to="/concerns?concern=sensitivity" class="dropdown-link" @click="closeMenu">
                {{ localeStore.t('nav.sensitivity') }}
              </router-link>
              <div class="dropdown-section-label">{{ localeStore.t('nav.by_type') }}</div>
              <router-link to="/concerns?type=dry" class="dropdown-link" @click="closeMenu">{{ localeStore.t('nav.dry_skin') }}</router-link>
              <router-link to="/concerns?type=oily" class="dropdown-link" @click="closeMenu">{{ localeStore.t('nav.oily_skin') }}</router-link>
              <router-link to="/concerns?type=combination" class="dropdown-link" @click="closeMenu">{{ localeStore.t('nav.combination_skin') }}</router-link>
              <router-link to="/concerns?type=sensitive" class="dropdown-link" @click="closeMenu">{{ localeStore.t('nav.sensitive_skin') }}</router-link>
            </div>
          </div>

          <!-- Direct Links -->
          <router-link
            to="/best-sellers"
            class="nav-link"
            :class="{ 'is-active': route.path === '/best-sellers' }"
            @click="closeMenu"
          >
            {{ localeStore.t('nav.best_sellers') }}
          </router-link>
          <router-link
            to="/new-arrivals"
            class="nav-link"
            :class="{ 'is-active': route.path === '/new-arrivals' }"
            @click="closeMenu"
          >
            {{ localeStore.t('nav.new_arrivals') }}
          </router-link>
          <router-link
            to="/deals"
            class="nav-link highlight-deals"
            :class="{ 'is-active': route.path === '/deals' }"
            @click="closeMenu"
          >
            {{ localeStore.t('nav.deals') }}
          </router-link>
          <router-link
            to="/articles"
            class="nav-link"
            :class="{ 'is-active': route.path.startsWith('/articles') }"
            @click="closeMenu"
          >
            {{ localeStore.t('nav.articles') }}
          </router-link>
          <router-link
            to="/quiz"
            class="nav-link nav-quiz-badge"
            :class="{ 'is-active': route.path.startsWith('/quiz') || route.path === '/routine' }"
            @click="closeMenu"
          >
            <Sparkles :size="13" class="quiz-badge-sparkle" />
            <span>{{ localeStore.t('nav.skin_quiz') }}</span>
          </router-link>
        </nav>

        <!-- Far Right: Format Minimal Icons (Language & Currency, Notifications, Wishlist, Cart with Badge, Account) -->
        <div class="header-action-icons">
          <!-- Notification Bell Icon with Badge -->
          <button
            type="button"
            class="header-icon-btn notif-icon-btn"
            @click="notifStore.toggleDrawer"
            title="Atelier Feed & Notifications"
            aria-label="Atelier Feed & Notifications"
          >
            <Bell :size="20" :stroke-width="1.8" />
            <span v-if="notifStore.unreadCount > 0" class="notif-circle-badge">
              {{ notifStore.unreadCount }}
            </span>
            <span v-if="notifStore.unreadCount > 0" class="notif-pulse-dot"></span>
          </button>

          <!-- Language & Currency Switcher Pill -->
          <div class="locale-switcher-wrap" ref="localeDropdownRef">
            <button
              class="locale-pill-btn"
              type="button"
              @click.stop="toggleLocaleMenu"
              aria-label="Change Language and Currency"
              :title="`Language: ${currentLanguageLabel} | Currency: ${localeStore.currentCurrency}`"
            >
              <Globe :size="15" class="locale-globe-svg" />
              <FlagIcon :locale="localeStore.currentLocale" class="locale-flag-icon" />
              <span class="locale-lang-code">{{ currentLanguageLabel }}</span>
              <span class="locale-divider-dot">·</span>
              <span class="locale-currency-code">{{ localeStore.currencySymbol }} {{ localeStore.currentCurrency }}</span>
              <ChevronDown :size="11" class="locale-caret-icon" :class="{ 'is-open': localeMenuOpen }" />
            </button>

            <!-- Luxury Atelier Popup Dropdown -->
            <div v-show="localeMenuOpen" class="locale-popover-menu" @click.stop>
              <!-- 1. Language Options -->
              <div class="popover-section">
                <div class="popover-section-header">
                  <span class="popover-heading">{{ localeStore.t('common.language') }}</span>
                  <span class="popover-hint">Auto Currency</span>
                </div>
                
                <div class="popover-options-list">
                  <!-- English -->
                  <button
                    type="button"
                    class="popover-option-item"
                    :class="{ active: localeStore.currentLocale === 'en' }"
                    @click="selectLanguage('en')"
                  >
                    <FlagIcon locale="en" class="pop-flag" />
                    <div class="pop-details">
                      <span class="pop-name">English</span>
                      <span class="pop-sub">Default (USD $)</span>
                    </div>
                    <Check v-if="localeStore.currentLocale === 'en'" :size="14" class="pop-check" />
                  </button>

                  <!-- Khmer -->
                  <button
                    type="button"
                    class="popover-option-item"
                    :class="{ active: localeStore.currentLocale === 'km' }"
                    @click="selectLanguage('km')"
                  >
                    <FlagIcon locale="km" class="pop-flag" />
                    <div class="pop-details">
                      <span class="pop-name">ភាសាខ្មែរ (Khmer)</span>
                      <span class="pop-sub">ប្តូរតម្លៃជាប្រាក់រៀល (៛ KHR)</span>
                    </div>
                    <Check v-if="localeStore.currentLocale === 'km'" :size="14" class="pop-check" />
                  </button>

                  <!-- Chinese -->
                  <button
                    type="button"
                    class="popover-option-item"
                    :class="{ active: localeStore.currentLocale === 'zh' }"
                    @click="selectLanguage('zh')"
                  >
                    <FlagIcon locale="zh" class="pop-flag" />
                    <div class="pop-details">
                      <span class="pop-name">简体中文 (Chinese)</span>
                      <span class="pop-sub">自动显示人民币 (¥ CNY)</span>
                    </div>
                    <Check v-if="localeStore.currentLocale === 'zh'" :size="14" class="pop-check" />
                  </button>
                </div>
              </div>

              <div class="popover-divider"></div>

              <!-- 2. Currency Options (Can change whenever user wants!) -->
              <div class="popover-section">
                <div class="popover-section-header">
                  <span class="popover-heading">{{ localeStore.t('common.currency') }}</span>
                  <span class="popover-hint">Can Change Anytime</span>
                </div>

                <div class="currency-chips-grid">
                  <button
                    type="button"
                    class="pop-curr-chip"
                    :class="{ active: localeStore.currentCurrency === 'USD' }"
                    @click="selectCurrency('USD')"
                  >
                    <span class="chip-sym">$</span>
                    <span class="chip-label">USD ($)</span>
                  </button>

                  <button
                    type="button"
                    class="pop-curr-chip"
                    :class="{ active: localeStore.currentCurrency === 'KHR' }"
                    @click="selectCurrency('KHR')"
                  >
                    <span class="chip-sym">៛</span>
                    <span class="chip-label">KHR (៛)</span>
                  </button>

                  <button
                    type="button"
                    class="pop-curr-chip"
                    :class="{ active: localeStore.currentCurrency === 'CNY' }"
                    @click="selectCurrency('CNY')"
                  >
                    <span class="chip-sym">¥</span>
                    <span class="chip-label">CNY (¥)</span>
                  </button>
                </div>

                <div class="popover-rate-footnote">
                  <span v-if="localeStore.currentCurrency === 'KHR'">
                    Official Atelier Rate: $1.00 USD ≈ 4,100 KHR (រៀល)
                  </span>
                  <span v-else-if="localeStore.currentCurrency === 'CNY'">
                    Official Atelier Rate: $1.00 USD ≈ 7.25 CNY (人民币)
                  </span>
                  <span v-else>
                    Base Atelier Tariff: USD ($)
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Wishlist Heart Icon with Count Badge -->
          <router-link
            to="/wishlist"
            class="header-icon-btn wishlist-icon-btn"
            :class="{ 'is-active': route.path === '/wishlist' }"
            title="Wishlist"
            aria-label="Wishlist"
          >
            <Heart :size="20" :stroke-width="1.8" />
            <span v-if="wishlistStore.totalItems > 0" class="wishlist-circle-badge">
              {{ wishlistStore.totalItems }}
            </span>
          </router-link>

          <!-- Shopping Bag Cart Icon with Terracotta Badge -->
          <button
            class="header-icon-btn cart-btn-pos"
            @click="cartStore.openDrawer"
            title="Shopping Cart"
            aria-label="Shopping Cart"
          >
            <ShoppingBag :size="20" :stroke-width="1.8" />
            <span class="cart-circle-badge">
              {{ cartStore.totalItems }}
            </span>
          </button>

          <!-- Account User Dropdown / Icon -->
          <div class="header-account-wrap" ref="accountDropdownRef">
            <button
              v-if="authStore.isAuthenticated"
              type="button"
              class="header-icon-btn account-icon-btn user-logged-in-btn"
              :class="{ 'is-active': accountMenuOpen || route.path.startsWith('/account') }"
              @click="toggleAccountMenu"
              title="My Account Menu"
              aria-label="My Account Menu"
            >
              <img v-if="authStore.userAvatar" :src="authStore.userAvatar" class="navbar-avatar-thumb" alt="Profile" />
              <UserCheck v-else :size="20" :stroke-width="1.8" />
            </button>
            <router-link
              v-else
              to="/login"
              class="header-icon-btn account-icon-btn"
              :class="{ 'is-active': route.path === '/login' }"
              title="Sign In"
              aria-label="Sign In"
            >
              <User :size="20" :stroke-width="1.8" />
            </router-link>

            <!-- Authenticated User Dropdown Menu -->
            <div v-if="accountMenuOpen && authStore.isAuthenticated" class="navbar-account-dropdown">
              <div class="dropdown-user-header">
                <strong>{{ authStore.userName }}</strong>
                <span>{{ authStore.userEmail }}</span>
                <span class="user-tier-pill-small">{{ authStore.user?.tier || 'Member' }}</span>
              </div>
              <div class="dropdown-divider"></div>
              <router-link to="/account" class="dropdown-menu-link" @click="accountMenuOpen = false">
                <Home :size="16" />
                <span>My Account</span>
              </router-link>
              <router-link to="/account/orders" class="dropdown-menu-link" @click="accountMenuOpen = false">
                <Package :size="16" />
                <span>Orders</span>
              </router-link>
              <router-link to="/account/profile" class="dropdown-menu-link" @click="accountMenuOpen = false">
                <Smile :size="16" />
                <span>Beauty Profile</span>
              </router-link>
              <router-link to="/routine" class="dropdown-menu-link" @click="accountMenuOpen = false">
                <Sparkles :size="16" />
                <span>Skincare Routine</span>
              </router-link>
              <div class="dropdown-divider"></div>
              <button type="button" class="dropdown-menu-link logout-link" @click="handleNavbarLogout">
                <LogOut :size="16" />
                <span>Log Out</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Slide-Down Drawer for Responsive Screens -->
    <div v-if="mobileMenuOpen" class="mobile-drawer-backdrop" @click.self="mobileMenuOpen = false">
      <div class="mobile-drawer-panel">
        <div class="mobile-drawer-header">
          <img src="/images/logo-lumea.png" alt="Luméa" class="mobile-logo-img" />
          <button class="mobile-close-btn" @click="mobileMenuOpen = false" aria-label="Close Menu">
            <X :size="20" />
          </button>
        </div>

        <div class="mobile-search-box">
          <form class="search-pill-form" @submit.prevent="handleSearch">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search products in shop..."
              class="search-pill-input"
            />
            <button type="submit" class="search-submit-btn" aria-label="Search">
              <Search :size="16" />
            </button>
          </form>
        </div>

        <!-- Mobile Notification Bar -->
        <div class="mobile-notif-shortcut-wrap">
          <button
            type="button"
            class="mobile-notif-shortcut-btn"
            @click="openNotifFromMobile"
          >
            <div class="m-notif-row">
              <Bell :size="17" class="m-notif-bell" />
              <span>Atelier Live Feed &amp; Updates</span>
            </div>
            <span v-if="notifStore.unreadCount > 0" class="m-notif-badge">
              {{ notifStore.unreadCount }} new
            </span>
          </button>
        </div>

        <nav class="mobile-nav-list">
          <router-link to="/shop" class="mobile-nav-item" @click="closeMenu">
            <span>{{ localeStore.t('nav.all_products') || 'Shop All Products' }}</span>
          </router-link>
          <router-link to="/category/cleansers" class="mobile-nav-subitem" @click="closeMenu">{{ localeStore.t('nav.cleansers') || 'Cleansers' }}</router-link>
          <router-link to="/category/toners" class="mobile-nav-subitem" @click="closeMenu">{{ localeStore.t('nav.toners') || 'Toners' }}</router-link>
          <router-link to="/category/serums" class="mobile-nav-subitem" @click="closeMenu">{{ localeStore.t('nav.serums') || 'Serums' }}</router-link>
          <router-link to="/category/moisturizers" class="mobile-nav-subitem" @click="closeMenu">{{ localeStore.t('nav.moisturizers') || 'Moisturizers' }}</router-link>

          <div class="mobile-divider"></div>

          <router-link to="/brands" class="mobile-nav-item" @click="closeMenu">
            <span>{{ localeStore.t('nav.browse_brands') || 'All Brands Directory' }}</span>
          </router-link>
          <router-link to="/brand/sk-ii" class="mobile-nav-subitem" @click="closeMenu">SK-II</router-link>
          <router-link to="/brand/innisfree" class="mobile-nav-subitem" @click="closeMenu">Innisfree</router-link>
          <router-link to="/brand/the-ordinary" class="mobile-nav-subitem" @click="closeMenu">The Ordinary</router-link>
          <router-link to="/brand/laneige" class="mobile-nav-subitem" @click="closeMenu">LANEIGE</router-link>
          <router-link to="/brand/cerave" class="mobile-nav-subitem" @click="closeMenu">CeraVe</router-link>

          <div class="mobile-divider"></div>

          <router-link to="/best-sellers" class="mobile-nav-item" @click="closeMenu">{{ localeStore.t('nav.best_sellers') || 'Best Sellers' }}</router-link>
          <router-link to="/new-arrivals" class="mobile-nav-item" @click="closeMenu">{{ localeStore.t('nav.new_arrivals') || 'New Arrivals' }}</router-link>
          <router-link to="/deals" class="mobile-nav-item highlight-deals" @click="closeMenu">{{ localeStore.t('nav.deals') || 'Special Offers & Deals' }}</router-link>
          <router-link to="/articles" class="mobile-nav-item" @click="closeMenu">{{ localeStore.t('nav.articles') || 'Skincare Journal' }}</router-link>
          <router-link to="/quiz" class="mobile-nav-item highlight-quiz" @click="closeMenu">
            <Sparkles :size="16" class="mobile-quiz-sparkle" />
            <span>{{ localeStore.t('nav.skin_quiz') || 'Skin Diagnostic Quiz' }}</span>
          </router-link>
          <router-link to="/returns/request" class="mobile-nav-item" @click="closeMenu">Returns &amp; Refunds</router-link>
          <router-link to="/concerns" class="mobile-nav-item" @click="closeMenu">{{ localeStore.t('nav.concerns') || 'Skin Concerns & Types' }}</router-link>
          <router-link to="/wishlist" class="mobile-nav-item" @click="closeMenu">{{ localeStore.t('nav.wishlist') || 'My Saved Wishlist' }}</router-link>
        </nav>

        <!-- Mobile Language & Currency Selector -->
        <div class="mobile-locale-card">
          <div class="mobile-locale-row">
            <span class="mobile-locale-label">{{ localeStore.t('common.language') }}</span>
            <div class="mobile-lang-pills">
              <button
                type="button"
                class="m-lang-btn"
                :class="{ active: localeStore.currentLocale === 'en' }"
                @click="selectLanguage('en')"
              >
                <FlagIcon locale="en" />
                <span>EN</span>
              </button>
              <button
                type="button"
                class="m-lang-btn"
                :class="{ active: localeStore.currentLocale === 'km' }"
                @click="selectLanguage('km')"
              >
                <FlagIcon locale="km" />
                <span>ខ្មែរ</span>
              </button>
              <button
                type="button"
                class="m-lang-btn"
                :class="{ active: localeStore.currentLocale === 'zh' }"
                @click="selectLanguage('zh')"
              >
                <FlagIcon locale="zh" />
                <span>中文</span>
              </button>
            </div>
          </div>

          <div class="mobile-locale-row mt-2">
            <span class="mobile-locale-label">{{ localeStore.t('common.currency') }}</span>
            <div class="mobile-lang-pills">
              <button
                type="button"
                class="m-lang-btn"
                :class="{ active: localeStore.currentCurrency === 'USD' }"
                @click="selectCurrency('USD')"
              >
                $ USD
              </button>
              <button
                type="button"
                class="m-lang-btn"
                :class="{ active: localeStore.currentCurrency === 'KHR' }"
                @click="selectCurrency('KHR')"
              >
                ៛ KHR
              </button>
              <button
                type="button"
                class="m-lang-btn"
                :class="{ active: localeStore.currentCurrency === 'CNY' }"
                @click="selectCurrency('CNY')"
              >
                ¥ CNY
              </button>
            </div>
          </div>
        </div>

        <div class="mobile-actions-footer">
          <template v-if="authStore.isAuthenticated">
            <div class="mobile-user-card">
              <img :src="authStore.userAvatar || '/images/avatars/avatar-default.png'" class="m-user-avatar" />
              <div class="m-user-info">
                <strong>{{ authStore.userName }}</strong>
                <span>{{ authStore.userEmail }}</span>
                <span class="m-user-tier">{{ authStore.user?.tier || 'Member' }}</span>
              </div>
            </div>
            <div class="mobile-user-action-row">
              <router-link to="/account" class="btn-m-account" @click="mobileMenuOpen = false">
                <Home :size="15" />
                <span>My Account</span>
              </router-link>
              <button type="button" class="btn-m-logout" @click="handleMobileLogout">
                <LogOut :size="15" />
                <span>Log Out</span>
              </button>
            </div>
          </template>
          <template v-else>
            <router-link to="/login" class="mobile-account-btn" @click="mobileMenuOpen = false">
              <User :size="18" />
              <span>Sign In / Create Account</span>
            </router-link>
          </template>
        </div>
      </div>
    </div>

    <!-- Account Modal -->
    <div v-if="showAccountModal" class="account-modal-backdrop" @click.self="showAccountModal = false">
      <div class="account-modal-card">
        <div class="modal-header">
          <h3>Welcome to Luméa</h3>
          <button class="modal-close" @click="showAccountModal = false" aria-label="Close">
            <X :size="18" />
          </button>
        </div>
        <p class="modal-sub">Sign in to track orders, save your skin routine, and collect beauty points.</p>

        <form @submit.prevent="handleAccountSubmit" class="account-form">
          <div class="form-group">
            <label>Email Address</label>
            <input type="email" v-model="accountEmail" placeholder="you@example.com" required />
          </div>
          <div class="form-group">
            <label>Password</label>
            <input type="password" v-model="accountPassword" placeholder="••••••••" required />
          </div>
          <button type="submit" class="btn btn-dark btn-block">Sign In</button>
        </form>
        <div class="modal-footer-note">
          <router-link to="/account/profile" class="admin-link" @click="showAccountModal = false" style="font-weight: 600; color: #9E3332; display: block; margin-bottom: 8px;">
            Go to My Skin Profile &rarr;
          </router-link>
          <div>
            <span>Admin console user?</span>
            <a :href="adminUrl" target="_blank" rel="noopener" class="admin-link">Open Atelier Admin &rarr;</a>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'
import { useProductStore } from '@/stores/products'
import { useWishlistStore } from '@/stores/wishlist'
import { useLocaleStore } from '@/stores/locale'
import { useAuthStore } from '@/stores/auth'
import { useAtelierNotificationStore } from '@/stores/atelierNotifications'
import FlagIcon from '@/components/common/FlagIcon.vue'
import {
  Bell,
  ChevronDown,
  Heart,
  Menu,
  Search,
  ShoppingBag,
  Sparkles,
  User,
  X,
  Globe,
  Check,
  UserCheck,
  Home,
  Package,
  Smile,
  LogOut
} from 'lucide-vue-next'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const adminUrl = import.meta.env.VITE_HOSTED_DEPLOYMENT === 'true' ? '/atelier/' : 'http://localhost:5174'
const cartStore = useCartStore()
const productStore = useProductStore()
const wishlistStore = useWishlistStore()
const localeStore = useLocaleStore()
const authStore = useAuthStore()
const notifStore = useAtelierNotificationStore()

const headerRef = ref(null)
const mobileMenuOpen = ref(false)
const searchQuery = ref('')
const activeDropdown = ref(null)
const showAccountModal = ref(false)
const accountEmail = ref('customer@lumea.com')
const accountPassword = ref('password123')

// Account dropdown state
const accountMenuOpen = ref(false)
const accountDropdownRef = ref(null)

function toggleAccountMenu() {
  accountMenuOpen.value = !accountMenuOpen.value
}

function handleNavbarLogout() {
  accountMenuOpen.value = false
  authStore.logout(true)
  router.push('/login')
}

function handleMobileLogout() {
  mobileMenuOpen.value = false
  authStore.logout(true)
  router.push('/login')
}

// Language & Currency Atelier Dropdown State
const localeMenuOpen = ref(false)
const localeDropdownRef = ref(null)

const currentLanguageLabel = computed(() => {
  if (localeStore.currentLocale === 'km') return 'ខ្មែរ'
  if (localeStore.currentLocale === 'zh') return '中文'
  return 'EN'
})

function toggleLocaleMenu() {
  localeMenuOpen.value = !localeMenuOpen.value
}

function selectLanguage(lang) {
  localeStore.setLocale(lang)
}

function selectCurrency(curr) {
  localeStore.setCurrency(curr, true)
}

function handleGlobalDropdownClick(e) {
  if (localeDropdownRef.value && !localeDropdownRef.value.contains(e.target)) {
    localeMenuOpen.value = false
  }
  if (accountDropdownRef.value && !accountDropdownRef.value.contains(e.target)) {
    accountMenuOpen.value = false
  }
}

const isShopActive = computed(() => {
  return route.path.startsWith('/shop') || route.path.startsWith('/category')
})

const isBrandsActive = computed(() => {
  return route.path.startsWith('/brand')
})

function updateHeaderHeight() {
  if (headerRef.value) {
    const h = headerRef.value.offsetHeight
    document.documentElement.style.setProperty('--navbar-height', `${h}px`)
  }
}

onMounted(() => {
  updateHeaderHeight()
  window.addEventListener('resize', updateHeaderHeight)
  document.addEventListener('click', handleGlobalDropdownClick)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateHeaderHeight)
  document.removeEventListener('click', handleGlobalDropdownClick)
})

function handleSearch() {
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim()
    productStore.filters.search = q
    router.push({ path: '/shop', query: { q } })
    mobileMenuOpen.value = false
    searchQuery.value = ''
  }
}

function openNotifFromMobile() {
  mobileMenuOpen.value = false
  notifStore.openDrawer()
}

function closeMenu() {
  mobileMenuOpen.value = false
  activeDropdown.value = null
}

function scrollToSection(sectionId) {
  closeMenu()
  const el = document.getElementById(sectionId)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  } else {
    router.push(`/#${sectionId}`)
  }
}

function openAccountModal() {
  mobileMenuOpen.value = false
  showAccountModal.value = true
}

function handleAccountSubmit() {
  showAccountModal.value = false
  router.push('/account/profile')
}
</script>

<style scoped>
/* ==========================================================================
   FORMAT-MATCHING SINGLE-ROW HEADER
   ========================================================================== */
.lumea-beauty-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: #FAF8F5;
  border-bottom: 1px solid rgba(28, 25, 23, 0.08);
  box-shadow: 0 1px 6px rgba(28, 25, 23, 0.03);
}

.header-main-row {
  height: 68px;
  display: flex;
  align-items: center;
}

.container-fluid.header-inner {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

/* 1. Left: Brand Logo */
.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-shrink: 0;
}

.brand-logo {
  display: flex;
  align-items: center;
  text-decoration: none;
}

.brand-logo-img {
  height: 38px;
  width: auto;
  object-fit: contain;
  display: block;
  transition: transform 0.2s ease;
}

.brand-logo:hover .brand-logo-img {
  transform: scale(1.02);
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: #1C1917;
  cursor: pointer;
  padding: 4px;
}

/* 2. Center: Desktop Nav Links */
.desktop-nav-links {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  flex-shrink: 0;
}

.nav-dropdown-item {
  position: relative;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 0.22rem;
  font-family: var(--font-sans);
  font-size: 0.86rem;
  font-weight: 500;
  color: #2B2625;
  text-decoration: none;
  padding: 0.5rem 0.15rem;
  transition: color 0.15s ease;
  cursor: pointer;
  white-space: nowrap;
}

.nav-link:hover {
  color: #8E4A3E;
}

.nav-link.is-active {
  color: #8E4A3E;
  font-weight: 600;
}

.nav-link.highlight-deals {
  color: #8E4A3E;
  font-weight: 600;
}

.nav-link.nav-quiz-badge {
  color: #8E4A3E;
  font-weight: 600;
  background: rgba(142, 74, 62, 0.08);
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  border: 1px solid rgba(142, 74, 62, 0.2);
  transition: all 0.2s ease;
}

.nav-link.nav-quiz-badge:hover,
.nav-link.nav-quiz-badge.is-active {
  background: #8E4A3E;
  color: #FFFFFF;
}

.nav-link.nav-quiz-badge:hover .quiz-badge-sparkle,
.nav-link.nav-quiz-badge.is-active .quiz-badge-sparkle {
  color: #FFFFFF;
}

.quiz-badge-sparkle {
  color: #8E4A3E;
}

.highlight-quiz {
  display: flex !important;
  align-items: center;
  gap: 8px;
  color: #8E4A3E !important;
  font-weight: 600;
}

.mobile-quiz-sparkle {
  color: #8E4A3E;
}

.caret-icon {
  color: #8C877F;
  transition: transform 0.2s cubic-bezier(0.23, 1, 0.32, 1), color 0.15s ease;
}

.nav-dropdown-item:hover .caret-icon {
  transform: rotate(180deg);
  color: #8E4A3E;
}

/* Dropdown Menus */
.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.09);
  border-radius: 10px;
  box-shadow: 0 10px 28px rgba(35, 25, 20, 0.08);
  min-width: 220px;
  padding: 0.5rem 0;
  z-index: 200;
  animation: dropdownFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes dropdownFadeIn {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-link {
  display: block;
  padding: 0.55rem 1.25rem;
  font-size: 0.84rem;
  color: #44403C;
  text-decoration: none;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.dropdown-link:hover {
  background-color: #F8F4F0;
  color: #8E4A3E;
}

.dropdown-link.featured-link {
  font-weight: 600;
  color: #8E4A3E;
  border-bottom: 1px solid rgba(28, 25, 23, 0.06);
  margin-bottom: 0.25rem;
}

.dropdown-section-label {
  padding: 0.4rem 1.25rem 0.15rem;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #8C877F;
  border-top: 1px solid rgba(28, 25, 23, 0.05);
  margin-top: 0.25rem;
}

/* 3. Center-Right: Search Pill Form (Icon on Right matching format) */
.search-pill-container {
  flex: 0 1 310px;
  min-width: 180px;
}

.search-pill-form {
  position: relative;
  display: flex;
  align-items: center;
  background: #F4EFEB;
  border: 1px solid rgba(28, 25, 23, 0.08);
  border-radius: 9999px;
  padding: 0.42rem 0.75rem 0.42rem 1.1rem;
  transition: all 0.2s cubic-bezier(0.23, 1, 0.32, 1);
}

.search-pill-form:focus-within {
  background: #FFFFFF;
  border-color: #8E4A3E;
  box-shadow: 0 0 0 2px rgba(142, 74, 62, 0.12);
}

.search-pill-input {
  flex: 1;
  width: 100%;
  border: none;
  background: transparent;
  font-size: 0.82rem;
  color: #1C1917;
  outline: none;
  font-family: var(--font-sans);
}

.search-pill-input::placeholder {
  color: #8C877F;
  font-size: 0.8rem;
}

.clear-search-btn {
  color: #8C877F;
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px 4px;
  display: flex;
  align-items: center;
}

.search-submit-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #2B2625;
  display: flex;
  align-items: center;
  padding: 2px 4px;
  transition: color 0.15s ease, transform 0.15s ease;
}

.search-submit-btn:hover {
  color: #8E4A3E;
  transform: scale(1.08);
}

/* 4. Far Right: Clean Minimal Icons (No Text Labels) */
.header-action-icons {
  display: flex;
  align-items: center;
  gap: 1.15rem;
  flex-shrink: 0;
}

.header-icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: #1C1917;
  cursor: pointer;
  position: relative;
  padding: 4px;
  text-decoration: none;
  transition: color 0.15s ease, transform 0.15s ease;
}

.header-icon-btn:hover {
  color: #8E4A3E;
  transform: scale(1.08);
}

.cart-btn-pos {
  position: relative;
}

/* Format Red/Terracotta Circular Cart Badge */
.cart-circle-badge {
  position: absolute;
  top: -3px;
  right: -7px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: #8E4A3E;
  color: #FFFFFF;
  font-size: 0.65rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  border: 1.5px solid #FAF8F5;
}

/* Wishlist Badge */
.wishlist-circle-badge {
  position: absolute;
  top: -3px;
  right: -7px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: #242721;
  color: #FFFFFF;
  font-size: 0.65rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  border: 1.5px solid #FAF8F5;
}

/* Notification Button & Badge */
.notif-icon-btn {
  position: relative;
}

.notif-circle-badge {
  position: absolute;
  top: -3px;
  right: -7px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: #7A2E22;
  color: #FFFFFF;
  font-size: 0.65rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  border: 1.5px solid #FAF8F5;
}

.notif-pulse-dot {
  position: absolute;
  top: 1px;
  right: 1px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #D97706;
  pointer-events: none;
}

.mobile-notif-shortcut-wrap {
  padding: 0 1.25rem 0.75rem;
}

.mobile-notif-shortcut-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #FAF7F2;
  border: 1px solid #EFEAE4;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  font-size: 0.84rem;
  font-weight: 600;
  color: #1C1917;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mobile-notif-shortcut-btn:hover {
  background: #F5EFEB;
  border-color: #7A2E22;
}

.m-notif-row {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.m-notif-bell {
  color: #7A2E22;
}

.m-notif-badge {
  background: #7A2E22;
  color: #FFFFFF;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.15rem 0.5rem;
  border-radius: 9999px;
}

/* ==========================================================================
   MOBILE DRAWER & RESPONSIVE BEHAVIOR
   ========================================================================== */
@media (max-width: 1180px) {
  .desktop-nav-links {
    gap: 0.85rem;
  }
  .nav-link {
    font-size: 0.82rem;
  }
  .search-pill-container {
    flex: 0 1 240px;
  }
}

@media (max-width: 1040px) {
  .desktop-nav-links {
    display: none;
  }
  .mobile-toggle {
    display: flex;
  }
  .search-pill-container {
    display: none;
  }
}

@media (max-width: 640px) {
  .container-fluid.header-inner {
    padding: 0 0.75rem;
    gap: 0.5rem;
  }
  .header-left {
    gap: 0.5rem;
  }
  .brand-logo-img {
    height: 28px;
  }
  .header-action-icons {
    gap: 0.5rem;
  }
  /* Primary icon on mobile is Cart Bag; hide redundant header wishlist and account icons (prominent in drawer) */
  .wishlist-icon-btn,
  .account-icon-btn {
    display: none !important;
  }
  /* Compact language & currency pill on mobile */
  .locale-pill-btn {
    padding: 0.28rem 0.45rem;
    gap: 3px;
  }
  .locale-globe-svg,
  .locale-lang-code,
  .locale-divider-dot {
    display: none !important;
  }
  .locale-currency-code {
    font-size: 0.7rem;
  }
}

@media (max-width: 360px) {
  .container-fluid.header-inner {
    padding: 0 0.4rem;
    gap: 0.35rem;
  }
  .header-left {
    gap: 0.35rem;
  }
  .brand-logo-img {
    height: 24px;
  }
  .header-action-icons {
    gap: 0.35rem;
  }
  .locale-pill-btn {
    padding: 0.22rem 0.35rem;
  }
  .locale-flag-icon {
    font-size: 0.75rem;
  }
  .locale-currency-code {
    font-size: 0.65rem;
  }
}

.mobile-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(28, 25, 23, 0.45);
  backdrop-filter: blur(4px);
  z-index: 250;
  display: flex;
  justify-content: flex-start;
}

.mobile-drawer-panel {
  width: 82%;
  max-width: 320px;
  height: 100vh;
  background: #FFFFFF;
  box-shadow: var(--shadow-lg);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 1.5rem;
  animation: slideInLeft 0.25s cubic-bezier(0.23, 1, 0.32, 1);
}

@keyframes slideInLeft {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}

.mobile-drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.mobile-logo-img {
  height: 32px;
  width: auto;
}

.mobile-close-btn {
  background: none;
  border: none;
  color: #1C1917;
  cursor: pointer;
  padding: 4px;
}

.mobile-search-box {
  margin-bottom: 1.25rem;
}

.mobile-nav-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  flex: 1;
}

.mobile-nav-item {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1C1917;
  text-decoration: none;
  padding: 0.5rem 0;
  display: flex;
  align-items: center;
}

.mobile-nav-item:hover,
.mobile-nav-item.highlight-deals {
  color: #8E4A3E;
}

.mobile-nav-subitem {
  font-size: 0.85rem;
  color: #57534E;
  text-decoration: none;
  padding: 0.35rem 0.75rem;
  display: block;
}

.mobile-nav-subitem:hover {
  color: #8E4A3E;
}

.mobile-divider {
  height: 1px;
  background: rgba(28, 25, 23, 0.08);
  margin: 0.75rem 0;
}

.mobile-actions-footer {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(28, 25, 23, 0.08);
}

.mobile-account-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #242721;
  color: #FFFFFF;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  text-decoration: none;
}

.mobile-user-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #FAF8F5;
  border: 1px solid #EFE6DD;
  border-radius: 12px;
  padding: 10px 14px;
  margin-bottom: 10px;
}

.m-user-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
  border: 1.5px solid #EFE6DD;
}

.m-user-info {
  display: flex;
  flex-direction: column;
}

.m-user-info strong {
  font-size: 0.9rem;
  color: #1C1917;
}

.m-user-info span {
  font-size: 0.78rem;
  color: #78716C;
}

.m-user-tier {
  font-size: 0.7rem !important;
  color: #8E4A3E !important;
  font-weight: 600;
  margin-top: 2px;
}

.mobile-user-action-row {
  display: flex;
  gap: 8px;
}

.btn-m-account,
.btn-m-logout {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
}

.btn-m-account {
  background: #FAF8F5;
  border: 1px solid #EFE6DD;
  color: #1C1917;
}

.btn-m-logout {
  background: #FEF2F2;
  border: 1px solid #FEE2E2;
  color: #DC2626;
}

/* Desktop Header Account Dropdown */
.header-account-wrap {
  position: relative;
}

.user-logged-in-btn {
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-avatar-thumb {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  object-fit: cover;
  border: 1.5px solid #8E4A3E;
}

.navbar-account-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 240px;
  background: #FFFFFF;
  border: 1px solid #EFE6DD;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(28, 25, 23, 0.12);
  padding: 8px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.dropdown-user-header {
  padding: 8px 12px 10px;
  display: flex;
  flex-direction: column;
}

.dropdown-user-header strong {
  font-size: 0.88rem;
  color: #1C1917;
}

.dropdown-user-header span {
  font-size: 0.76rem;
  color: #78716C;
}

.user-tier-pill-small {
  margin-top: 4px;
  display: inline-block;
  padding: 2px 7px;
  background: #F5EAE7;
  color: #8E4A3E;
  border-radius: 999px;
  font-size: 0.68rem !important;
  font-weight: 700;
  width: fit-content;
}

.dropdown-divider {
  height: 1px;
  background: #F5EFEB;
  margin: 4px 0;
}

.dropdown-menu-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 0.82rem;
  font-weight: 500;
  color: #57534E;
  text-decoration: none;
  background: transparent;
  border: none;
  width: 100%;
  cursor: pointer;
  transition: all 0.15s ease;
}

.dropdown-menu-link:hover {
  background: #FAF8F5;
  color: #8E4A3E;
}

.dropdown-menu-link.logout-link {
  color: #DC2626;
}

.dropdown-menu-link.logout-link:hover {
  background: #FEF2F2;
  color: #991B1B;
}

/* ==========================================================================
   ACCOUNT QUICK MODAL
   ========================================================================== */
.account-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(28, 25, 23, 0.6);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 1.5rem;
}

.account-modal-card {
  width: 100%;
  max-width: 420px;
  background: #FFFFFF;
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-lg);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.35rem;
}

.modal-header h3 {
  font-family: var(--font-serif);
  font-size: 1.4rem;
  color: var(--text-primary);
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: #8C877F;
  padding: 4px;
}

.modal-sub {
  font-size: 0.82rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.4;
}

.account-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-secondary);
}

.form-group input {
  padding: 0.7rem 1rem;
  border: 1px solid rgba(28, 25, 23, 0.15);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  font-family: inherit;
}

.btn-dark {
  background: #242721;
  color: #FFFFFF;
  padding: 0.85rem;
  border-radius: var(--radius-sm);
  font-weight: 600;
  border: none;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s ease;
}

.btn-dark:hover {
  background: #171914;
}

.btn-block {
  width: 100%;
}

.modal-footer-note {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.78rem;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.admin-link {
  color: #8E4A3E;
  font-weight: 600;
  text-decoration: none;
}

/* ==========================================================================
   LANGUAGE & CURRENCY ATELIER SWITCHER STYLES
   ========================================================================== */
.locale-switcher-wrap {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.locale-pill-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #F4EFEB;
  border: 1px solid rgba(28, 25, 23, 0.1);
  border-radius: 9999px;
  padding: 0.35rem 0.65rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
  cursor: pointer;
  transition: all 0.18s ease;
  user-select: none;
}

.locale-pill-btn:hover {
  background: #EFE7E0;
  border-color: #8B2E24;
  color: #8B2E24;
}

.locale-globe-svg {
  color: #8C877F;
  flex-shrink: 0;
}

.locale-flag-icon {
  font-size: 0.85rem;
  line-height: 1;
}

.locale-lang-code {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.locale-divider-dot {
  color: #B8ADA5;
  font-weight: 700;
  font-size: 0.75rem;
}

.locale-currency-code {
  font-size: 0.72rem;
  font-weight: 700;
  color: #8B2E24;
}

.locale-caret-icon {
  color: #8C877F;
  transition: transform 0.2s ease;
}

.locale-caret-icon.is-open {
  transform: rotate(180deg);
  color: #8B2E24;
}

/* Luxury Atelier Popover Dropdown */
.locale-popover-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 280px;
  background: #FFFFFF;
  border: 1px solid rgba(28, 25, 23, 0.1);
  border-radius: 12px;
  box-shadow: 0 16px 36px rgba(35, 25, 20, 0.14);
  padding: 0.85rem;
  z-index: 300;
  animation: dropdownFadeIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.popover-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.45rem;
}

.popover-heading {
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #8C877F;
}

.popover-hint {
  font-size: 0.625rem;
  font-weight: 600;
  color: #92400E;
  background: #FEF3C7;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.popover-options-list {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.popover-option-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  width: 100%;
  padding: 0.5rem 0.65rem;
  border: 1px solid transparent;
  border-radius: 8px;
  background: #FAF8F5;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s ease;
}

.popover-option-item:hover {
  background: #F4EFEB;
  border-color: #E2D7CE;
}

.popover-option-item.active {
  background: #FFF7F5;
  border-color: #8B2E24;
}

.pop-flag {
  font-size: 1.15rem;
  line-height: 1;
}

.pop-details {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.pop-name {
  font-size: 0.78rem;
  font-weight: 600;
  color: #2D2422;
}

.pop-sub {
  font-size: 0.65rem;
  color: #8C877F;
  margin-top: 1px;
}

.pop-check {
  color: #8B2E24;
  flex-shrink: 0;
}

.popover-divider {
  height: 1px;
  background: #F0E8E2;
  margin: 0.75rem 0;
}

/* Currency Chips Grid */
.currency-chips-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.4rem;
  margin-top: 0.35rem;
}

.pop-curr-chip {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.45rem 0.25rem;
  border: 1px solid #E5DDD5;
  border-radius: 6px;
  background: #FAF8F5;
  cursor: pointer;
  transition: all 0.15s ease;
}

.pop-curr-chip:hover {
  background: #F4EFEB;
  border-color: #8B2E24;
}

.pop-curr-chip.active {
  background: #8B2E24;
  border-color: #8B2E24;
  color: #FFFFFF;
}

.chip-sym {
  font-size: 0.85rem;
  font-weight: 700;
  line-height: 1;
}

.chip-label {
  font-size: 0.65rem;
  font-weight: 600;
  margin-top: 2px;
}

.pop-curr-chip.active .chip-label,
.pop-curr-chip.active .chip-sym {
  color: #FFFFFF;
}

.popover-rate-footnote {
  font-size: 0.65rem;
  color: #8C877F;
  margin-top: 0.6rem;
  text-align: center;
}

/* Mobile Locale Selector */
.mobile-locale-card {
  padding: 1rem 1.25rem;
  border-top: 1px solid rgba(28, 25, 23, 0.08);
  border-bottom: 1px solid rgba(28, 25, 23, 0.08);
  background: #FAF8F5;
}

.mobile-locale-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.mobile-locale-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #2D2422;
}

.mobile-lang-pills {
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.m-lang-btn {
  padding: 0.3rem 0.6rem;
  font-size: 0.7rem;
  font-weight: 600;
  border: 1px solid #E2D7CE;
  border-radius: 6px;
  background: #FFFFFF;
  color: #2D2422;
  cursor: pointer;
  transition: all 0.15s ease;
}

.m-lang-btn.active {
  background: #8B2E24;
  border-color: #8B2E24;
  color: #FFFFFF;
}
</style>
