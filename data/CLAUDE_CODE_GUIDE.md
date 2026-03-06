# Radiance Overseas — Claude Code Batch Generation Guide

## Your Data Files

| File | Purpose |
|------|---------|
| `radiance_full_hierarchy.json` | Master data — Category → Subcategory → Product → Variants (nested) |
| `radiance_full_hierarchy.csv` | Flat table — one row per variant, all columns |
| `radiance_all_pages.json` | Ordered page list — 464 entries with level/file/metadata |

## Page Counts

| Level | Count | Template | Example |
|-------|-------|----------|---------|
| Static | 5 | `index.html`, `Product.html`, etc. | Already built |
| Category | 11 | `rice.html` | Subcategory tabs + product cards |
| Product | 166 | `rice-basmati-1121.html` | Hero + specs + variant cards |
| Variant | 282 | (to be templated) | Detailed spec sheet for one variant |
| **TOTAL** | **464** | | |

---

## Setup (Run Once)

```bash
# 1. Create project folder
mkdir -p ~/radiance-website
cd ~/radiance-website

# 2. Copy your template files and data
cp /path/to/your/templates/*.html ./templates/
cp /path/to/radiance_full_hierarchy.json ./data/
cp /path/to/radiance_all_pages.json ./data/

# 3. Create output structure
mkdir -p output
```

---

## How to Use with Claude Code

### Strategy: Template + Data-Driven Batch Generation

Your templates are self-contained HTML files (CSS inline, no build system needed).
The approach is: **read JSON → inject data into template patterns → write files.**

### Step 1: Generate Category Pages (11 pages)

Prompt Claude Code:

```
Read ./templates/rice.html as the category page template.
Read ./data/radiance_full_hierarchy.json for product data.

For each category in the JSON, generate a category page that:
- Uses the same HTML structure, CSS, and layout as rice.html
- Replaces the hero section (title, description, badges) for that category
- Creates subcategory sections with product cards
- Each product card links to its product_file
- Updates breadcrumbs, schema.org JSON-LD, meta tags, FAQs
- Saves to ./output/{category_file}

Start with spices.html, then do the remaining 9 categories.
Do NOT regenerate rice.html (already done).
```

### Step 2: Generate Product Pages (166 pages)

Prompt Claude Code:

```
Read ./templates/rice-basmati-1121.html as the product page template.
Read ./data/radiance_full_hierarchy.json for product data.

For each product in the JSON, generate a product page that:
- Uses the same HTML structure as rice-basmati-1121.html
- Replaces: hero (product name, origin, grade, keynote)
- Replaces: spec table (product-specific specs)
- Replaces: variant cards section (link to each variant file)
- Replaces: related products (other products in same subcategory)
- Replaces: breadcrumb, schema.org, meta title/description
- Saves to ./output/{product_file}

Process in batches of 20. Start with Indian Spices whole spices.
Use web_fetch on omshreegroup.com product pages for spec data where needed.
```

### Step 3: Generate Variant Pages (282 pages)

Prompt Claude Code:

```
Create a variant page template based on rice-basmati-1121.html but simplified:
- Hero: variant name, parent product, spec/grade
- Spec table: detailed specifications for this specific variant
- Packaging options
- Back link to parent product page
- Related variants (other variants of same product)
- CTA to contact/quote form

For each variant in radiance_full_hierarchy.json, generate a page.
Save to ./output/{variant_file}

Process in batches of 30.
```

### Step 4: SEO/AI Optimization Pass

```
For all 464 HTML files in ./output/:
1. Validate and fix schema.org JSON-LD (Product, BreadcrumbList, FAQPage)
2. Ensure unique meta title (≤60 chars) and description (≤155 chars)
3. Ensure canonical URLs are correct
4. Add hreflang if needed
5. Verify all internal links resolve to actual files
6. Generate sitemap.xml from radiance_all_pages.json
7. Generate robots.txt
```

### Step 5: Competitor Content Research

```
For each product, fetch the corresponding page from omshreegroup.com
to get real spec data (moisture %, broken %, oil content, etc.)
and use that to populate the spec tables.

Use the omshree_hierarchy.json mapping to find corresponding URLs.
Don't copy content — just extract factual specs and rewrite descriptions.
```

---

## Token-Saving Tips

1. **Process in batches** — Do 15-20 pages per prompt, not all at once
2. **Use Sonnet** — Claude Code defaults to Sonnet, which is cheaper and fast
3. **Only escalate to Opus** for complex SEO strategy, content differentiation
4. **Share templates once** — Reference the template by file path, don't paste HTML
5. **Use the JSON** — Let Claude Code read the JSON, don't describe products manually
6. **Script repetitive work** — Ask Claude Code to write a Python/Node script for
   batch generation rather than generating each file individually
7. **Verify in batches** — Spot-check 3-4 files per batch instead of reviewing all

## Recommended Batch Order

| Batch | Pages | Priority |
|-------|-------|----------|
| 1 | 11 category pages | High — these are index/landing pages |
| 2 | 30 spice products | High — most products, most variants |
| 3 | 13 rice products | High — hero category |
| 4 | 12 oil seed products | High — hero category |
| 5 | 13 pulse products | High — hero category |
| 6 | 10 coffee products | Medium |
| 7 | 11 cereal products | Medium |
| 8 | 9 dry fruit products | Medium |
| 9 | 13 dehydrated products | Medium |
| 10 | 21 herb products | Medium |
| 11 | 21 food chemical products | Lower |
| 12 | 13 animal feed products | Lower |
| 13-18 | 282 variant pages (in batches of 50) | Do after products |
| 19 | SEO audit + sitemap | Final pass |

## Sample Claude Code Prompt (Copy-Paste Ready)

```
I'm building a 464-page HTML website for Radiance Overseas (agro exporter).

Files in this project:
- ./templates/rice.html — category page template
- ./templates/rice-basmati-1121.html — product page template  
- ./data/radiance_full_hierarchy.json — all products & variants
- ./data/radiance_all_pages.json — master page list

Task: Generate the 11 category pages.

Read the rice.html template to understand the exact HTML structure,
CSS classes, and layout patterns. Then for each category in the JSON,
create a page following the same pattern but with that category's data.

Write a Python script that reads the JSON and generates all 11 files
to ./output/. Use the template's HTML structure — don't simplify it.
```
