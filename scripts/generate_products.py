#!/usr/bin/env python3
"""
Generates the full /products/<category>/<subcategory>/<leaf>/ tree for the
Kaleido static site, including a generic product-details.html + data.json
per leaf node with 4 placeholder products.

Re-run this script any time TAXONOMY below changes:
    python3 scripts/generate_products.py

It is a dev-time content generator, not a runtime build step — the site
stays plain static HTML/CSS/JS for GitHub Pages hosting.
"""
import hashlib, base64, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_BASE = "/kaleido_website"  # GitHub Pages project-site prefix

# ---------------------------------------------------------------- slugify --
def slugify(text):
    text = text.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")

def det_hash(seed):
    return hashlib.md5(seed.encode()).hexdigest()

def det_int(seed, mod):
    return int(det_hash(seed)[:8], 16) % mod

def gen_id(seed):
    b = bytes.fromhex(det_hash(seed))[:8]
    return base64.urlsafe_b64encode(b).decode().rstrip("=")[:10]

# ---------------------------------------------------------------- taxonomy --
# category_slug: (Display Name, blurb, is_service, [ (Subcategory Name, [Leaf names...]), ... ])
TAXONOMY = {
  "stationary-and-office-supplies": ("Stationery & Office Supplies",
    "Everyday writing, desk, filing and printing essentials for the modern workplace.", False, [
    ("Writing & Paper", ["Pens","Pencils","Markers & Highlighters","Diaries & Notebooks","Sticky Notes","Writing Pads","Journals"]),
    ("Desk & Workspace", ["Desktop Accessories","Desk Organisers","Pen Stands","File Holders","Document Trays","Desk Mats","Calendars"]),
    ("Filing & Storage", ["Files & Folders","Binders","Document Storage","Storage Boxes","Archive Supplies"]),
    ("Office Essentials", ["Staplers & Staples","Punching Machines","Scissors & Cutters","Adhesives & Tapes","Labels","Clips & Pins"]),
    ("Printing Supplies", ["Printer Paper","Copier Paper","Toners & Cartridges","Labels & Stickers"]),
  ]),
  "hygiene-supplies": ("Hygiene Supplies",
    "Personal care, washroom, cleaning and protection supplies for safe, healthy workplaces.", False, [
    ("Personal Hygiene", ["Hand Sanitizers","Hand Wash","Soaps","Wet Wipes","Tissues","Toilet Paper"]),
    ("Washroom Supplies", ["Toilet Paper","Paper Towels","Hand Dryers","Soap Dispensers","Sanitary Dispensers"]),
    ("Cleaning Supplies", ["Surface Cleaners","Floor Cleaners","Glass Cleaners","Disinfectants","Cleaning Cloths"]),
    ("Cleaning Equipment", ["Mops","Brooms","Buckets","Dustbins","Cleaning Tools"]),
    ("Personal Protection", ["Gloves","Masks","Shoe Covers","Protective Kits"]),
  ]),
  "gifting": ("Corporate Gifting",
    "The broad, everyday gifting catalogue — drinkware, gourmet, gift sets and lifestyle picks.", False, [
    ("Drinkware", ["Sippers & Bottles","Mugs","Tumblers","Flasks","Glassware"]),
    ("Food & Gourmet", ["Chocolates","Sweets","Cookies","Nuts","Gourmet Food"]),
    ("Gift Sets", ["Giftsets","Hampers","Joining Kits","Festive Hampers","Welcome Kits"]),
    ("Personal Accessories", ["Keychains","Wallets","Sunglasses","Watches","Accessories"]),
    ("Home & Lifestyle", ["Home Decor","Art & Crafts","Wellness","Travel Accessories"]),
    ("Sustainable Gifting", ["Eco-friendly Gifts","Reusable Products","Sustainable Gift Sets"]),
  ]),
  "it-and-electronics": ("IT & Electronics",
    "Computer, mobile, audio and smart-device accessories for hybrid, connected teams.", False, [
    ("Computer Accessories", ["Keyboard & Mouse","Laptop Stands","Laptop Sleeves","Laptop Bags","USB Hubs","Webcams"]),
    ("Mobile Accessories", ["PowerBanks","Chargers","Charging Cables","Wireless Chargers","Mobile Stands","Phone Accessories"]),
    ("Audio", ["Earbuds","Headphones & Earphones","Speakers","Smart Speakers"]),
    ("Smart Devices", ["Smart Watches","Fitness Bands","Smart Home Devices","Wearable Electronics"]),
    ("Appliances", ["Small Appliances","Kitchen Appliances","Personal Appliances"]),
    ("Electronics", ["Computer Peripherals","Storage Devices","Gadgets","Other Electronics"]),
  ]),
  "apparel": ("Apparel",
    "Corporate wear, uniforms and branded accessories for teams and events.", False, [
    ("Corporate Apparel", ["T-Shirts","Polo T-Shirts","Shirts","Formal Wear"]),
    ("Outerwear", ["Jackets","Hoodies","Sweatshirts"]),
    ("Bottomwear", ["Pants","Tracksuits","Joggers"]),
    ("Headwear", ["Caps","Hats"]),
    ("Uniforms", ["Corporate Uniforms","Industrial Uniforms","Hospitality Uniforms","Promotional Apparel"]),
    ("Apparel Accessories", ["Belts","Scarves","Socks","Other Accessories"]),
  ]),
  "horeca": ("HORECA",
    "Tableware, kitchen, storage and housekeeping supplies for hotels, restaurants & cafés.", False, [
    ("Tableware", ["Dinnerware & Serveware","Plates & Bowls","Cutlery","Utensils"]),
    ("Glassware & Drinkware", ["Glassware","Mugs","Cups","Beverage Service"]),
    ("Kitchen & Cooking", ["Utensils & Cookware","Kitchen Tools","Food Preparation","Kitchen Storage"]),
    ("Food Storage", ["Storage Containers","Lunch Boxes","Food Containers"]),
    ("Housekeeping", ["Cleaning Supplies","Housekeeping Equipment","Laundry Supplies"]),
    ("Hospitality Essentials", ["Guest Amenities","Room Accessories","Service Accessories"]),
  ]),
  "strategic-sourcing": ("Strategic Sourcing",
    "A procurement capability, not a fixed catalogue — custom manufacturing, bulk sourcing and packaging built around your project.", True, [
    ("Custom Manufacturing", ["Custom Products","Private Label Products","OEM Products","White Label Products"]),
    ("Bulk Procurement", ["Bulk Sourcing","Vendor Consolidation","Volume Procurement"]),
    ("Packaging", ["Custom Packaging","Gift Packaging","Sustainable Packaging","Promotional Packaging"]),
    ("Special Requirements", ["Custom Requirements","Project-Based Procurement","International Sourcing","Hard-to-Source Products"]),
    ("Industry-Specific Sourcing", ["Industrial Supplies","Facility Supplies","Promotional Merchandise","Custom Corporate Requirements"]),
  ]),
  "premium-gifting": ("Premium Gifting",
    "A curated, elevated gifting line for leadership, clients and milestone moments.", False, [
    ("Luxury Accessories", ["Watches","Wallets","Premium Sunglasses","Leather Accessories"]),
    ("Premium Technology", ["Premium Audio","Smart Devices","Luxury Gadgets"]),
    ("Premium Lifestyle", ["Home Decor","Luxury Drinkware","Premium Travel Accessories","Wellness Gifts"]),
    ("Gourmet", ["Premium Chocolates","Dry Fruits & Nuts","Gourmet Hampers","Premium Sweets"]),
    ("Executive Gifts", ["Executive Giftsets","Desk Accessories","Premium Writing Instruments","Leather Office Accessories"]),
    ("Curated Collections", ["Festive Hampers","Anniversary Gifts","Leadership Gifts","Client Gifts","Milestone Gifts"]),
  ]),
  "construction-adhesives": ("Construction Adhesives",
    "Adhesives, sealants, waterproofing and tapes sourced for facilities and construction projects.", False, [
    ("General Adhesives", ["Multi-Purpose Adhesives","Contact Adhesives","Spray Adhesives"]),
    ("Construction Adhesives", ["Tile Adhesives","Wood Adhesives","Concrete Adhesives","Stone Adhesives"]),
    ("Sealants", ["Silicone Sealants","PU Sealants","Acrylic Sealants"]),
    ("Waterproofing", ["Waterproof Coatings","Crack Fillers","Waterproof Sealants"]),
    ("Repair & Maintenance", ["Epoxy Adhesives","Instant Adhesives","Repair Compounds"]),
    ("Tapes", ["Industrial Tapes","Double-Sided Tapes","Mounting Tapes","Sealing Tapes"]),
  ]),
}

