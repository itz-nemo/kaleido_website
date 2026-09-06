# Kaleido — Progress Snapshot

Kept up to date at the end of every session so a new session can start with minimal context. This is a living summary — overwritten, not appended to.

## Current focus
Building out the **Products** side of the site only, until it's fully developed. Homepage/other sections are stable and out of scope for now.

## Live site
https://itz-nemo.github.io/kaleido_website/ — plain static HTML/CSS/JS, hosted free on GitHub Pages (public repo). No build step; `.nojekyll` is present so GitHub Pages serves files as-is.

## What exists today
- `index.html` — homepage (white + LinkedIn-blue theme).
- `products.html` — top-level catalog page: 9 categories shown as a corpattire-style icon grid (`.corp-grid`), each linking to its category page.
- `products/<category-slug>/index.html` — one per category (9 total): subcategory grid.
- `products/<category-slug>/<subcategory-slug>/index.html` — one per subcategory (51 total): leaf-node grid + a "Search what's in your mind" search bar.
- `products/<category-slug>/<subcategory-slug>/<leaf-slug>/index.html` — one per leaf node (212 total): price-tier filter tabs (Under ₹500/₹1,000/₹2,500/₹5,000, client-side JS filter) + a 4-item product grid.
- `products/<category-slug>/<subcategory-slug>/<leaf-slug>/product-details.html` — one generic template per leaf, reads `?id=&slug=` from the URL and fetches `data.json` in the same folder to render a Snappy-style PDP (image gallery of 4 + swappable thumbnails, price, description, specs, Enquire Now CTA).
- `products/.../<leaf-slug>/data.json` — 4 placeholder products per leaf (name, price, 4 picsum images, description, specs: Category/Material/Customization/MOQ/Lead Time). All data is dummy/placeholder — no real backend yet.
- Nav mega-menu on "Products" (desktop hover only; mobile keeps a plain link) — two columns: **Shop by Occasion** (8 items, all currently point to `products.html` — no dedicated occasion pages yet) and **Shop by Category** (9 real category links) + an "Explore All Products" CTA.
- `assets/img/brand-icon.png` — the logo was extracted out of a 109KB inline base64 blob (was duplicated in every page) into a real file; all pages reference it via `/kaleido_website/assets/img/brand-icon.png`.
- `scripts/generate_products.py` — the generator for the entire `/products/` tree. **This is the source of truth for the taxonomy.** To add/edit/remove categories, subcategories or leaf items, edit the `TAXONOMY` dict at the top of this script and re-run `python3 scripts/generate_products.py` — it wipes and rebuilds `products/<category>/` for every category on each run.

## Key conventions (don't relitigate these)
- **URL prefix**: every internal link on generated pages uses the absolute path prefix `/kaleido_website/...` (not relative `../../..`), since the site is a GitHub Pages *project* site living at that subpath. This was a deliberate choice to avoid relative-path bugs across 4 levels of nesting.
- **Slugs**: category slugs are hand-picked in `TAXONOMY` (e.g. `stationary-and-office-supplies` — intentionally matches the user's own URL example spelling, not the correct "stationery"; `gifting` for Corporate Gifting; `it-and-electronics`). Subcategory and leaf slugs are auto-generated via `slugify()` (lowercases, `&`→`and`, non-alphanumerics→`-`).
- **Design system reuse**: new components added to `assets/css/styles.css` (search near the bottom, "SECTION 11" onward): `.has-mega`/`.mega-menu` (nav dropdown), `.corp-grid`/`.corp-card` (corpattire-style small-icon category grid, used at every taxonomy level), `.search-bar`, `.breadcrumb`, `.price-tabs`, `.item-grid`/`.item-card` (leaf-page product grid), `.pdp-*` (product detail page).
- **Reveal-on-scroll gotcha**: `main.js`'s IntersectionObserver only scans `.reveal`/`.reveal-stag` elements present at page load. Any content injected later via JS (like the PDP gallery) must NOT use those classes, or it stays permanently invisible — already hit and fixed once in `product-details.html`'s generator function.
- **Strategic Sourcing** is flagged `is_service=True` in the taxonomy — it's framed as a procurement capability rather than a fixed catalogue (different eyebrow/intro copy), but reuses the same page template as the other 8 categories for consistency.
- Verification method: no persistent browser available by default — use `python3 -m http.server` from `/Users/nemo/Desktop` (one level above the repo) so root-relative `/kaleido_website/...` paths resolve exactly like production, then `curl -o /dev/null -w "%{http_code}"` per file. Chrome browser tools (`mcp__claude-in-chrome__*`) were available and used for real visual verification in the session that built this — use them again if available.

## Known gaps / not done yet
- Occasion mega-menu links (Employee Onboarding, Work Anniversaries, etc.) all point to `products.html` — no dedicated occasion-filtered pages exist.
- All product data is placeholder/random — no real product catalog, pricing, or images yet.
- No search functionality actually wired up (the search bar on subcategory pages is UI-only, `onsubmit="return false"`).
- No contact/inquiry form yet — "Enquire Now" and "Connect With Us" CTAs still just deep-link to `index.html#connect`, which itself has no working form.
- Mobile nav does not expose the mega-menu categories (by design, kept simple) — mobile users can still reach `products.html` via the flat "Products" link.

## Next candidates (not yet started, not yet requested)
- Wire an actual contact/inquiry form.
- Real product data/catalog once available (would replace `data.json` placeholders).
- Decide CMS vs. custom admin, ordering flow (inquiry vs. checkout) — still open per `README.md`.
