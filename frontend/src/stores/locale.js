import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const translations = {
  en: {
    nav: {
      shop: 'Shop',
      brands: 'Brands',
      concerns: 'Concerns & Types',
      best_sellers: 'Best Sellers',
      new_arrivals: 'New Arrivals',
      deals: 'Deals',
      articles: 'Articles',
      skin_quiz: 'Skin Quiz',
      search_placeholder: 'Search for products, brands, or concerns...',
      wishlist: 'Wishlist',
      shopping_bag: 'Shopping Bag',
      my_account: 'My Account',
      all_products: 'All Products (Shop All)',
      browse_brands: 'Browse All Brands Directory →',
      explore_concerns: 'Explore Full Diagnostic Matrix →',
      by_concern: 'By Skin Concern',
      by_type: 'By Skin Type',
      dryness: 'Dryness & Dehydration',
      dark_spots: 'Dark Spots & Pigmentation',
      aging: 'Fine Lines & Elasticity',
      acne: 'Blemishes & Pore Care',
      sensitivity: 'Redness & Sensitive Barrier',
      dry_skin: 'Dry Skin',
      oily_skin: 'Oily Skin',
      combination_skin: 'Combination Skin',
      sensitive_skin: 'Sensitive Skin',
      cleansers: 'Cleansers & Balms',
      toners: 'Toners & Essences',
      serums: 'Serums & Ampoules',
      moisturizers: 'Moisturizers & Creams',
      sunscreens: 'Sun Protection SPF',
      masks: 'Sheet & Clay Masks',
      treatments: 'Exfoliants & Peels',
      kits: 'Discovery Sets & Bundles'
    },
    common: {
      free: 'FREE',
      qty: 'Qty',
      price: 'Price',
      quantity: 'Quantity',
      subtotal: 'Subtotal',
      shipping: 'Shipping',
      tax: 'Estimated Tax',
      total: 'Total',
      discount: 'Discount',
      apply: 'Apply',
      remove: 'Remove',
      delete: 'Remove',
      save: 'Save',
      cancel: 'Cancel',
      close: 'Close',
      loading: 'Loading...',
      language: 'Language',
      currency: 'Currency',
      rate_hint: 'Exchange Rate',
      authentic_guarantee: '100% Authentic Products',
      reliable_shipping: 'Reliable Nationwide Courier',
      easy_returns: '30-Day Easy Returns & Exchanges',
      better_skin: 'Clinically Curated Formulations'
    },
    product: {
      add_to_bag: 'Add to Bag',
      added_to_bag: 'Added to Bag',
      out_of_stock: 'Out of Stock',
      quick_buy: 'Quick Buy',
      full_size: 'Full Size',
      reviews: 'Reviews',
      rating: 'Rating',
      key_ingredients: 'Key Ingredients',
      how_to_use: 'How to Use',
      description: 'Description',
      related_products: 'Related Formulations',
      skin_type_match: 'Skin Type Match',
      texture: 'Sensory Texture',
      video_reel: 'Video Texture Demo'
    },
    cart: {
      title: 'Shopping Bag',
      formulation: 'Formulation',
      empty: 'Your shopping bag is currently empty.',
      return_to_catalog: 'Return to Catalog',
      free_shipping_unlocked: 'You have unlocked Complimentary Free Shipping!',
      add_more_for_free: 'Add {amount} more for Complimentary Free Shipping',
      promo_code: 'Have a Promo Code?',
      enter_code: 'Enter promo code',
      checkout_btn: 'Proceed to Checkout',
      view_bag: 'View Shopping Bag',
      items_count: '{count} item | {count} items'
    },
    checkout: {
      title: 'Checkout',
      subtitle: 'Review your details, choose delivery & payment, and place your order.',
      step_bag: 'Bag',
      step_delivery: 'Delivery & Payment',
      step_review: 'Review Order',
      step_confirmation: 'Confirmation',
      contact_info: 'Contact Information',
      contact_sub: "We'll use this to keep you updated about your order.",
      already_account: 'Already have an account?',
      log_in: 'Log in',
      full_name: 'Full Name',
      phone_number: 'Phone Number (Courier Contact)',
      email_address: 'Email Address',
      newsletter_opt: 'Keep me updated on exclusive offers, new arrivals, and skincare tips.',
      delivery_dispatch: 'Delivery & Courier Dispatch',
      delivery_sub: 'Select your address, courier, and delivery option in Cambodia.',
      shipping_address: 'Shipping Address',
      province_city: 'Province / City',
      street_address: 'Street Address, Sangkat & Khan',
      default_address: 'Default',
      add_new_address: 'Add New Address',
      delivery_location_pin: 'Delivery Location (Fine-tune)',
      delivery_location_hint: 'Help our courier find you faster. Pin your exact location on the map.',
      locate_me: 'Locate Me',
      select_courier: 'Select Cambodia Courier',
      courier_hint: 'Direct delivery to all 25 provinces and Phnom Penh.',
      vet_name: 'Vireak Buntham',
      vet_sub: '(VET Express)',
      vet_tag: 'NATIONWIDE #1',
      jt_name: 'J&T Express',
      jt_sub: 'Cambodia',
      jt_tag: 'FAST DOMESTIC',
      grab_name: 'GrabExpress',
      grab_sub: 'On-Demand',
      grab_tag: 'INSTANT EXPRESS',
      pp_only: 'PP ONLY',
      concierge_name: 'Luméa Atelier',
      concierge_sub: 'Concierge',
      concierge_tag: 'ATELIER SIGNATURE',
      payment_selection: 'Payment Selection',
      payment_sub: 'Choose a secure and convenient payment method.',
      bakong_khqr: 'Bakong KHQR - ABA Mobile',
      instant_clearance: 'INSTANT CLEARANCE',
      khqr_desc: 'Scan with ABA Mobile, Bakong, Wing, ACLEDA, or any Cambodian banking app.',
      all_banks: '+ All Banks',
      cod_name: 'Cash on Delivery (COD)',
      doorstep_handover: 'DOORSTEP HANDOVER',
      cod_desc: 'Pay in cash (USD $ or KHR ៛) directly to the delivery driver upon receiving your package.',
      usd_cash: 'USD Cash',
      khr_cash: 'KHR Cash',
      zero_surcharge: 'Zero Surcharge',
      order_summary: 'Order Summary',
      edit_cart: 'Edit Cart',
      review_order_btn: 'Review Your Order →',
      back_to_bag: '← Back to Shopping Bag',
      need_help: 'Need Help?',
      contact_us: 'Contact Us',
      special_promo: 'Atelier Special Promotion',
      complimentary_delivery: 'Complimentary Free Delivery'
    },
    home: {
      hero_tag: 'Pure Botanical Science',
      hero_title: 'Nourish Your Skin, Reveal Your Radiance',
      hero_sub: 'Clinically proven, mindful formulations crafted with rare botanicals to restore balance and luminosity.',
      shop_all: 'Shop Collection',
      take_quiz: 'Take Skin Quiz',
      featured_title: 'Atelier Best Sellers',
      featured_sub: 'Our most coveted, dermatologically vetted essentials loved across the Kingdom.',
      view_all: 'View All Products'
    },
    footer: {
      about_title: 'Luméa Atelier',
      about_desc: 'Contemporary skincare atelier curated for Southeast Asian climate. Clinically proven, mindful beauty.',
      shop_links: 'Shop Categories',
      customer_care: 'Customer Care',
      legal_title: 'Atelier Policies',
      copyright: '© 2026 Luméa Atelier Co., Ltd. All rights reserved.',
      phnom_penh: '#123 Norodom Blvd, BKK1, Phnom Penh, Cambodia'
    }
  },

  km: {
    nav: {
      shop: 'ហាងទំនិញ',
      brands: 'ម៉ាកយីហោ',
      concerns: 'បញ្ហា & ប្រភេទស្បែក',
      best_sellers: 'លក់ដាច់បំផុត',
      new_arrivals: 'ទើបមកដល់ថ្មី',
      deals: 'ប្រូម៉ូសិនពិសេស',
      articles: 'អត្ថបទថែរក្សាស្បែក',
      skin_quiz: 'តេស្តវិភាគស្បែក',
      search_placeholder: 'ស្វែងរកផលិតផល ម៉ាកយីហោ ឬបញ្ហាស្បែក...',
      wishlist: 'បញ្ជីចង់បាន',
      shopping_bag: 'កន្ត្រកទំនិញ',
      my_account: 'គណនីរបស់ខ្ញុំ',
      all_products: 'ផលិតផលទាំងអស់ (ទិញទាំងអស់)',
      browse_brands: 'មើលបញ្ជីម៉ាកយីហោទាំងអស់ →',
      explore_concerns: 'ពិនិត្យតារាងវិភាគបញ្ហាស្បែក →',
      by_concern: 'តាមបញ្ហាស្បែក',
      by_type: 'តាមប្រភេទស្បែក',
      dryness: 'ស្បែកស្ងួត & ខ្វះជាតិទឹក',
      dark_spots: 'ស្នាមអុចខ្មៅ & ស្នាមជាំ',
      aging: 'ភាពយារធ្លាក់ & ស្នាមជ្រីវជ្រួញ',
      acne: 'មុន & រន្ធញើសធំ',
      sensitivity: 'ស្បែកក្រហម & ងាយប្រតិកម្ម',
      dry_skin: 'ស្បែកស្ងួត',
      oily_skin: 'ស្បែកខ្លាញ់',
      combination_skin: 'ស្បែកចម្រុះ',
      sensitive_skin: 'ស្បែកងាយប្រតិកម្ម',
      cleansers: 'ហ្វូម & ប្រេងលាងសម្អាត',
      toners: 'ទឹកតប់ & អេសសិន',
      serums: 'សេរ៉ូម & អំពូល',
      moisturizers: 'ក្រែមផ្តល់សំណើម',
      sunscreens: 'ឡេការពារកម្តៅថ្ងៃ SPF',
      masks: 'ម៉ាសបិទមុខ & ម៉ាសភក់',
      treatments: 'ផលិតផលជម្រុះកោសិកាចាស់',
      kits: 'ឈុតសាកល្បង & កញ្ចប់ពិសេស'
    },
    common: {
      free: 'ឥតគិតថ្លៃ',
      qty: 'ចំនួន',
      price: 'តម្លៃ',
      quantity: 'បរិមាណ',
      subtotal: 'សរុបរង',
      shipping: 'ថ្លៃដឹកជញ្ជូន',
      tax: 'ពន្ធប៉ាន់ស្មាន',
      total: 'សរុប',
      discount: 'បញ្ចុះតម្លៃ',
      apply: 'អនុវត្ត',
      remove: 'លុបចេញ',
      delete: 'លុបចេញ',
      save: 'រក្សាទុក',
      cancel: 'បោះបង់',
      close: 'បិទ',
      loading: 'កំពុងផ្ទុក...',
      language: 'ភាសា',
      currency: 'រូបិយប័ណ្ណ',
      rate_hint: 'អត្រាប្តូរប្រាក់',
      authentic_guarantee: 'ផលិតផលសុទ្ធ ១០០%',
      reliable_shipping: 'ដឹកជញ្ជូនរហ័សទូទាំងប្រទេស',
      easy_returns: 'ប្តូរទំនិញងាយស្រួលក្នុងរយៈពេល ៣០ថ្ងៃ',
      better_skin: 'រូបមន្តវេជ្ជសាស្ត្រស្តង់ដារខ្ពស់'
    },
    product: {
      add_to_bag: 'ដាក់ចូលកន្ត្រក',
      added_to_bag: 'បានដាក់ចូលកន្ត្រក',
      out_of_stock: 'អស់ពីស្តុក',
      quick_buy: 'ទិញរហ័ស',
      full_size: 'ទំហំពេញ',
      reviews: 'ការវាយតម្លៃ',
      rating: 'ពិន្ទុ',
      key_ingredients: 'ធាតុផ្សំសំខាន់ៗ',
      how_to_use: 'របៀបប្រើប្រាស់',
      description: 'ការពិពណ៌នា',
      related_products: 'ផលិតផលស្រដៀងគ្នា',
      skin_type_match: 'ស័ក្តិសមនឹងស្បែក',
      texture: 'សាច់ផលិតផល',
      video_reel: 'វីដេអូបង្ហាញសាច់ផលិតផល'
    },
    cart: {
      title: 'កន្ត្រកទំនិញ',
      formulation: 'រូបមន្តផលិតផល',
      empty: 'កន្ត្រកទំនិញរបស់អ្នកបច្ចុប្បន្ននៅទទេ។',
      return_to_catalog: 'ត្រឡប់ទៅកាន់ហាងទំនិញ',
      free_shipping_unlocked: 'អ្នកទទួលបានការដឹកជញ្ជូនឥតគិតថ្លៃ!',
      add_more_for_free: 'ទិញបន្ថែម {amount} ទៀតដើម្បីទទួលបានការដឹកជញ្ជូនឥតគិតថ្លៃ',
      promo_code: 'តើអ្នកមានលេខកូដបញ្ចុះតម្លៃទេ?',
      enter_code: 'បញ្ចូលលេខកូដបញ្ចុះតម្លៃ',
      checkout_btn: 'បន្តទៅកាន់ការទូទាត់ប្រាក់',
      view_bag: 'មើលកន្ត្រកទំនិញ',
      items_count: '{count} មុខ'
    },
    checkout: {
      title: 'ការទូទាត់ប្រាក់',
      subtitle: 'ពិនិត្យព័ត៌មានរបស់អ្នក ជ្រើសរើសក្រុមហ៊ុនដឹកជញ្ជូន និងវិធីសាស្ត្រទូទាត់។',
      step_bag: 'កន្ត្រក',
      step_delivery: 'ដឹកជញ្ជូន & ទូទាត់',
      step_review: 'ពិនិត្យការបញ្ជាទិញ',
      step_confirmation: 'ការបញ្ជាក់ការបញ្ជាទិញ',
      contact_info: 'ព័ត៌មានទំនាក់ទំនង',
      contact_sub: 'យើងនឹងប្រើព័ត៌មាននេះដើម្បីធ្វើបច្ចុប្បន្នភាពអំពីការបញ្ជាទិញរបស់អ្នក។',
      already_account: 'មានគណនីរួចហើយ?',
      log_in: 'ចូលគណនី',
      full_name: 'ឈ្មោះពេញ',
      phone_number: 'លេខទូរស័ព្ទ (សម្រាប់អ្នកដឹកជញ្ជូន)',
      email_address: 'អាសយដ្ឋានអ៊ីមែល',
      newsletter_opt: 'ទទួលព័ត៌មានអំពីការផ្តល់ជូនពិសេស ផលិតផលថ្មីៗ និងគន្លឹះថែរក្សាស្បែក។',
      delivery_dispatch: 'ការដឹកជញ្ជូន & ក្រុមហ៊ុននាំសំបុត្រ',
      delivery_sub: 'ជ្រើសរើសអាសយដ្ឋាន ក្រុមហ៊ុនដឹកជញ្ជូន និងជម្រើសសេវាកម្មនៅកម្ពុជា។',
      shipping_address: 'អាសយដ្ឋានដឹកជញ្ជូន',
      province_city: 'រាជធានី / ខេត្ត',
      street_address: 'អាសយដ្ឋានផ្លូវ សង្កាត់ និងខណ្ឌ',
      default_address: 'លំនាំដើម',
      add_new_address: 'បន្ថែមអាសយដ្ឋានថ្មី',
      delivery_location_pin: 'ទីតាំងដឹកជញ្ជូនជាក់លាក់ (ផែនទី)',
      delivery_location_hint: 'ជួយអ្នកដឹកជញ្ជូនស្វែងរកអ្នកលឿនជាងមុន ដោយកំណត់ទីតាំងច្បាស់លាស់លើផែនទី។',
      locate_me: 'កំណត់ទីតាំងខ្ញុំ',
      select_courier: 'ជ្រើសរើសក្រុមហ៊ុនដឹកជញ្ជូននៅកម្ពុជា',
      courier_hint: 'ដឹកជញ្ជូនផ្ទាល់ដល់ ២៥ រាជធានី-ខេត្ត។',
      vet_name: 'វីរៈប៊ុនថាំ',
      vet_sub: '(VET Express)',
      vet_tag: 'ទូទាំងប្រទេស #1',
      jt_name: 'ជេ អែន ធី',
      jt_sub: 'J&T Express',
      jt_tag: 'រហ័សទូទាំងស្រុក',
      grab_name: 'GrabExpress',
      grab_sub: 'ដឹកភ្លាមៗ',
      grab_tag: 'រហ័សទាន់ចិត្ត',
      pp_only: 'ភ្នំពេញប៉ុណ្ណោះ',
      concierge_name: 'លូម៊ែរ អាតឺលីយេ',
      concierge_sub: 'ខុនសៀហ្ស៍',
      concierge_tag: 'សេវាកម្មកម្រិតខ្ពស់',
      payment_selection: 'ជ្រើសរើសវិធីសាស្ត្រទូទាត់',
      payment_sub: 'ជ្រើសរើសវិធីទូទាត់ដែលមានសុវត្ថិភាព និងងាយស្រួល។',
      bakong_khqr: 'បាគង KHQR - ABA ម៉ូបាល',
      instant_clearance: 'ទូទាត់រហ័សទាន់ចិត្ត',
      khqr_desc: 'ស្កេនជាមួយ ABA Mobile, Bakong, Wing, ACLEDA ឬកម្មវិធីធនាគារណាមួយនៅកម្ពុជា។',
      all_banks: '+ គ្រប់ធនាគារ',
      cod_name: 'ទូទាត់ពេលទទួលទំនិញ (COD)',
      doorstep_handover: 'ទូទាត់ពេលប្រគល់ទំនិញ',
      cod_desc: 'ទូទាត់ជាសាច់ប្រាក់ (ដុល្លារ $ ឬ រៀល ៛) ដោយផ្ទាល់ជាមួយអ្នកដឹកជញ្ជូនពេលទទួលទំនិញ។',
      usd_cash: 'ប្រាក់ដុល្លារ',
      khr_cash: 'ប្រាក់រៀល',
      zero_surcharge: 'គ្មានការគិតថ្លៃបន្ថែម',
      order_summary: 'សង្ខេបការបញ្ជាទិញ',
      edit_cart: 'កែសម្រួលកន្ត្រក',
      review_order_btn: 'ពិនិត្យការបញ្ជាទិញ →',
      back_to_bag: '← ត្រឡប់ទៅកន្ត្រកទំនិញ',
      need_help: 'ត្រូវការជំនួយ?',
      contact_us: 'ទាក់ទងមកកាន់យើងខ្ញុំ',
      special_promo: 'ប្រូម៉ូសិនពិសេសប្រចាំហាង',
      complimentary_delivery: 'ការដឹកជញ្ជូនឥតគិតថ្លៃ'
    },
    home: {
      hero_tag: 'វិទ្យាសាស្ត្ររុក្ខជាតិធម្មជាតិសុទ្ធ',
      hero_title: 'ចិញ្ចឹមបីបាច់ស្បែកអ្នក បង្ហាញភាពភ្លឺថ្លាពិតប្រាកដ',
      hero_sub: 'រូបមន្តវេជ្ជសាស្ត្រឆ្លងកាត់ការពិសោធន៍ច្បាស់លាស់ ផ្សំពីរុក្ខជាតិកម្រដើម្បីស្តារតុល្យភាព និងពន្លឺស្បែក។',
      shop_all: 'ទិញទំនិញឥឡូវនេះ',
      take_quiz: 'ធ្វើតេស្តស្បែក',
      featured_title: 'ទំនិញលក់ដាច់បំផុតប្រចាំហាង',
      featured_sub: 'ផលិតផលដែលទទួលបានការស្រឡាញ់ពេញចិត្តបំផុតទូទាំងព្រះរាជាណាចក្រកម្ពុជា។',
      view_all: 'មើលផលិតផលទាំងអស់'
    },
    footer: {
      about_title: 'លូម៊ែរ អាតឺលីយេ',
      about_desc: 'ហាងថែរក្សាស្បែកបែបសហសម័យ សម្រិតសម្រាំងសម្រាប់អាកាសធាតុអាស៊ីអាគ្នេយ៍។ សោភ័ណភាពពិត និងលទ្ធផលច្បាស់លាស់។',
      shop_links: 'ប្រភេទផលិតផល',
      customer_care: 'សេវាបម្រើអតិថិជន',
      legal_title: 'គោលការណ៍ហាង',
      copyright: '© ២០២៦ Luméa Atelier Co., Ltd. រក្សាសិទ្ធិគ្រប់យ៉ាង។',
      phnom_penh: 'អគារលេខ ១២៣ មហាវិថីព្រះនរោត្តម បឹងកេងកង១ ភ្នំពេញ កម្ពុជា'
    }
  },

  zh: {
    nav: {
      shop: '探索商城',
      brands: '品牌专区',
      concerns: '肤质诉求',
      best_sellers: '热销榜单',
      new_arrivals: '当季新品',
      deals: '臻选特惠',
      articles: '护肤专栏',
      skin_quiz: '智能测肤',
      search_placeholder: '搜索护肤品、品牌或肤质诉求...',
      wishlist: '心愿单',
      shopping_bag: '购物袋',
      my_account: '个人中心',
      all_products: '全部商品 (探索全馆)',
      browse_brands: '浏览全部官方旗舰品牌 →',
      explore_concerns: '查看全方位肤质诊断矩阵 →',
      by_concern: '按护肤诉求',
      by_type: '按肌肤类型',
      dryness: '干燥缺水 & 补水修护',
      dark_spots: '色斑暗沉 & 匀净焕亮',
      aging: '抗皱紧致 & 弹润饱满',
      acne: '痘肌护理 & 细致毛孔',
      sensitivity: '泛红舒缓 & 屏障修护',
      dry_skin: '干性肌肤',
      oily_skin: '油性肌肤',
      combination_skin: '混合性肌肤',
      sensitive_skin: '敏感性肌肤',
      cleansers: '洁面与卸妆膏',
      toners: '爽肤水与精萃水',
      serums: '修护精华与安瓶',
      moisturizers: '面霜与乳液',
      sunscreens: '防晒乳与隔离 SPF',
      masks: '贴片面膜与泥膜',
      treatments: '温和刷酸与角质护理',
      kits: '旅行甄选与礼品套装'
    },
    common: {
      free: '免费',
      qty: '数量',
      price: '价格',
      quantity: '数量',
      subtotal: '商品小计',
      shipping: '配送运费',
      tax: '预估税费',
      total: '合计总额',
      discount: '优惠减免',
      apply: '使用',
      remove: '移除',
      delete: '移除',
      save: '保存',
      cancel: '取消',
      close: '关闭',
      loading: '加载中...',
      language: '语言',
      currency: '货币',
      rate_hint: '参考汇率',
      authentic_guarantee: '100% 官方正品保障',
      reliable_shipping: '柬埔寨全境极速直达',
      easy_returns: '30天安心售后退换',
      better_skin: '临床级天然植萃配方'
    },
    product: {
      add_to_bag: '加入购物袋',
      added_to_bag: '已加入购物袋',
      out_of_stock: '暂时缺货',
      quick_buy: '快捷选购',
      full_size: '标准正装',
      reviews: '顾客评价',
      rating: '评分',
      key_ingredients: '核心成分',
      how_to_use: '使用方法',
      description: '产品详情',
      related_products: '推荐搭配配方',
      skin_type_match: '适用肤质',
      texture: '质地展示',
      video_reel: '质地实测短视频'
    },
    cart: {
      title: '购物袋',
      formulation: '产品配方',
      empty: '您的购物袋目前是空的。',
      return_to_catalog: '返回挑选商品',
      free_shipping_unlocked: '恭喜！您已解锁全境免运费优惠！',
      add_more_for_free: '再购 {amount} 即可享受免费包邮',
      promo_code: '使用优惠券码',
      enter_code: '输入优惠代码',
      checkout_btn: '前往安全结账',
      view_bag: '查看购物袋',
      items_count: '{count} 件商品'
    },
    checkout: {
      title: '安全结账',
      subtitle: '核对收货详情，选择配送快递与支付方式，完成您的订单。',
      step_bag: '购物袋',
      step_delivery: '配送与支付',
      step_review: '核对订单',
      step_confirmation: '订单确认',
      contact_info: '联系人信息',
      contact_sub: '用于向您发送物流追踪与订单更新。',
      already_account: '已有账号？',
      log_in: '立即登录',
      full_name: '收件人姓名',
      phone_number: '联系电话 (快递联络)',
      email_address: '电子邮箱',
      newsletter_opt: '订阅 Luméa 护肤秘诀、新品发售与独家礼遇资讯。',
      delivery_dispatch: '配送与快递派发',
      delivery_sub: '选择您在柬埔寨的收货地址、快递与派送服务。',
      shipping_address: '收货地址',
      province_city: '省份 / 城市',
      street_address: '详细街道地址及门牌号',
      default_address: '默认',
      add_new_address: '添加新收货地址',
      delivery_location_pin: '精确定位 (地图标记)',
      delivery_location_hint: '在地图上精准标记您的位置，助快递员更快送达。',
      locate_me: '定位我的位置',
      select_courier: '选择柬埔寨快递服务',
      courier_hint: '覆盖金边及全国 24 省份直达配送。',
      vet_name: 'Vireak Buntham',
      vet_sub: '(VET 快递)',
      vet_tag: '全国覆盖 #1',
      jt_name: '极兔速递',
      jt_sub: 'J&T Express',
      jt_tag: '极速陆运',
      grab_name: 'GrabExpress',
      grab_sub: '即时闪送',
      grab_tag: '金边同城',
      pp_only: '仅限金边',
      concierge_name: 'Luméa 贵宾专送',
      concierge_sub: 'Concierge',
      concierge_tag: '尊享白手套',
      payment_selection: '选择支付方式',
      payment_sub: '支持主流安全便捷的柬埔寨本地与数字结算方式。',
      bakong_khqr: 'Bakong KHQR - ABA 扫码',
      instant_clearance: '秒级到账',
      khqr_desc: '使用 ABA Mobile、Bakong、Wing、ACLEDA 或任何柬埔寨银行 App 扫码。',
      all_banks: '+ 支持所有银行',
      cod_name: '货到付款 (现金 COD)',
      doorstep_handover: '送货上门当面付',
      cod_desc: '收货时可直接以美金 ($) 或瑞尔 (៛) 现金向派送骑手支付。',
      usd_cash: '美金现金',
      khr_cash: '瑞尔现金',
      zero_surcharge: '免手续费',
      order_summary: '订单摘要',
      edit_cart: '修改商品',
      review_order_btn: '核对订单详情 →',
      back_to_bag: '← 返回购物袋',
      need_help: '需要帮助？',
      contact_us: '联系护肤顾问',
      special_promo: '特别企划包邮活动',
      complimentary_delivery: '已享受全境免运费'
    },
    home: {
      hero_tag: '纯澈植物护肤科学',
      hero_title: '润泽肌底，绽放天然光芒',
      hero_sub: '以临床实证为基石，精研罕见植物精萃，为东方肌肤定制平衡与通透之美。',
      shop_all: '立即选购',
      take_quiz: '开始测肤',
      featured_title: '热销明星单品',
      featured_sub: '深受全柬女性与皮肤专科推荐的常青臻品。',
      view_all: '浏览全馆好物'
    },
    footer: {
      about_title: 'Luméa 护肤工坊',
      about_desc: '专为东南亚气候定制的当代护肤工坊。科学实证，纯澈温和，赋能自信光采。',
      shop_links: '甄选分类',
      customer_care: '专属客户关怀',
      legal_title: '工坊政策',
      copyright: '© 2026 Luméa Atelier Co., Ltd. 版权所有。',
      phnom_penh: '金边市万景岗1区诺罗敦大道123号'
    }
  }
}