CATEGORY_ORDER = list(TAXONOMY.keys())

# ---------------------------------------------------------- dummy product data --
ADJECTIVES = ["Premium","Classic","Executive","Eco-Friendly","Compact","Deluxe",
              "Signature","Essential","Modern","Everyday","Pro","Elite"]
BRANDS = ["Nova","Vertex","Meridian","Solace","Crestline","Lumen","Trueline","Kindred",
          "Everline","Bellwood","Arcadia","Northfield","Cambria","Halcyon","Ridgeline",
          "Marlow","Windermere","Ashcroft","Fenwick","Oakhaven"]
MATERIALS = ["ABS Plastic","Anodized Aluminium","Recycled PET","Stainless Steel",
             "Bamboo & Wood","Genuine Leather","Cotton Blend","Food-Grade Silicone"]
TAGLINE_TEMPLATES = [
    "{leaf}, done right — dependable quality for corporate gifting and everyday use.",
    "A team favourite: practical {leaf_lower} built for daily reliability.",
    "Thoughtfully finished {leaf_lower} that feels as good as it looks.",
    "Everyday {leaf_lower}, elevated — perfect for gifting at scale.",
]
# Use-case tags shared with the nav mega-menu's "Shop by Occasion" column — kept as
# a single list so both stay in sync. Used to facet products *within* a leaf page
# (e.g. Pens) without ever mixing in another leaf's products (e.g. Pencils).
OCCASIONS = ["Employee Onboarding", "Work Anniversaries", "Festivals", "Birthdays",
             "Corporate Events", "Conferences", "Product Launches", "Rewards & Recognition"]

