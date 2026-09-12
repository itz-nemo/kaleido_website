#!/usr/bin/env python3
"""
Generates the Kaleido blog: blog.html (listing) + blog/<slug>/index.html (posts).

Structure/format is inspired by robotostudio.com/blog (featured post banner,
category filter chips, 3-up card grid, and a post-detail layout with a TL;DR
box + sticky table-of-contents) — reskinned entirely in Kaleido's own brand
(colours/fonts/components), no copy or imagery reused from that site.

Re-run any time BLOG_POSTS changes:
    python3 scripts/generate_blog.py

Shares nav/footer/page-shell with the products generator so the two stay in
sync automatically — this is a thin, separate script rather than folding into
generate_products.py because a blog post isn't part of the product taxonomy.
"""
import os, re
from generate_products import SITE_BASE, ROOT, page_shell, breadcrumb, write, slugify

# ---------------------------------------------------------------- content --
# All content here is placeholder/dummy, written for this site — no real posts yet.
BLOG_POSTS = [
    {
        "slug": "sourcing-not-catalogue",
        "featured": True,
        "category": "Sourcing",
        "read_min": 12,
        "date": "September 2, 2026",
        "title": "How we treat corporate gifting as a sourcing problem, not a catalogue",
        "excerpt": "Most gifting platforms sell you a catalogue and hope the order fits. We built a sourcing network instead — here's the difference it makes when a procurement team actually needs something in bulk, on time, and customized.",
        "author": "Kaleido Team",
        "image_seed": "kaleido-blog-sourcing",
        "tldr": "Catalogues are optimized for browsing, not for procurement at scale. A sourcing network — manufacturer relationships, flexible MOQs, in-house customization — bends around the requirement instead of forcing the requirement to fit pre-made SKUs. That's the whole difference between a gifting website and a sourcing partner.",
        "sections": [
            ("The problem with catalogue-first gifting",
             "<p>Most corporate gifting sites work like any other e-commerce store: a fixed SKU, a fixed price, a fixed MOQ, and a checkout flow that assumes you're ordering exactly what's on the page. That's a fine model for an individual buying one water bottle.</p>"
             "<p>It breaks down the moment a procurement team needs 400 welcome kits with a logo on them, delivered to three offices, on a budget that doesn't match any of the pre-set tiers. Suddenly the catalogue isn't the solution — it's the constraint.</p>"),
            ("What a sourcing network actually does differently",
             "<p>A sourcing network doesn't start from \"what's in stock.\" It starts from the requirement — quantity, budget, timeline, branding — and works backward to the right combination of manufacturer, material, and finish. The product you land on might not exist as a listed SKU anywhere, because it's assembled to fit your brief rather than the other way around.</p>"
             "<ul><li>Flexible minimum order quantities instead of fixed pack sizes</li>"
             "<li>Direct manufacturer relationships across categories, not a single warehouse of pre-bought stock</li>"
             "<li>Pricing that reflects your actual volume, not a public list price</li></ul>"),
            ("Manufacturer relationships, not just inventory",
             "<p>The nine categories on this site — stationery, hygiene, apparel, IT accessories and the rest — aren't nine warehouses. They're nine networks of manufacturers we've already vetted for quality and lead time, so a request in any of them can move straight to production instead of waiting on a listing to be created first.</p>"),
            ("Customization without the lead-time tax",
             "<p>Logo branding, packaging, and colourways are usually where a \"simple\" order turns into a six-week wait. Because customization is built into how the network operates — not bolted on as an afterthought — it doesn't multiply the timeline the way it does when a request has to be routed to a separate print vendor after the fact.</p>"),
            ("What this means for procurement teams",
             "<p>In practice: fewer rounds of \"sorry, that's not available in that quantity,\" fewer separate vendors to manage for branding versus product versus packaging, and a quote that's built around your actual requirement rather than the closest pre-made bundle.</p>"),
        ],
    },
    {
        "slug": "onboarding-kits-that-get-used",
        "featured": False,
        "category": "Onboarding",
        "read_min": 7,
        "date": "August 18, 2026",
        "title": "Employee onboarding kits that actually get used",
        "excerpt": "Most welcome kits end up in a drawer by week two. A few practical rules for building one your new hires actually keep on their desk.",
        "author": "Kaleido Team",
        "image_seed": "kaleido-blog-onboarding",
        "tldr": "Build the kit around what a new hire needs at their desk in week one, not around what looks good in an unboxing photo. Fewer, more useful items beat a bigger box every time — and the things people actually keep are the ones that solve a small daily annoyance.",
        "sections": [
            ("Start with the desk, not the box",
             "<p>The best onboarding kits are designed backward from a new hire's first Monday: a decent notebook, a pen that doesn't skip, a laptop stand if they're hybrid, a water bottle they'll actually refill. None of that is exciting to unbox. All of it gets used every day, which is the entire point.</p>"),
            ("Skip the logo-everything reflex",
             "<p>A logo on every single item reads as merchandise, not a gift. Branding the box and one or two hero items — a notebook cover, a mug — usually lands better than stamping the mark on the pen, the coaster, and the keychain too.</p>"),
            ("Bundle for the first week, not the first day",
             "<p>A kit that only makes sense on day one (balloons, a giant welcome sign) gets thrown out by day two. A kit that's useful through the first week — desk setup, a few snacks for the first few late evenings, something to write in during onboarding sessions — keeps earning its shelf space.</p>"),
            ("Measure what gets used",
             "<p>If you're running onboarding kits at any scale, it's worth asking new hires 30 days in what they still have on their desk. That's a far better signal than what got the most \"oohs\" during unboxing, and it's the number we look at when we help a team refresh a kit.</p>"),
        ],
    },
    {
        "slug": "hidden-costs-of-ad-hoc-procurement",
        "featured": False,
        "category": "Procurement",
        "read_min": 9,
        "date": "July 30, 2026",
        "title": "The hidden costs of ad-hoc procurement (and how to fix them)",
        "excerpt": "Every one-off purchase order looks small on its own. Add them up across a year and most teams are paying for the same convenience three times over.",
        "author": "Kaleido Team",
        "image_seed": "kaleido-blog-procurement",
        "tldr": "Ad-hoc, single-vendor purchase orders feel fast in the moment but quietly cost more in premium pricing, duplicated vendor management, and inconsistent quality. Consolidating recurring categories — without adding a heavier approval process — is usually the cheapest change a procurement team can make.",
        "sections": [
            ("The maverick spend problem",
             "<p>Almost every organization has it: a department that needed something quickly, found a vendor on their own, and paid retail because going through the \"proper\" channel would have taken two weeks. Multiply that across departments and a full year, and it adds up to real, invisible spend that never shows up as a single line item.</p>"),
            ("What it actually costs beyond the invoice",
             "<ul><li>Retail or near-retail pricing instead of volume rates</li>"
             "<li>A different vendor relationship (and different invoice, tax paperwork, and quality bar) for every one-off order</li>"
             "<li>No consistency in quality or branding across departments buying the \"same\" thing separately</li></ul>"),
            ("Consolidation without the bureaucracy",
             "<p>The usual fix — route everything through central procurement — often just recreates the original problem by making every request slower. The better fix is a standing relationship with a sourcing partner across your recurring categories, so a department can still request quickly, but it lands through one relationship instead of ten.</p>"),
            ("A simple way to start",
             "<p>Pick the two or three categories your organization buys most often in small, disconnected batches — stationery and onboarding kits are common ones — and consolidate just those first. It's a smaller change than a full procurement overhaul, and it's usually where the savings show up fastest.</p>"),
        ],
    },
    {
        "slug": "sustainable-gifting-that-isnt-greenwashing",
        "featured": False,
        "category": "Sustainability",
        "read_min": 8,
        "date": "July 9, 2026",
        "title": "Sustainable corporate gifting: what \"eco-friendly\" should actually mean",
        "excerpt": "A bamboo pen with a plastic cap isn't a sustainability strategy. Some questions worth asking before you brief your next gifting vendor.",
        "author": "Kaleido Team",
        "image_seed": "kaleido-blog-sustainability",
        "tldr": "\"Eco-friendly\" gets attached to a lot of products that are mostly plastic with one sustainable-sounding material somewhere on them. Ask about the whole product, the packaging, and how long it's built to last — not just the headline material.",
        "sections": [
            ("The bamboo-pen problem",
             "<p>A pen with a bamboo barrel and a plastic ink cartridge, clip, and tip is still, by weight, mostly plastic. That's not a knock on bamboo pens specifically — it's a reminder that a single sustainable-sounding material doesn't make the whole product sustainable, and it's worth looking past the marketing material to what's actually in the item.</p>"),
            ("Questions worth asking before you order",
             "<ul><li>What percentage of the product, by weight or volume, is the sustainable material actually claimed for?</li>"
             "<li>Is the packaging itself recyclable or minimal, or does the sustainable product ship in a plastic-heavy box?</li>"
             "<li>Is there a real certification behind the claim, or just a word on the product page?</li></ul>"),
            ("Durability is a sustainability feature",
             "<p>A well-made steel bottle that lasts five years is very often a better sustainability choice than a \"compostable\" item that gets used twice and thrown away — because it never needed replacing in the first place. Longevity rarely gets the same attention as material sourcing, but it usually matters more.</p>"),
            ("Packaging counts too",
             "<p>It's easy to sustainability-audit the gift and skip the box it arrives in. Bulk corporate orders multiply packaging waste fast, so it's worth asking your sourcing partner about the shipping and unit packaging just as closely as the product itself.</p>"),
        ],
    },
]