export const useLocaleStore = defineStore('locale', () => {
  // 1. Language state: 'en' | 'km' | 'zh'
  const savedLocale = localStorage.getItem('lumea_locale') || 'en'
  const currentLocale = ref(savedLocale)

  // 2. Currency state: 'USD' | 'KHR' | 'CNY'
  // Auto-derived default based on language, or user's explicit preference
  const savedCurrency = localStorage.getItem('lumea_currency')
  const isCurrencyExplicit = localStorage.getItem('lumea_currency_explicit') === 'true'

  const defaultCurrencyForLocale = (loc) => {
    if (loc === 'km') return 'KHR'
    if (loc === 'zh') return 'CNY'
    return 'USD'
  }

  const currentCurrency = ref(
    savedCurrency || defaultCurrencyForLocale(savedLocale)
  )

  const hasExplicitlyPickedCurrency = ref(isCurrencyExplicit)

  // Exchange rates: $1 USD base
  const rates = {
    USD: 1.0,
    KHR: 4100.0, // Standard National Bank of Cambodia / ABA market rate
    CNY: 7.25    // Standard PBOC market rate
  }

  const symbols = {
    USD: '$',
    KHR: '៛',
    CNY: '¥'
  }

  const currencySymbol = computed(() => symbols[currentCurrency.value] || '$')

  // Set Language:
  // User Rule:
  // 1. When user selects Khmer -> currency automatically changes to Riel (KHR)
  // 2. When user selects Chinese -> currency automatically changes to Yuan (CNY)
  // 3. When user selects English -> defaults to USD (or stays Riel if explicitly chosen)
  function setLocale(loc) {
    if (!['en', 'km', 'zh'].includes(loc)) return
    currentLocale.value = loc
    localStorage.setItem('lumea_locale', loc)
    if (typeof document !== 'undefined') {
      document.documentElement.lang = loc
    }

    if (loc === 'km') {
      currentCurrency.value = 'KHR'
      localStorage.setItem('lumea_currency', 'KHR')
      hasExplicitlyPickedCurrency.value = false
      localStorage.removeItem('lumea_currency_explicit')
    } else if (loc === 'zh') {
      currentCurrency.value = 'CNY'
      localStorage.setItem('lumea_currency', 'CNY')
      hasExplicitlyPickedCurrency.value = false
      localStorage.removeItem('lumea_currency_explicit')
    } else if (loc === 'en') {
      // If user hasn't explicitly locked in a different currency, default back to USD
      if (!hasExplicitlyPickedCurrency.value) {
        currentCurrency.value = 'USD'
        localStorage.setItem('lumea_currency', 'USD')
      }
    }
  }

  // Ensure documentElement has initial lang set
  if (typeof document !== 'undefined') {
    document.documentElement.lang = currentLocale.value
  }

  // Set Currency independently:
  // User Rule: "the price also Can show in riel when user select english if they want select or has price in riel"
  function setCurrency(curr, explicit = true) {
    if (!['USD', 'KHR', 'CNY'].includes(curr)) return
    currentCurrency.value = curr
    localStorage.setItem('lumea_currency', curr)
    if (explicit) {
      hasExplicitlyPickedCurrency.value = true
      localStorage.setItem('lumea_currency_explicit', 'true')
    }
  }

  // Convert raw USD amount to the active currency value
  function convertFromUsd(usdAmount) {
    const amt = Number(usdAmount) || 0
    const rate = rates[currentCurrency.value] || 1.0
    return amt * rate
  }

  // Format price cleanly according to active currency
  function formatPrice(usdAmount, options = {}) {
    const amt = Number(usdAmount) || 0
    const curr = typeof options === 'string' ? options : (options?.currency || currentCurrency.value)

    if (curr === 'KHR') {
      const khrVal = Math.round(amt * rates.KHR)
      // Khmer format: e.g. "405,900 ៛"
      return `${khrVal.toLocaleString()} ៛`
    } else if (curr === 'CNY') {
      const cnyVal = amt * rates.CNY
      // Yuan format: e.g. "¥ 717.75"
      return `¥ ${cnyVal.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
    } else {
      // USD format: e.g. "$99.00"
      return `$${amt.toFixed(2)}`
    }
  }

  // Dual format: e.g. "405,900 ៛ ($99.00)" or "¥ 717.75 ($99.00)"
  function formatPriceDual(usdAmount) {
    const amt = Number(usdAmount) || 0
    const primary = formatPrice(amt)
    if (currentCurrency.value === 'USD') return primary
    return `${primary} ($${amt.toFixed(2)})`
  }

  // Translation helper: t('nav.shop')
  function t(path, params = {}) {
    if (!path || typeof path !== 'string') return ''
    const normalizedPath = path.toLowerCase()
    const keys = normalizedPath.split('.')
    let current = translations[currentLocale.value]
    let fallback = translations.en

    // Traverse target locale
    let val = current
    for (const k of keys) {
      if (val && typeof val === 'object' && k in val) {
        val = val[k]
      } else {
        val = undefined
        break
      }
    }

    // Fallback to English if missing
    if (val === undefined) {
      val = fallback
      for (const k of keys) {
        if (val && typeof val === 'object' && k in val) {
          val = val[k]
        } else {
          val = undefined
          break
        }
      }
    }

    if (typeof val !== 'string') {
      const lastKey = keys[keys.length - 1]
      val = lastKey.charAt(0).toUpperCase() + lastKey.slice(1).replace(/_/g, ' ')
    }

    // Param substitution: e.g. {amount} or {count}
    let res = val
    for (const [pk, pv] of Object.entries(params)) {
      res = res.replace(new RegExp(`\\{${pk}\\}`, 'g'), pv)
    }
    return res
  }

  return {
    currentLocale,
    currentCurrency,
    currencySymbol,
    hasExplicitlyPickedCurrency,
    rates,
    symbols,
    setLocale,
    setCurrency,
    convertFromUsd,
    formatPrice,
    formatPriceDual,
    t
  }
})