def gen_products(cat_slug, cat_name, sub_name, leaf_name, leaf_slug, is_service):
    products = []
    for i in range(4):
        seed_base = f"{cat_slug}/{leaf_slug}/{i}"
        adj = ADJECTIVES[(det_int(seed_base + "adj", 1000) + i) % len(ADJECTIVES)]
        brand = BRANDS[(det_int(seed_base + "brand", 1000) + i) % len(BRANDS)]
        name = f"{brand} {adj} {leaf_name}"
        tagline = TAGLINE_TEMPLATES[i % len(TAGLINE_TEMPLATES)].format(leaf=leaf_name, leaf_lower=leaf_name.lower())
        tiers = [499, 999, 2499, 4999]
        lower = tiers[i-1] if i > 0 else 99
        price = lower + det_int(seed_base + "price", tiers[i] - lower)
        pid = gen_id(seed_base + "id")
        slug = slugify(f"{name}-{i+1}")
        material = MATERIALS[det_int(seed_base + "mat", len(MATERIALS))]
        images = [f"https://picsum.photos/seed/{slugify(cat_slug)}-{leaf_slug}-{i}-{n}/700/700" for n in range(4)]
        blurb = ("a dependable procurement option for bulk facility or project needs" if is_service
                 else f"a popular pick for {sub_name.lower()} programs and everyday {cat_name.lower()} gifting")
        description = (f"{tagline} The {name} is {blurb}. Finished to a consistent quality standard and built for "
                        f"reliable performance, it's designed for corporate gifting, welcome kits and bulk "
                        f"procurement at scale — with logo branding and packaging customization available on request.")
        specs = {
            "Category": leaf_name,
            "Material": material,
            "Customization": "Logo branding available",
            "MOQ": f"{[25,50,100,250][i]} units",
            "Lead Time": ["5–7 business days","7–10 business days","10–14 business days","2–3 weeks"][i],
        }
        occasion_count = 2 + (det_int(seed_base + "occ-count", 2))  # 2 or 3 tags per product
        ranked = sorted(OCCASIONS, key=lambda occ: det_hash(seed_base + "occ" + occ))
        occasions = ranked[:occasion_count]
        products.append({
            "id": pid, "slug": slug, "name": name, "tagline": tagline, "price": price,
            "images": images, "description": description, "specs": specs, "occasions": occasions,
        })
    return products

# ---------------------------------------------------------------- shared HTML --
FONT_LINKS = (
  '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
  '<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap" rel="stylesheet">\n'
  f'<link rel="stylesheet" href="{SITE_BASE}/assets/css/styles.css">'
)

MEGA_MENU = f'''<div class="has-mega">
        <a href="{SITE_BASE}/products.html" class="mega-trigger">Products</a>
        <div class="mega-menu">
          <div class="mega-inner">
            <div class="mega-col">
              <h5>Shop by Occasion</h5>
              {"".join(f'<a href="{SITE_BASE}/products.html">{occ}</a>' + chr(10) + "              " for occ in OCCASIONS)}
            </div>
            <div class="mega-col">
              <h5>Shop by Category</h5>
              {"".join(f'<a href="{SITE_BASE}/products/{slug}/">{TAXONOMY[slug][0]}</a>' + chr(10) + "              " for slug in CATEGORY_ORDER)}
            </div>
          </div>
          <a href="{SITE_BASE}/products.html" class="mega-explore">Explore All Products →</a>
        </div>
      </div>'''

def nav_html():
    return f'''<header class="nav" id="siteNav">
  <div class="nav-inner">
    <a href="{SITE_BASE}/index.html#top" class="brand">
      <span class="mark">
        <img class="brand-icon" src="{SITE_BASE}/assets/img/brand-icon.png" alt="Kaleido mark">
        KALEIDO
      </span>
      <span class="tag">Multiple Categories. One Platform.</span>
    </a>
    <nav class="primary">
      {MEGA_MENU}
      <a href="{SITE_BASE}/index.html#solutions">Make It Yours</a>
      <a href="{SITE_BASE}/index.html#process">How It Works</a>
      <a href="{SITE_BASE}/index.html#clients">Clients</a>
      <a href="{SITE_BASE}/index.html#about">About Us</a>
    </nav>
    <div class="nav-ctas">
      <a href="{SITE_BASE}/products.html" class="btn btn-ghost">Explore Products</a>
      <a href="{SITE_BASE}/index.html#connect" class="btn btn-dark">Connect With Us</a>
    </div>
    <button class="hamburger" id="hamburgerBtn" aria-label="Open menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="mobile-menu" id="mobileMenu">
    <a href="{SITE_BASE}/products.html">Products</a>
    <a href="{SITE_BASE}/index.html#solutions">Make It Yours</a>
    <a href="{SITE_BASE}/index.html#process">How It Works</a>
    <a href="{SITE_BASE}/index.html#clients">Clients</a>
    <a href="{SITE_BASE}/index.html#about">About Us</a>
    <div class="mobile-ctas">
      <a href="{SITE_BASE}/products.html" class="btn btn-ghost">Explore Products</a>
      <a href="{SITE_BASE}/index.html#connect" class="btn btn-dark">Connect With Us</a>
    </div>
  </div>
</header>'''