def read_time_label(mins):
    return f"{mins} MIN READ"


def post_url(slug):
    return f"{SITE_BASE}/blog/{slug}/"


def toc_id(heading):
    return slugify(heading)


def author_initials(name):
    parts = name.split()
    return "".join(p[0] for p in parts[:2]).upper()


def render_post_card(post, featured_badge=False):
    heading_tag = "h3" if featured_badge else "h4"
    return f'''<a class="post-card" href="{post_url(post['slug'])}">
      <div class="post-card-media"><img src="https://picsum.photos/seed/{post['image_seed']}/700/560" alt="{post['title']}" loading="lazy"></div>
      <div class="post-card-body">
        <div class="post-meta">{read_time_label(post['read_min'])}<span class="sep">•</span>{post['date'].upper()}</div>
        <{heading_tag}>{post['title']}</{heading_tag}>
        <p>{post['excerpt']}</p>
        <div class="post-card-foot">
          <div class="post-author"><span class="author-avatar">{author_initials(post['author'])}</span>{post['author']}</div>
          <span class="read-link">Read post →</span>
        </div>
      </div>
    </a>'''


def build_blog_index():
    featured = next(p for p in BLOG_POSTS if p["featured"])
    rest = [p for p in BLOG_POSTS if not p["featured"]]
    categories = sorted({p["category"] for p in BLOG_POSTS})

    filter_chips = ['<button class="price-tab active" data-cat-filter="all">All</button>']
    filter_chips += [f'<button class="price-tab" data-cat-filter="{slugify(c)}">{c}</button>' for c in categories]

    featured_block = f'''<a class="featured-post" href="{post_url(featured['slug'])}" data-cat="{slugify(featured['category'])}">
      <div class="featured-post-media"><img src="https://picsum.photos/seed/{featured['image_seed']}/900/700" alt="{featured['title']}" loading="lazy"></div>
      <div class="featured-post-body">
        <span class="featured-tag">Featured</span>
        <div class="post-meta">{read_time_label(featured['read_min'])}<span class="sep">•</span>{featured['date'].upper()}</div>
        <h3>{featured['title']}</h3>
        <p>{featured['excerpt']}</p>
        <div class="post-author"><span class="author-avatar">{author_initials(featured['author'])}</span>{featured['author']}</div>
      </div>
    </a>'''

    cards = []
    for p in rest:
        card_html = render_post_card(p)
        card_html = card_html.replace('class="post-card"', f'class="post-card" data-cat="{slugify(p["category"])}"', 1)
        cards.append(card_html)

    body = f'''
<section class="bg-beige" id="top">
  <div class="section-inner catalog-top">
    {breadcrumb([("Home", f"{SITE_BASE}/index.html"), ("Blog", None)])}
    <div class="section-head catalog reveal">
      <span class="eyebrow">Insights</span>
      <h1>The Kaleido Blog</h1>
      <p>Notes on corporate gifting, procurement and sourcing — practical ideas from the categories we source across every day.</p>
    </div>
  </div>
</section>
<section class="bg-white">
  <div class="section-inner catalog-bottom">
    <div class="price-tabs" id="blogFilter" style="margin-bottom:44px;">
      {chr(10).join(filter_chips)}
    </div>
    <div class="section-label">Featured</div>
    {featured_block}
    <div class="section-label">Latest Articles</div>
    <div class="post-grid reveal-stag" id="postGrid">
      {chr(10).join(cards)}
    </div>
  </div>
</section>'''

    script = '''<script>
(function(){
  var tabs = document.querySelectorAll('#blogFilter .price-tab');
  var items = document.querySelectorAll('#postGrid .post-card, .featured-post');
  tabs.forEach(function(tab){
    tab.addEventListener('click', function(){
      tabs.forEach(function(t){ t.classList.remove('active'); });
      tab.classList.add('active');
      var cat = tab.getAttribute('data-cat-filter');
      items.forEach(function(item){
        var show = cat === 'all' || item.getAttribute('data-cat') === cat;
        item.style.display = show ? '' : 'none';
      });
    });
  });
})();
</script>'''

    title = "Blog — Kaleido"
    desc = "Notes on corporate gifting, procurement and sourcing from the Kaleido team."
    out = os.path.join(ROOT, "blog.html")
    write(out, page_shell(title, desc, body, extra_script=script))


