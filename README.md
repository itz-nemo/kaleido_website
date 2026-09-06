# Kaleido — Corporate Gifting Website

Domain: kaleido.com
Corporate gifting platform showcasing services and a large, varied product catalog across multiple domains/categories, with SEO-driven content and a planned AI gift-recommendation layer.

## 1. Requirements

### Functional
- **Product catalog**: Large number of products across varied categories/domains (e.g. apparel, tech, hampers, etc.). Needs category/domain browsing, filtering, search, and individual product detail pages.
- **Services pages**: Present corporate gifting services (bulk orders, custom branding, curated hampers, etc.).
- **Blog**: Content listing for SEO — articles that drive organic traffic (e.g. "gifting guides", "corporate gifting trends").
- **Ordering flow**: Not finalized yet — likely inquiry/quote-based to start (browse → add to an inquiry list → submit request → sales follow-up), with the data model kept flexible enough to add a direct checkout later if needed.
- **Content management**: Not finalized yet — architecture should support a CMS-backed workflow so non-technical staff can eventually manage products/blog without a developer, even if the first version is code/git-managed.
- **Future — AI gift recommendation**: Users should be able to ask an AI assistant for gift recommendations (e.g. "suggest gifts for a client under $50 for a tech startup") and get results pulled from the live product database.

### Non-functional
- **SEO**: Product and blog pages must be crawlable and fast — server-rendered or statically generated, not client-only rendering.
- **Scalability of catalog**: Data model must comfortably handle many products across many categories with attributes/variants (size, branding options, price tiers).
- **Frontend/backend separation**: Clean API boundary so the same product data can later feed an AI layer (recommendation engine, chat assistant) without re-architecting.
- **Performance**: Image-heavy product pages need optimized image delivery.

### Open decisions (to revisit as the project develops)
- Direct checkout vs. inquiry/quote flow vs. both.
- Headless CMS vs. custom-built admin dashboard for non-technical content editing.

## 2. Recommended Tech Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend/full-stack framework | **Next.js (React, App Router)** | SSR/SSG/ISR out of the box → strong SEO for product & blog pages; file-based routing scales well for many product/category pages; built-in image optimization for a product-heavy catalog; API routes/server actions double as a lightweight backend; largest ecosystem for e-commerce and AI SDKs when we get there. |
| Database & backend services | **Supabase (Postgres)** | Relational model fits a product catalog with categories/variants/pricing well; includes auth, file storage (product images), and the **pgvector** extension — which becomes the storage for product embeddings when we build the AI recommendation feature, avoiding a second database migration later. |
| Content editing (blog + marketing) | **Headless CMS (e.g. Sanity)** — *or* a custom-built admin panel in Next.js if we'd rather keep everything in one codebase | Sanity: fastest to give non-technical staff a friendly editing UI. Custom admin: more upfront dev work, but avoids a second system and keeps content directly in Supabase alongside products. Decide once the content-ownership question above is settled. |
| Future AI layer | **Claude API** for the conversational assistant, using Retrieval-Augmented Generation over product embeddings in pgvector | Keeps recommendations grounded in the real, live product catalog rather than the model guessing. |
| Hosting | **Vercel** (frontend) + **Supabase Cloud** (data) | Native Next.js integration, preview deployments per PR, minimal ops overhead. |

### Why this stack supports the AI roadmap
Because products live in Postgres with pgvector available from day one, adding the AI recommendation feature later is additive (generate embeddings for existing products, build a retrieval + chat endpoint) rather than a rewrite of the data layer.

## 3. Next Steps
1. Decide ordering flow (inquiry vs. checkout vs. both) and content-management approach (CMS vs. custom admin).
2. Define the product data model (categories, attributes, variants, pricing, images).
3. Scaffold the Next.js project and Supabase schema.
4. Build product listing/detail pages and blog listing for SEO.
5. Revisit AI recommendation feature once the catalog and content pipeline are stable.