def footer_html():
    return f'''<footer id="about">
  <div class="footer-top">
    <div class="footer-brand">
      <div class="mark">KALEIDO</div>
      <div class="tag">Multiple Categories. One Platform.</div>
      <p class="desc">Connecting requirements to products, manufacturers and supply capabilities.</p>
    </div>
    <div class="footer-col">
      <h4>Categories</h4>
      <ul>
        <li><a href="{SITE_BASE}/products/stationary-and-office-supplies/">Stationery &amp; Office Supplies</a></li>
        <li><a href="{SITE_BASE}/products/hygiene-supplies/">Hygiene Supplies</a></li>
        <li><a href="{SITE_BASE}/products/gifting/">Corporate Gifting</a></li>
        <li><a href="{SITE_BASE}/products/it-and-electronics/">IT &amp; Electronics</a></li>
        <li><a href="{SITE_BASE}/products/apparel/">Apparel</a></li>
        <li><a href="{SITE_BASE}/products.html">View All Categories</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Solutions</h4>
      <ul>
        <li><a href="{SITE_BASE}/index.html#solutions">Business</a></li>
        <li><a href="{SITE_BASE}/products/strategic-sourcing/">Strategic Sourcing</a></li>
        <li><a href="{SITE_BASE}/index.html#solutions">Employee Solutions</a></li>
        <li><a href="{SITE_BASE}/index.html#solutions">Events &amp; Marketing</a></li>
        <li><a href="{SITE_BASE}/index.html#solutions">Institutional</a></li>
        <li><a href="{SITE_BASE}/products/strategic-sourcing/">Custom Solutions</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Ecosystem</h4>
      <ul>
        <li><a href="{SITE_BASE}/index.html#process">Manufacturers</a></li>
        <li><a href="{SITE_BASE}/index.html#process">Warehousing</a></li>
        <li><a href="{SITE_BASE}/index.html#process">Customization</a></li>
        <li><a href="{SITE_BASE}/index.html#process">Packaging</a></li>
        <li><a href="{SITE_BASE}/index.html#process">Logistics</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <ul>
        <li><a href="{SITE_BASE}/index.html#about">About Us</a></li>
        <li><a href="{SITE_BASE}/index.html#clients">Clients &amp; Testimonials</a></li>
        <li><a href="{SITE_BASE}/index.html#connect">Insights</a></li>
        <li><a href="{SITE_BASE}/index.html#connect">Contact</a></li>
        <li><a href="{SITE_BASE}/index.html#connect">Become a Partner</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 Kaleido. All rights reserved.</span>
    <div class="legal">
      <a href="#">Privacy Policy</a>
      <a href="#">Terms</a>
    </div>
    <div class="social">
      <a href="#" aria-label="LinkedIn">LinkedIn</a>
      <a href="#" aria-label="Instagram">Instagram</a>
    </div>
  </div>
</footer>'''