def build_post_page(post):
    toc_items = []
    body_sections = []
    for heading, html in post["sections"]:
        hid = toc_id(heading)
        toc_items.append(f'<li><a href="#{hid}">{heading}</a></li>')
        body_sections.append(f'<h2 id="{hid}">{heading}</h2>\n{html}')

    others = [p for p in BLOG_POSTS if p["slug"] != post["slug"]][:3]
    related_cards = [render_post_card(p) for p in others]

    body = f'''
<section class="bg-beige" id="top">
  <div class="section-inner catalog-top">
    {breadcrumb([("Home", f"{SITE_BASE}/index.html"), ("Blog", f"{SITE_BASE}/blog.html"), (post['title'], None)])}
    <div class="post-hero-grid">
      <div class="post-hero-body reveal">
        <span class="eyebrow">{post['category']}</span>
        <h1>{post['title']}</h1>
        <p class="post-excerpt">{post['excerpt']}</p>
        <div class="post-dates">{read_time_label(post['read_min'])} &middot; {post['date']}</div>
        <div class="post-author"><span class="author-avatar">{author_initials(post['author'])}</span>{post['author']}</div>
      </div>
      <div class="post-hero-media reveal"><img src="https://picsum.photos/seed/{post['image_seed']}/900/700" alt="{post['title']}" loading="lazy"></div>
    </div>
  </div>
</section>
<section class="bg-white">
  <div class="section-inner catalog-bottom">
    <details class="tldr">
      <summary>Click for the TL;DR</summary>
      <div class="tldr-body">{post['tldr']}</div>
    </details>
    <div class="post-layout">
      <article class="post-body">
        {chr(10).join(body_sections)}
      </article>
      <aside class="post-toc">
        <h6>On this page</h6>
        <ol>{chr(10).join(toc_items)}</ol>
      </aside>
    </div>
    <div class="related-posts">
      <div class="section-label" style="text-align:left;">More from the blog</div>
      <div class="post-grid">
        {chr(10).join(related_cards)}
      </div>
    </div>
    <a href="{SITE_BASE}/index.html#connect" class="prod-cta-banner reveal" style="margin-top:52px;">
      <div>
        <h3>Have a sourcing requirement in mind?</h3>
        <p>Tell us what you need and our team will get back within a working day.</p>
      </div>
      <span class="btn btn-light">Connect With Us →</span>
    </a>
  </div>
</section>'''

    title = f"{post['title']} — Kaleido Blog"
    desc = post["excerpt"]
    out = os.path.join(ROOT, "blog", post["slug"], "index.html")
    write(out, page_shell(title, desc, body))


def main():
    build_blog_index()
    for post in BLOG_POSTS:
        build_post_page(post)
    print(f"Generated blog.html + {len(BLOG_POSTS)} post pages.")


if __name__ == "__main__":
    main()
