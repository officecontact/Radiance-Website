# Radiance Overseas — Public HTML Site

## Project Overview
Static HTML website for **Radiance Overseas** (radianceoverseas.com), an Indian certified organic agro-product export company. The site is a large B2B product catalog with hundreds of product pages across categories like spices, rice, coffee, pulses, oil seeds, herbs, dry fruits, dehydrated products, cereals/flour, food chemicals, and animal feed.

## Tech Stack
- **Pure static HTML** — no build step, no framework
- **CSS**: Single master stylesheet `assets/css/radiance.css` (CSS custom properties / design tokens in `:root`)
- **JS**: Single master script `assets/js/radiance.js` (vanilla JS, IIFE pattern)
- **Vendor assets**: `webassets/` — Bootstrap CSS, jQuery, Owl Carousel, Three.js (3D globe), Font Awesome (via CDN)
- **Fonts**: Playfair Display (headings), Open Sans (body), Poppins (UI) — loaded via Google Fonts
- **Blog API**: `api/blog-save.php` — PHP endpoint for blog post saving
- **Blog data**: `blogs/posts.json`

## Directory Structure
```
├── index.html              # Homepage
├── Product.html            # Main product catalog page
├── Certification.html      # Certifications page
├── Contact.html            # Contact page
├── blog.html               # Blog listing
├── blog-post.html          # Blog post template
├── sitemap.xml             # XML sitemap
├── robots.txt              # Robots file
├── assets/
│   ├── css/radiance.css    # Master stylesheet
│   └── js/radiance.js      # Master JavaScript
├── webassets/              # Vendor/third-party assets (CSS, JS, images)
├── uploads/images/         # Uploaded images (logos, etc.)
├── api/blog-save.php       # Blog save endpoint
├── blogs/posts.json        # Blog post data
├── data/
│   ├── radiance_all_pages.json       # Page registry (level: static/category/subcategory/product/grade)
│   └── radiance_full_hierarchy.json  # Full product hierarchy tree
├── [category].html         # Category pages (e.g., spices.html, rice.html)
├── [category]-[sub].html   # Subcategory pages (e.g., spices-whole-spices.html)
└── [category]-...-[product].html  # Product/grade pages (deeply nested naming)
```

## Page Hierarchy
Pages follow a 5-level hierarchy defined in `data/radiance_all_pages.json`:
1. **static** — index, Product, Certification, Contact, blog
2. **category** — top-level product categories (spices, rice, coffee, etc.)
3. **subcategory** — product groupings within categories
4. **product** — individual product pages
5. **grade** — specific grades/variants of products

File names use hyphenated paths reflecting the hierarchy (e.g., `spices-whole-spices-cumin-seeds-europe.html`).

## Design Tokens (CSS Variables)
Key colors: `--green: #36d022`, `--gold: #c8a84b`, `--cream: #f7f4ef`, `--green-deep: #1a4731`

## SEO
- Each page has full meta tags: title, description, keywords, Open Graph, Twitter Card
- Canonical URLs point to `https://www.radianceoverseas.com/`
- Structured data (JSON-LD) for Organization schema on homepage
- Sitemap at `sitemap.xml`

## Conventions
- All HTML pages are self-contained (no server-side includes in production)
- Product pages share a consistent structure: nav, hero, product details, specs table, FAQ, CTA, footer
- WhatsApp floating button on all pages
- Mobile-responsive with hamburger nav