def page_shell(title, description, body, extra_script=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
{FONT_LINKS}
</head>
<body>

{nav_html()}

<main>
{body}
</main>

{footer_html()}

<script src="{SITE_BASE}/assets/js/main.js"></script>
{extra_script}
</body>
</html>
'''

def breadcrumb(items):
    # items: list of (label, href_or_None) or (label, href_or_None, siblings)
    # siblings: optional list of (sib_label, sib_href) rendered as a hover dropdown,
    # letting a visitor jump sideways (e.g. to another leaf) without backtracking.
    parts = []
    for i, item in enumerate(items):
        label, href = item[0], item[1]
        siblings = item[2] if len(item) > 2 else None
        if i > 0:
            parts.append('<span class="sep">/</span>')
        if href and siblings:
            menu = "".join(
                f'<a class="{"is-current" if sib_label == label else ""}" href="{sib_href}">{sib_label}</a>'
                for sib_label, sib_href in siblings
            )
            parts.append(f'<span class="crumb-drop"><a href="{href}">{label}</a><span class="crumb-menu">{menu}</span></span>')
        elif href:
            parts.append(f'<a href="{href}">{label}</a>')
        else:
            parts.append(f'<span class="current">{label}</span>')
    return '<div class="breadcrumb">' + "".join(parts) + '</div>'

# ---------------------------------------------------------------- writers --
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

def build_category_page(cat_slug, cat_name, blurb, is_service, subs):
    cards = []
    for sub_name, leaves in subs:
        sub_slug = slugify(sub_name)
        seed = f"{cat_slug}-{sub_slug}"
        img = f"https://picsum.photos/seed/{seed}/160/160"
        href = f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/"
        cards.append(f'<a class="corp-card" href="{href}"><span class="corp-icon"><img src="{img}" alt="{sub_name}" loading="lazy"></span><span>{sub_name}</span></a>')
    all_cats_siblings = [(TAXONOMY[s][0], f"{SITE_BASE}/products/{s}/") for s in CATEGORY_ORDER]
    hero_img = f"https://picsum.photos/seed/kaleido-hero-{cat_slug}/900/560"

    # ---- "Shop All" flat, faceted listing: a Uline/Grainger-style bypass so a
    # visitor can go straight from the category page to a product without
    # clicking through every subcategory/leaf page in between. Those pages
    # still exist and are still linked above/from the mega-menu (kept for
    # deep-linking + SEO) — this just adds a second, faster path to the same products.
    all_products = []
    sub_counts = {}
    for sub_name, leaves in subs:
        sub_slug = slugify(sub_name)
        sub_counts[sub_slug] = 0
        for leaf_name in leaves:
            leaf_slug = slugify(leaf_name)
            for p in gen_products(cat_slug, cat_name, sub_name, leaf_name, leaf_slug, is_service):
                detail_href = f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/{leaf_slug}/product-details.html?id={p['id']}&slug={p['slug']}"
                all_products.append((sub_slug, p, detail_href))
                sub_counts[sub_slug] += 1

    shop_cards = []
    for sub_slug, p, detail_href in all_products:
        shop_cards.append(f'''<a class="item-card" href="{detail_href}" data-sub="{sub_slug}" data-price="{p['price']}">
        <div class="item-img"><img src="{p['images'][0]}" alt="{p['name']}" loading="lazy"></div>
        <div class="item-body">
          <div class="item-name">{p['name']}</div>
          <div class="item-tagline">{p['tagline']}</div>
          <div class="item-price">₹{p['price']:,}</div>
        </div>
      </a>''')

    sub_facet_buttons = [f'<button class="active" data-sub-filter="all">All <span class="count">{len(all_products)}</span></button>']
    for sub_name, leaves in subs:
        sub_slug = slugify(sub_name)
        sub_facet_buttons.append(f'<button data-sub-filter="{sub_slug}">{sub_name} <span class="count">{sub_counts[sub_slug]}</span></button>')

    price_facet_buttons = '''<button class="active" data-price-filter="999999">All</button>
      <button data-price-filter="500">Under ₹500</button>
      <button data-price-filter="1000">Under ₹1,000</button>
      <button data-price-filter="2500">Under ₹2,500</button>
      <button data-price-filter="5000">Under ₹5,000</button>'''

    body = f'''
<section class="bg-beige" id="top">
  <div class="section-inner catalog-top">
    {breadcrumb([("All Categories", f"{SITE_BASE}/products.html", all_cats_siblings), (cat_name, None)])}
    <div class="catalog-hero-grid">
      <div class="section-head catalog reveal">
        <span class="eyebrow">{"Sourcing Capability" if is_service else "Category"}</span>
        <h1>{cat_name}</h1>
        <p>{blurb}</p>
      </div>
      <div class="catalog-hero-media reveal"><img src="{hero_img}" alt="{cat_name}" loading="lazy"></div>
    </div>
  </div>
</section>
<section class="bg-white">
  <div class="section-inner catalog-bottom">
    <div class="corp-grid reveal-stag">
      {chr(10).join(cards)}
    </div>
  </div>
</section>
<section class="bg-white" id="shop-all">
  <div class="section-inner" style="padding-top:0;">
    <div class="shop-all-divider">Or shop every {cat_name.lower()} product in one place</div>
    <div class="shop-all-layout">
      <aside class="shop-all-sidebar">
        <div class="facet">
          <h6>Subcategory</h6>
          <div class="facet-list" id="subFacet">{"".join(sub_facet_buttons)}</div>
        </div>
        <div class="facet">
          <h6>{"Indicative Scale" if is_service else "Budget"}</h6>
          <div class="facet-list" id="priceFacet">{price_facet_buttons}</div>
        </div>
      </aside>
      <div>
        <div class="shop-all-count" id="shopAllCount">{len(all_products)} products</div>
        <div class="item-grid" id="shopAllGrid">
          {chr(10).join(shop_cards)}
        </div>
      </div>
    </div>
    <a href="{SITE_BASE}/index.html#connect" class="prod-cta-banner reveal" style="margin-top:44px;">
      <div>
        <h3>Can't find what you're looking for?</h3>
        <p>Talk to our team about sourcing or customizing for your specific requirement.</p>
      </div>
      <span class="btn btn-light">Connect With Us →</span>
    </a>
  </div>
</section>'''
    script = '''<script>
(function(){
  var subBtns = document.querySelectorAll('#subFacet button');
  var priceBtns = document.querySelectorAll('#priceFacet button');
  var cards = document.querySelectorAll('#shopAllGrid .item-card');
  var countEl = document.getElementById('shopAllCount');
  var activeSub = 'all', activeMax = 999999;
  function apply(){
    var visible = 0;
    cards.forEach(function(card){
      var matchesSub = activeSub === 'all' || card.getAttribute('data-sub') === activeSub;
      var matchesPrice = parseInt(card.getAttribute('data-price'), 10) <= activeMax;
      var show = matchesSub && matchesPrice;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    countEl.textContent = visible + (visible === 1 ? ' product' : ' products');
  }
  subBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      subBtns.forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      activeSub = btn.getAttribute('data-sub-filter');
      apply();
    });
  });
  priceBtns.forEach(function(btn){
    btn.addEventListener('click', function(){
      priceBtns.forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      activeMax = parseInt(btn.getAttribute('data-price-filter'), 10);
      apply();
    });
  });
})();
</script>'''
    title = f"{cat_name} — Kaleido"
    desc = f"Browse {cat_name} subcategories from Kaleido's corporate sourcing catalogue. {blurb}"
    out = os.path.join(ROOT, "products", cat_slug, "index.html")
    write(out, page_shell(title, desc, body, extra_script=script))

def build_subcategory_page(cat_slug, cat_name, sub_name, leaves, is_service):
    sub_slug = slugify(sub_name)
    cards = []
    for leaf_name in leaves:
        leaf_slug = slugify(leaf_name)
        seed = f"{cat_slug}-{sub_slug}-{leaf_slug}"
        img = f"https://picsum.photos/seed/{seed}/160/160"
        href = f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/{leaf_slug}/"
        cards.append(f'<a class="corp-card" href="{href}"><span class="corp-icon"><img src="{img}" alt="{leaf_name}" loading="lazy"></span><span>{leaf_name}</span></a>')
    all_cats_siblings = [(TAXONOMY[s][0], f"{SITE_BASE}/products/{s}/") for s in CATEGORY_ORDER]
    sub_siblings = [(sn, f"{SITE_BASE}/products/{cat_slug}/{slugify(sn)}/") for sn, _ in TAXONOMY[cat_slug][3]]
    hero_img = f"https://picsum.photos/seed/kaleido-hero-{cat_slug}-{sub_slug}/900/560"
    body = f'''
<section class="bg-beige" id="top">
  <div class="section-inner catalog-top">
    {breadcrumb([("All Categories", f"{SITE_BASE}/products.html", all_cats_siblings), (cat_name, f"{SITE_BASE}/products/{cat_slug}/", sub_siblings), (sub_name, None)])}
    <div class="catalog-hero-grid">
      <div class="section-head catalog reveal">
        <span class="eyebrow">{cat_name}</span>
        <h1>{sub_name}</h1>
        <p>Explore every product line under {sub_name.lower()} — pick a subcategory below or search for exactly what you need.</p>
      </div>
      <div class="catalog-hero-media reveal"><img src="{hero_img}" alt="{sub_name}" loading="lazy"></div>
    </div>
    <form class="search-bar reveal" onsubmit="return false;">
      <input type="text" placeholder="Search what's in your mind">
      <button type="submit"><span>Search</span> 🔍</button>
    </form>
  </div>
</section>
<section class="bg-white">
  <div class="section-inner catalog-bottom">
    <div class="corp-grid reveal-stag">
      {chr(10).join(cards)}
    </div>
  </div>
</section>'''
    title = f"{sub_name} — {cat_name} — Kaleido"
    desc = f"{sub_name} under {cat_name}: browse product lines and find exactly what your organization needs."
    out = os.path.join(ROOT, "products", cat_slug, sub_slug, "index.html")
    write(out, page_shell(title, desc, body))

def build_leaf_page(cat_slug, cat_name, sub_name, leaf_name, is_service):
    sub_slug = slugify(sub_name)
    leaf_slug = slugify(leaf_name)
    products = gen_products(cat_slug, cat_name, sub_name, leaf_name, leaf_slug, is_service)

    # write data.json for this leaf (consumed by product-details.html)
    data_out = os.path.join(ROOT, "products", cat_slug, sub_slug, leaf_slug, "data.json")
    write(data_out, json.dumps({
        "category": cat_name, "categorySlug": cat_slug,
        "subcategory": sub_name, "subcategorySlug": sub_slug,
        "leaf": leaf_name, "leafSlug": leaf_slug,
        "products": products,
    }, indent=2))

    # ---- Snappy (browse-gifts)-style layout: a top filter bar + left checkbox
    # sidebar. The sidebar facets by *occasion* (Employee Onboarding, Festivals,
    # etc.), not by sibling leaf — a leaf page shows only that leaf's own products
    # (Pens only ever shows Pens), the checkboxes just narrow which of its own
    # products match a use case. Checking multiple occasions is OR'd together;
    # the price tabs then AND against that.
    all_cards = []
    for p in products:
        detail_href = f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/{leaf_slug}/product-details.html?id={p['id']}&slug={p['slug']}"
        occ_slugs = " ".join(slugify(o) for o in p["occasions"])
        all_cards.append(f'''<a class="item-card" href="{detail_href}" data-occasions="{occ_slugs}" data-price="{p['price']}">
        <div class="item-img"><img src="{p['images'][0]}" alt="{p['name']}" loading="lazy"></div>
        <div class="item-body">
          <div class="item-name">{p['name']}</div>
          <div class="item-tagline">{p['tagline']}</div>
          <div class="item-price">₹{p['price']:,}</div>
        </div>
      </a>''')

    occasion_checkboxes = []
    for occ in OCCASIONS:
        occ_slug = slugify(occ)
        count = sum(1 for p in products if occ in p["occasions"])
        occasion_checkboxes.append(
            f'<label><input type="checkbox" data-occasion-filter="{occ_slug}">{occ}<span class="count">{count}</span></label>'
        )

    tabs_label = "Budget" if not is_service else "Indicative Scale"
    all_cats_siblings = [(TAXONOMY[s][0], f"{SITE_BASE}/products/{s}/") for s in CATEGORY_ORDER]
    sub_siblings = [(sn, f"{SITE_BASE}/products/{cat_slug}/{slugify(sn)}/") for sn, _ in TAXONOMY[cat_slug][3]]
    leaf_siblings = [(ln, f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/{slugify(ln)}/") for ln in dict(TAXONOMY[cat_slug][3])[sub_name]]
    hero_img = f"https://picsum.photos/seed/kaleido-hero-{cat_slug}-{leaf_slug}/900/560"
    body = f'''
<section class="bg-beige" id="top">
  <div class="section-inner catalog-top">
    {breadcrumb([("All Categories", f"{SITE_BASE}/products.html", all_cats_siblings), (cat_name, f"{SITE_BASE}/products/{cat_slug}/", sub_siblings), (sub_name, f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/", leaf_siblings), (leaf_name, None)])}
    <div class="catalog-hero-grid">
      <div class="section-head catalog reveal">
        <span class="eyebrow">{sub_name}</span>
        <h1>{leaf_name}</h1>
        <p>Indicative {leaf_name.lower()} options{" for your procurement requirement" if is_service else " for your corporate gifting or workplace requirement"}. Sample listing shown below — final assortment is confirmed with our sourcing team.</p>
      </div>
      <div class="catalog-hero-media reveal"><img src="{hero_img}" alt="{leaf_name}" loading="lazy"></div>
    </div>
  </div>
</section>
<section class="bg-white">
  <div class="section-inner catalog-bottom">
    <div class="browse-topbar">
      <div class="browse-topbar-left">
        <span class="filters-label">Filters</span>
        <button class="reset-link" id="resetFilters">Reset</button>
      </div>
      <div class="price-tabs" id="priceTabs" data-label="{tabs_label}">
        <button class="price-tab active" data-max="999999">All</button>
        <button class="price-tab" data-max="500">Under ₹500</button>
        <button class="price-tab" data-max="1000">Under ₹1,000</button>
        <button class="price-tab" data-max="2500">Under ₹2,500</button>
        <button class="price-tab" data-max="5000">Under ₹5,000</button>
      </div>
    </div>
    <div class="browse-layout">
      <aside class="browse-sidebar">
        <h6>Shop By Occasion</h6>
        <div class="checkbox-list" id="occasionFacet">
          {chr(10).join(occasion_checkboxes)}
        </div>
      </aside>
      <div>
        <div class="shop-all-count" id="leafGridCount">{len(products)} products</div>
        <div class="item-grid" id="itemGrid">
          {chr(10).join(all_cards)}
        </div>
      </div>
    </div>
    <a href="{SITE_BASE}/index.html#connect" class="prod-cta-banner reveal" style="margin-top:44px;">
      <div>
        <h3>Looking for something specific?</h3>
        <p>Share your requirement and our team will source or customize it for you.</p>
      </div>
      <span class="btn btn-light">Connect With Us →</span>
    </a>
  </div>
</section>'''
    script = '''<script>
(function(){
  var priceTabs = document.querySelectorAll('.price-tab');
  var occBoxes = document.querySelectorAll('#occasionFacet input[type=checkbox]');
  var cards = document.querySelectorAll('#itemGrid .item-card');
  var countEl = document.getElementById('leafGridCount');
  var activeMax = 999999;
  function apply(){
    var activeOccasions = [];
    occBoxes.forEach(function(box){ if (box.checked) activeOccasions.push(box.getAttribute('data-occasion-filter')); });
    var visible = 0;
    cards.forEach(function(card){
      var cardOccasions = card.getAttribute('data-occasions').split(' ');
      var matchesOccasion = activeOccasions.length === 0 || activeOccasions.some(function(o){ return cardOccasions.indexOf(o) !== -1; });
      var matchesPrice = parseInt(card.getAttribute('data-price'), 10) <= activeMax;
      var show = matchesOccasion && matchesPrice;
      card.style.display = show ? '' : 'none';
      if (show) visible++;
    });
    countEl.textContent = visible + (visible === 1 ? ' product' : ' products');
  }
  occBoxes.forEach(function(box){ box.addEventListener('change', apply); });
  priceTabs.forEach(function(tab){
    tab.addEventListener('click', function(){
      priceTabs.forEach(function(t){ t.classList.remove('active'); });
      tab.classList.add('active');
      activeMax = parseInt(tab.getAttribute('data-max'), 10);
      apply();
    });
  });
  document.getElementById('resetFilters').addEventListener('click', function(){
    occBoxes.forEach(function(box){ box.checked = false; });
    priceTabs.forEach(function(t){ t.classList.remove('active'); });
    priceTabs[0].classList.add('active');
    activeMax = 999999;
    apply();
  });
})();
</script>'''
    title = f"{leaf_name} — {sub_name} — Kaleido"
    desc = f"Browse {leaf_name} options under {sub_name} ({cat_name}) from Kaleido's corporate sourcing catalogue."
    out = os.path.join(ROOT, "products", cat_slug, sub_slug, leaf_slug, "index.html")
    write(out, page_shell(title, desc, body, extra_script=script))
    build_product_details_page(cat_slug, cat_name, sub_name, leaf_name)

def build_product_details_page(cat_slug, cat_name, sub_name, leaf_name):
    sub_slug = slugify(sub_name)
    leaf_slug = slugify(leaf_name)
    all_cats_siblings = [(TAXONOMY[s][0], f"{SITE_BASE}/products/{s}/") for s in CATEGORY_ORDER]
    sub_siblings = [(sn, f"{SITE_BASE}/products/{cat_slug}/{slugify(sn)}/") for sn, _ in TAXONOMY[cat_slug][3]]
    leaf_siblings = [(ln, f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/{slugify(ln)}/") for ln in dict(TAXONOMY[cat_slug][3])[sub_name]]
    body = f'''
<section class="bg-beige" id="top">
  <div class="section-inner" style="padding-bottom:0;">
    {breadcrumb([("All Categories", f"{SITE_BASE}/products.html", all_cats_siblings), (cat_name, f"{SITE_BASE}/products/{cat_slug}/", sub_siblings), (sub_name, f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/", leaf_siblings), (leaf_name, f"{SITE_BASE}/products/{cat_slug}/{sub_slug}/{leaf_slug}/"), ("Product", None)])}
  </div>
</section>
<section class="bg-white">
  <div class="section-inner" id="pdpRoot">
    <div class="pdp-loading">Loading product…</div>
  </div>
</section>'''
    script = f'''<script>
(function(){{
  var params = new URLSearchParams(window.location.search);
  var id = params.get('id');
  fetch('data.json').then(function(r){{ return r.json(); }}).then(function(data){{
    var product = data.products.find(function(p){{ return p.id === id; }}) || data.products[0];
    var root = document.getElementById('pdpRoot');
    var thumbs = product.images.map(function(src, i){{
      return '<button class="' + (i===0 ? 'active' : '') + '" data-idx="' + i + '"><img src="' + src + '" alt="' + product.name + ' view ' + (i+1) + '"></button>';
    }}).join('');
    var specs = Object.keys(product.specs).map(function(k){{
      return '<dt>' + k + '</dt><dd>' + product.specs[k] + '</dd>';
    }}).join('');
    root.innerHTML =
      '<div class="pdp-grid">' +
        '<div class="pdp-gallery">' +
          '<div class="pdp-main-img"><img id="pdpMainImg" src="' + product.images[0] + '" alt="' + product.name + '"></div>' +
          '<div class="pdp-thumbs">' + thumbs + '</div>' +
        '</div>' +
        '<div class="pdp-info">' +
          '<span class="eyebrow">{sub_name}</span>' +
          '<h1>' + product.name + '</h1>' +
          '<div class="pdp-price">₹' + product.price.toLocaleString('en-IN') + '</div>' +
          '<p class="pdp-desc">' + product.description + '</p>' +
          '<div class="pdp-specs"><dl>' + specs + '</dl></div>' +
          '<div class="pdp-ctas">' +
            '<a href="{SITE_BASE}/index.html#connect" class="btn btn-dark">Enquire Now</a>' +
            '<a href="{SITE_BASE}/products/{cat_slug}/{sub_slug}/{leaf_slug}/" class="btn btn-ghost">Back to {leaf_name}</a>' +
          '</div>' +
        '</div>' +
      '</div>';
    document.title = product.name + ' — Kaleido';
    root.querySelectorAll('.pdp-thumbs button').forEach(function(btn){{
      btn.addEventListener('click', function(){{
        root.querySelectorAll('.pdp-thumbs button').forEach(function(b){{ b.classList.remove('active'); }});
        btn.classList.add('active');
        document.getElementById('pdpMainImg').src = product.images[parseInt(btn.getAttribute('data-idx'), 10)];
      }});
    }});
  }}).catch(function(){{
    document.getElementById('pdpRoot').innerHTML = '<div class="pdp-loading">Product not found.</div>';
  }});
}})();
</script>'''
    title = f"{leaf_name} — Product — Kaleido"
    desc = f"Product details for {leaf_name} under {sub_name} ({cat_name}) from Kaleido."
    out = os.path.join(ROOT, "products", cat_slug, sub_slug, leaf_slug, "product-details.html")
    write(out, page_shell(title, desc, body, extra_script=script))

def main():
    products_dir = os.path.join(ROOT, "products")
    for cat_slug in CATEGORY_ORDER:
        cat_dir = os.path.join(products_dir, cat_slug)
        if os.path.isdir(cat_dir):
            shutil.rmtree(cat_dir)

    total_leaves = 0
    for cat_slug, (cat_name, blurb, is_service, subs) in TAXONOMY.items():
        build_category_page(cat_slug, cat_name, blurb, is_service, subs)
        for sub_name, leaves in subs:
            build_subcategory_page(cat_slug, cat_name, sub_name, leaves, is_service)
            for leaf_name in leaves:
                build_leaf_page(cat_slug, cat_name, sub_name, leaf_name, is_service)
                total_leaves += 1
    print(f"Generated {len(TAXONOMY)} category pages, "
          f"{sum(len(s) for _,_,_,s in TAXONOMY.values())} subcategory pages, "
          f"{total_leaves} leaf pages (+ product-details.html + data.json each).")

if __name__ == "__main__":
    main()
