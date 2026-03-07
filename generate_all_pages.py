#!/usr/bin/env python3
"""
generate_all_pages.py
Generates ALL HTML pages for the Radiance Overseas website.
Run from repo root: python3 generate_all_pages.py
"""

import json
import os
import re

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
JSON_PATH  = os.path.join(BASE_DIR, 'radiance_full_hierarchy.json')
RICE_TPL   = os.path.join(BASE_DIR, 'rice.html')
PROD_TPL   = os.path.join(BASE_DIR, 'rice-basmati-1121.html')

SKIP_FILES = {
    'index.html', 'Contact.html', 'Certification.html', 'blog.html',
    'blog-admin.html', 'Product.html', 'rice.html', 'rice-basmati.html',
    'rice-basmati-1121.html', 'rice-basmati-1121-sella.html',
}

IMG_URL = 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600&q=80'

# ── Constants ─────────────────────────────────────────────────────────────────
ORG_SCHEMA = '''<script type="application/ld+json">
  {"@context":"https://schema.org","@type":"Organization","name":"Radiance Overseas",
  "url":"https://www.radianceoverseas.com/","logo":"https://www.radianceoverseas.com/uploads/images/Radiancelogo.png",
  "address":{"@type":"PostalAddress","streetAddress":"60, Silver Oaks, Annapurna Road","addressLocality":"Indore","addressRegion":"Madhya Pradesh","postalCode":"452009","addressCountry":"IN"},
  "contactPoint":{"@type":"ContactPoint","telephone":"+919584949494","email":"info@radianceoverseas.com","contactType":"customer service"}}
  </script>'''

CAT_META = {
    "Indian Rice":        {"emoji":"🌾","file":"rice.html","desc":"APEDA Registered · Basmati & Non-Basmati","badges":["APEDA Registered","EU & India Organic","MOQ 25 MT","NABL Tested"],"moq":"25 MT","certs":["APEDA RCMC","EU Organic","India Organic","GI Tagged"],"img_kw":"rice"},
    "Indian Spices":      {"emoji":"🌶","file":"spices.html","desc":"Spices Board RCMC · Whole & Powdered","badges":["Spices Board RCMC","EU & India Organic","MOQ 1 MT","NABL Tested"],"moq":"1 MT","certs":["Spices Board RCMC","EU Organic","India Organic","AGMARK"],"img_kw":"spices"},
    "Oil Seeds":          {"emoji":"🌻","file":"oil-seeds.html","desc":"IOPEPC Registered · Sesame · Groundnut","badges":["IOPEPC Registered","EU Organic","MOQ 5 MT","NABL Tested"],"moq":"5 MT","certs":["IOPEPC","EU Organic","FSSAI","NABL Tested"],"img_kw":"oilseed"},
    "Pulses":             {"emoji":"🫘","file":"pulses.html","desc":"NABL Tested · Whole & Split Dal","badges":["FSSAI Approved","EU Organic","MOQ 10 MT","NABL Tested"],"moq":"10 MT","certs":["FSSAI","EU Organic","India Organic","NABL"],"img_kw":"pulses"},
    "Coffee":             {"emoji":"☕","file":"coffee.html","desc":"Coffee Board RCMC · Arabica & Robusta","badges":["Coffee Board RCMC","EU Organic","MOQ 1 MT","GCP Certified"],"moq":"1 MT","certs":["Coffee Board RCMC","EU Organic","Rainforest Alliance","UTZ"],"img_kw":"coffee"},
    "Cereals & Flour":    {"emoji":"🌾","file":"cereals.html","desc":"Millets · Wheat · Corn · Sorghum","badges":["FSSAI Approved","EU Organic","MOQ 5 MT","NABL Tested"],"moq":"5 MT","certs":["FSSAI","EU Organic","India Organic","NABL"],"img_kw":"cereal"},
    "Dry Fruits & Nuts":  {"emoji":"🫐","file":"dry-fruits.html","desc":"Raisins · Cashews · Walnuts · Almonds","badges":["FSSAI Approved","EU Organic","MOQ 1 MT","NABL Tested"],"moq":"1 MT","certs":["FSSAI","EU Organic","ISO 22000","NABL"],"img_kw":"dryfruits"},
    "Dehydrated Products":{"emoji":"🧅","file":"dehydrated.html","desc":"Flakes & Powders · Onion · Garlic · Ginger","badges":["EU Organic","FSSAI Approved","MOQ 1 MT","NABL Tested"],"moq":"1 MT","certs":["EU Organic","FSSAI","India Organic","NABL"],"img_kw":"dehydrated"},
    "Herbs & Crude Drugs":{"emoji":"🌿","file":"herbs.html","desc":"Leaves · Fruits · Seeds · Roots","badges":["WHO-GMP","EU Organic","MOQ 500 KG","NABL Tested"],"moq":"500 KG","certs":["WHO-GMP","EU Organic","India Organic","NABL"],"img_kw":"herbs"},
    "Food Chemicals":     {"emoji":"⚗️","file":"food-chemicals.html","desc":"FSSAI · Sugars · Additives · Natural Colours","badges":["FSSAI Approved","EU E-numbers","MOQ 500 KG","NABL Tested"],"moq":"500 KG","certs":["FSSAI","EU Approved","ISO 22000","NABL"],"img_kw":"foodchem"},
    "Animal Feed":        {"emoji":"🐄","file":"animal-feed.html","desc":"GMP+ Certified · Corn · Millets · Protein Meals","badges":["GMP+ Certified","FSSAI Approved","MOQ 10 MT","NABL Tested"],"moq":"10 MT","certs":["GMP+","FSSAI","EU Organic","NABL"],"img_kw":"animalfeed"},
}

# Cat chips nav list (emoji, label, file)
CAT_CHIPS = [
    ("🌾", "Indian Rice",       "rice.html"),
    ("🌶", "Indian Spices",     "spices.html"),
    ("🌻", "Oil Seeds",         "oil-seeds.html"),
    ("🫘", "Pulses",            "pulses.html"),
    ("☕", "Coffee",            "coffee.html"),
    ("🌽", "Cereals & Flour",   "cereals.html"),
    ("🍇", "Dry Fruits",        "dry-fruits.html"),
    ("🧅", "Dehydrated",        "dehydrated.html"),
    ("🌿", "Herbs",             "herbs.html"),
    ("⚗️", "Food Chemicals",    "food-chemicals.html"),
    ("🐄", "Animal Feed",       "animal-feed.html"),
]

# ── Extract common sections from templates ────────────────────────────────────

def extract_common_wrapper(rice_content):
    """Extract from <body> up to and including }());\n</script>"""
    body_start = rice_content.find('<body>')
    marker = '}());\n</script>'
    marker_end = rice_content.find(marker)
    if marker_end == -1:
        raise ValueError("Could not find nav_js end marker in rice.html")
    return rice_content[body_start: marker_end + len(marker)]


def extract_common_footer(rice_content):
    """Extract from \n<footer role="contentinfo"> to end of file"""
    marker = '\n<footer role="contentinfo">'
    idx = rice_content.find(marker)
    if idx == -1:
        raise ValueError("Could not find footer in rice.html")
    return rice_content[idx:]


def extract_css_block(content, after_script_end=True):
    """
    Extract the <style> block that immediately follows the nav_js </script>.
    Returns the raw CSS text (between <style> and </style>).
    """
    nav_end_marker = '}());\n</script>'
    nav_end_idx = content.find(nav_end_marker)
    if nav_end_idx == -1:
        raise ValueError("Could not find nav_js end marker")
    after_nav = content[nav_end_idx + len(nav_end_marker):]
    style_start = after_nav.find('<style>')
    style_end = after_nav.find('</style>', style_start)
    if style_start == -1 or style_end == -1:
        raise ValueError("Could not find <style> block after nav_js")
    return after_nav[style_start: style_end + len('</style>')]

# ── Head generation ───────────────────────────────────────────────────────────

def gen_head(title, desc, keywords, canonical, schemas_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="author" content="Radiance Overseas">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://www.radianceoverseas.com/{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.radianceoverseas.com/{canonical}">
  <meta property="og:image" content="https://www.radianceoverseas.com/uploads/images/Radiancelogo.png">
  <meta property="og:site_name" content="Radiance Overseas">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <link rel="shortcut icon" href="webassets/images/favicon.png" type="image/x-icon">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=Open+Sans:wght@300;400;600;700&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="assets/css/radiance.css">
  {ORG_SCHEMA}
  {schemas_html}
<noscript><style>.anim-fade-up{{opacity:1!important;transform:none!important;}}</style></noscript>
<style>.anim-fade-up{{animation:forceShow 0s 1.5s forwards}}@keyframes forceShow{{to{{opacity:1;transform:none}}}}.faq-item.open .faq-a{{display:block!important;}}
    .faq-item.open .faq-icon{{transform:rotate(45deg);}}
    .faq-q{{width:100%;background:none;border:none;text-align:left;}}
  </style>
</head>"""


# ── Helper: cat chips nav ─────────────────────────────────────────────────────

def gen_cat_chips_nav(active_file):
    chips_html = ''
    for emoji, label, file in CAT_CHIPS:
        active_class = ' is-active' if file == active_file else ''
        chips_html += f'<a href="{file}" class="cat-chip{active_class}">{emoji} {label}</a>\n'
    return f'''<div class="cat-chips-nav">
  <div class="container"><div class="cat-chips-nav-inner"><strong style="font-family:'Poppins',sans-serif;font-size:10.5px;color:#888;text-transform:uppercase;letter-spacing:1px;flex-shrink:0;margin-right:4px;">All:</strong>
{chips_html}</div></div>
</div>'''


# ── Helper: slug ───────────────────────────────────────────────────────────────

def to_id(name):
    """Convert subcategory name to HTML id"""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


# ── FAQ generators ─────────────────────────────────────────────────────────────

def gen_cat_faqs(cat_name, cat_meta):
    moq = cat_meta.get('moq', '25 MT')
    certs = ', '.join(cat_meta.get('certs', []))
    faqs = [
        (f"What {cat_name} products does Radiance Overseas export?",
         f"Radiance Overseas exports a comprehensive range of {cat_name} products sourced directly from certified farms and processing units across India. All products are FSSAI compliant and available in custom grades and packaging."),
        (f"What certifications does your {cat_name} hold?",
         f"Our {cat_name} products carry the following certifications: {certs}. These ensure compliance with international food safety and quality standards."),
        (f"What is the MOQ for {cat_name} export?",
         f"Minimum Order Quantity (MOQ) for {cat_name} starts at {moq}. Trial shipments in smaller quantities are available at a slight premium for new buyers."),
        (f"What packaging is available for {cat_name}?",
         f"Standard packaging includes 25 kg and 50 kg PP woven bags, 1–5 kg consumer packs, and bulk container shipments (20'/40' FCL). Custom private-label packaging is also available."),
        (f"What documents are provided for {cat_name} exports?",
         f"We provide Phytosanitary Certificate, Certificate of Analysis (COA), Certificate of Origin (CoO), FSSAI compliance document, and any market-specific documentation required by the importing country."),
    ]
    items = ''
    for q, a in faqs:
        items += f'''  <div class="faq-item">
    <button class="faq-q" onclick="faqToggle(this)">{q}<span class="faq-icon">+</span></button>
    <div class="faq-a"><p>{a}</p></div>
  </div>
'''
    return f'''<section class="faq-section">
  <div class="container">
    <h2>Frequently Asked Questions — {cat_name}</h2>
    <div class="faq-list">
{items}    </div>
  </div>
</section>'''


def gen_prod_faqs(prod_name, origin, grade):
    faqs = [
        (f"What is {prod_name}?",
         f"{prod_name} is a premium export-quality product sourced from {origin}. Grade: {grade}. Radiance Overseas ensures strict quality control at every stage from procurement to shipment."),
        (f"What is the MOQ for {prod_name}?",
         f"The standard MOQ for {prod_name} is 25 MT (one 20-foot container). Trial orders of 5–10 MT are available for new buyers at a slight premium."),
        (f"What certifications apply to {prod_name}?",
         f"{prod_name} from Radiance Overseas is tested by NABL-accredited laboratories. We hold APEDA RCMC, EU Organic, and India Organic certifications applicable to this product."),
        (f"What packaging options are available for {prod_name}?",
         f"Standard packaging: 25 kg and 50 kg PP woven bags with inner HDPE liner. Consumer packs (1 kg, 2 kg, 5 kg) and bulk container loads are also available. Custom private-label branding upon request."),
        (f"What documents are provided with {prod_name} shipments?",
         f"We provide Phytosanitary Certificate, Certificate of Analysis, Certificate of Origin, FSSAI compliance document, and all customs/shipping documents required for your destination country."),
    ]
    items = ''
    for q, a in faqs:
        items += f'''  <div class="faq-item">
    <button class="faq-q" onclick="faqToggle(this)">{q}<span class="faq-icon">+</span></button>
    <div class="faq-a"><p>{a}</p></div>
  </div>
'''
    return f'''<section style="padding:48px 0;background:#f7fbf7;">
  <div class="container">
    <h2 style="font-family:'Playfair Display',serif;font-size:clamp(20px,2.5vw,28px);color:#1a2e1a;margin-bottom:24px;">Frequently Asked Questions</h2>
    <div class="faq-list">
{items}    </div>
  </div>
</section>'''


# ── CTA band ───────────────────────────────────────────────────────────────────

def gen_cta_band():
    return '''<section class="cta-band">
  <div class="container">
    <h2>Ready to Source from India?</h2>
    <p>Get competitive FOB/CIF pricing, product samples, and full documentation within 24 hours.</p>
    <div class="cta-btns">
      <a href="Contact.html#form" class="btn" style="background:#36d022;color:#fff;padding:14px 32px;border-radius:7px;font-family:Poppins,sans-serif;font-weight:700;font-size:14px;text-decoration:none;display:inline-block;">&#128203; Request a Quote</a>
      <a href="Product.html" class="btn" style="background:rgba(255,255,255,.12);border:2px solid rgba(255,255,255,.35);color:#fff;padding:12px 28px;border-radius:7px;font-family:Poppins,sans-serif;font-weight:700;font-size:14px;text-decoration:none;display:inline-block;">Browse All Products</a>
    </div>
  </div>
</section>'''


def gen_sp_cta():
    return '''<section class="sp-cta">
  <div class="container">
    <h2>Get a Quote for This Product</h2>
    <p>Competitive FOB/CIF pricing, product samples, and full documentation within 24 hours.</p>
    <div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:12px;">
      <a href="Contact.html#form" class="btn-gold">&#128203; Request a Quote</a>
      <a href="Product.html" class="btn-outline-w">Browse All Products</a>
    </div>
  </div>
</section>'''


# ── Category page builder ──────────────────────────────────────────────────────

def build_category_page(cat_name, cat_data, cat_meta, COMMON_WRAPPER, COMMON_FOOTER, CAT_CSS):
    file = cat_meta['file']
    emoji = cat_meta['emoji']
    desc_short = cat_meta['desc']
    badges = cat_meta['badges']
    moq = cat_meta['moq']
    certs = cat_meta['certs']

    subcategories = cat_data.get('subcategories', {})
    all_products = []
    for sc_name, sc_data in subcategories.items():
        all_products.extend(sc_data.get('products', {}).keys())

    prod_count = len(all_products)
    subcat_count = len(subcategories)

    title = f"{cat_name} Export — Bulk {cat_name} from India | Radiance Overseas"
    desc = f"Buy bulk {cat_name} from India. {desc_short}. {prod_count} varieties. MOQ {moq}. 30+ countries. Radiance Overseas."
    keywords = f"{cat_name.lower()} export india,bulk {cat_name.lower()} supplier,{cat_name.lower()} exporter india,radiance overseas"
    canonical = file

    # Schema
    breadcrumb_schema = f'{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://www.radianceoverseas.com/"}},{{"@type":"ListItem","position":2,"name":"Products","item":"https://www.radianceoverseas.com/Product.html"}},{{"@type":"ListItem","position":3,"name":"{cat_name}","item":"https://www.radianceoverseas.com/{file}"}}]}}'
    schemas_html = f'<script type="application/ld+json">{breadcrumb_schema}</script>'

    head = gen_head(title, desc, keywords, canonical, schemas_html)

    # badges html
    badge_icons = ["fas fa-certificate", "fas fa-leaf", "fas fa-ship", "fas fa-flask"]
    badges_html = ''.join(
        f'<span class="pg-hero-badge"><i class="{badge_icons[i % len(badge_icons)]}"></i> {b}</span>'
        for i, b in enumerate(badges)
    )

    # Hero section
    hero = f'''<section class="pg-hero" style="--hero-bg:url('{IMG_URL}')">
  <div class="container">
    <nav class="pg-breadcrumb" aria-label="Breadcrumb">
      <a href="index.html">Home</a><span>›</span>
      <a href="Product.html">Products</a><span>›</span>
      <span>{cat_name}</span>
    </nav>
    <div class="pg-hero-body">
      <div class="pg-hero-eyebrow">{emoji} Export Category &nbsp;·&nbsp; {prod_count} Products &nbsp;·&nbsp; {desc_short}</div>
      <h1>Premium <em>{cat_name}</em> — Export from India</h1>
      <p class="pg-hero-desc">India's finest {cat_name.lower()} sourced directly from certified farms and processing units. {desc_short}. Available in {subcat_count} categories, {prod_count} product varieties, exported to 30+ countries.</p>
      <div class="pg-hero-badges">
        {badges_html}
      </div>
    </div>
  </div>
  <div class="pg-hero-wave"></div>
</section>'''

    # Stats strip
    stats = f'''<div class="stats-strip">
  <div class="stat-item"><div class="stat-num">{prod_count}</div><div class="stat-lbl">Varieties</div></div><div class="stat-item"><div class="stat-num">{subcat_count}</div><div class="stat-lbl">Sub-types</div></div><div class="stat-item"><div class="stat-num">{moq}</div><div class="stat-lbl">Min. Order</div></div><div class="stat-item"><div class="stat-num">30+</div><div class="stat-lbl">Export Countries</div></div><div class="stat-item"><div class="stat-num">15 Yrs</div><div class="stat-lbl">Export Experience</div></div>
</div>'''

    # Cat chips nav
    cat_chips_nav = gen_cat_chips_nav(file)

    # Subcat sticky nav
    subcat_nav_links = ''
    for sc_name, sc_data in subcategories.items():
        sc_id = to_id(sc_name)
        sc_prod_count = len(sc_data.get('products', {}))
        active_cls = ' is-active' if sc_name == list(subcategories.keys())[0] else ''
        subcat_nav_links += f'<a href="#{sc_id}" class="subcat-nav-link{active_cls}">{sc_name} <span class="snl-count">{sc_prod_count}</span></a>'

    subcat_sticky_nav = f'<nav class="subcat-sticky-nav" aria-label="Sub-category navigation"><div class="container"><div class="subcat-sticky-inner">{subcat_nav_links}</div></div></nav>'

    # Intro strip
    intro = f'''<div class="intro-strip">
  <div class="container">
    <h2>About Radiance Overseas {cat_name} Export</h2>
    <p>Radiance Overseas is a certified exporter of {cat_name.lower()} from India. We source directly from farmers and processing units, ensuring consistent quality, competitive pricing, and reliable supply. All products are tested by NABL-accredited laboratories and come with full export documentation.</p>
  </div>
</div>'''

    # Trust strip
    cert_items = ''.join(f'<div class="trust-item"><i class="fas fa-certificate"></i> {c}</div>' for c in certs)
    trust = f'''<div class="trust-strip">
  <div class="container">
    <div class="trust-items">
      {cert_items}
      <div class="trust-item"><i class="fas fa-ship"></i> {moq} MOQ</div>
      <div class="trust-item"><i class="fas fa-file-alt"></i> Phyto / COA / CoO Provided</div>
    </div>
  </div>
</div>'''

    # Subcategory sections
    subcat_sections = ''
    for sc_name, sc_data in subcategories.items():
        sc_id = to_id(sc_name)
        products = sc_data.get('products', {})

        # Cert badges for subcat header
        cert_spans = ''.join(f'<span class="subcat-cert">{c}</span>' for c in certs[:4])

        # Product cards
        cards_html = ''
        for prod_name, prod_data in products.items():
            prod_file = prod_data.get('file', '#')
            prod_grade = prod_data.get('grade', '')
            prod_origin = prod_data.get('origin', 'India')
            prod_note = prod_data.get('note', '')
            variant_count = len(prod_data.get('variants', []))
            cards_html += f'''<a href="{prod_file}" class="spice-prod-card" itemscope itemtype="https://schema.org/Product">
  <meta itemprop="name" content="{prod_name}">
  <meta itemprop="description" content="{prod_name} — {prod_grade}. {prod_note}. Export from India by Radiance Overseas.">
  <div class="spc__img-wrap">
    <img src="{IMG_URL}" alt="{prod_name} bulk export India Radiance Overseas"
         class="spc__img" loading="lazy" onerror="this.parentNode.style.background='#edf7ed';this.style.display='none'">
    <span class="spc__origin">{prod_origin}</span>
  </div>
  <div class="spc__body">
    <div class="spc__name">{prod_name}</div>
    <div class="spc__grade">{prod_grade}</div>
    <div class="spc__note">{prod_note}{f" · {variant_count} variants" if variant_count else ""}</div>
    <div class="spc__cta">View Details <span class="spc__arrow">›</span></div>
  </div>
</a>
'''

        subcat_sections += f'''<section class="subcat-section" id="{sc_id}" aria-label="{sc_name}">
  <div class="subcat-header">
    <div class="subcat-header__left">
      <h2 class="subcat-title">{sc_name}</h2>
      <p class="subcat-tagline">Premium quality {sc_name.lower()} sourced from the finest growing regions of India. Available in multiple grades and processing options.</p>
    </div>
    <div class="subcat-header__right">{cert_spans}</div>
  </div>
  <div class="subcat-intro-box">
    <div class="subcat-intro-img"><img src="{IMG_URL}" alt="{sc_name}" loading="lazy" onerror="this.style.display='none'"></div>
    <p>Radiance Overseas exports {sc_name.lower()} in {len(products)} variety/varieties. All products are sourced directly from certified farms and processing units, tested at NABL-accredited labs, and shipped with full documentation.</p>
  </div>
  <div class="spc-grid">
{cards_html}  </div>
  <div class="subcat-actions">
    <a href="Contact.html#form" class="btn-enquire-sub"><i class="fas fa-file-alt"></i> Enquire About {sc_name}</a>
  </div>
</section>
<hr class="subcat-divider">
'''

    # Products main
    products_main = f'''<div class="products-main" itemscope itemtype="https://schema.org/ItemList">
  <meta itemprop="name" content="{cat_name} — Radiance Overseas Export Catalog">
  <div class="container">
{subcat_sections}  </div>
</div>'''

    faq_section = gen_cat_faqs(cat_name, cat_meta)
    cta = gen_cta_band()

    return '\n'.join([
        head,
        COMMON_WRAPPER,
        '\n',
        CAT_CSS,
        '\n',
        hero,
        stats,
        cat_chips_nav,
        subcat_sticky_nav,
        intro,
        trust,
        products_main,
        faq_section,
        cta,
        COMMON_FOOTER,
    ])


# ── Product page builder ───────────────────────────────────────────────────────

def build_product_page(prod_name, prod_data, cat_name, cat_file, subcat_name,
                       subcat_products, COMMON_WRAPPER, COMMON_FOOTER, PROD_CSS):
    prod_file = prod_data['file']
    grade = prod_data.get('grade', '')
    origin = prod_data.get('origin', 'India')
    note = prod_data.get('note', '')
    variants = prod_data.get('variants', [])

    title = f"{prod_name} Export — {grade} | {cat_name} | Radiance Overseas"
    desc = f"Buy bulk {prod_name} from India. {grade}. Origin: {origin}. {note}. MOQ 25 MT. Radiance Overseas certified exporter."
    keywords = f"{prod_name.lower()} export india,{prod_name.lower()} bulk supplier,{cat_name.lower()} exporter india"
    canonical = prod_file

    breadcrumb_schema = f'{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://www.radianceoverseas.com/"}},{{"@type":"ListItem","position":2,"name":"Products","item":"https://www.radianceoverseas.com/Product.html"}},{{"@type":"ListItem","position":3,"name":"{cat_name}","item":"https://www.radianceoverseas.com/{cat_file}"}},{{"@type":"ListItem","position":4,"name":"{prod_name}","item":"https://www.radianceoverseas.com/{prod_file}"}}]}}'
    schemas_html = f'<script type="application/ld+json">{breadcrumb_schema}</script>'

    head = gen_head(title, desc, keywords, canonical, schemas_html)

    # Variant toggle bar
    variant_toggle = ''
    if variants:
        variant_links = ''.join(
            f'<a href="{v["file"]}" style="display:inline-flex;align-items:center;padding:6px 14px;border:1.5px solid rgba(255,255,255,.3);border-radius:5px;color:rgba(255,255,255,.8);font-family:Poppins,sans-serif;font-size:12px;font-weight:600;text-decoration:none;background:rgba(255,255,255,.08);margin:4px;">{v["name"]}</a>'
            for v in variants
        )
        variant_toggle = f'''<div style="margin-top:12px;">
  <strong style="color:rgba(255,255,255,.9);font-family:Poppins,sans-serif;font-size:12px;">Variants:</strong>
  <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">{variant_links}</div>
</div>'''

    # Hero
    hero = f'''<section class="sp-hero">
  <div class="sp-hero-bg" style="background-image:url('{IMG_URL}');"></div>
  <div class="sp-hero-overlay"></div>
  <div class="sp-breadcrumb">
    <div class="container">
      <ol><li><a href="index.html">Home</a></li>
        <li><span class="sep">/</span></li>
        <li><a href="Product.html">Products</a></li>
        <li><span class="sep">/</span></li>
        <li><a href="{cat_file}">{cat_name}</a></li>
        <li><span class="sep">/</span></li>
        <li><span class="cur">{prod_name}</span></li></ol>
    </div>
  </div>
  <div class="container">
    <div class="sp-hero-inner">
      <div class="sp-hero-grid">
        <div class="sp-hero-img">
          <img src="{IMG_URL}" alt="{prod_name} Export India" onerror="this.parentNode.style.background='#222';this.style.display='none'">
        </div>
        <div class="sp-hero-content">
          <span class="sp-eyebrow">{cat_name} · {subcat_name} · {len(variants)} Variants</span>
          <h1>{prod_name}</h1>
          <p class="sp-origin"><i class="fas fa-map-marker-alt"></i> Origin: {origin}</p>
          <div class="sp-keynote">{grade}{" — " + note if note else ""}</div>
          {variant_toggle}
          <div class="sp-certs">
            <span class="cert-badge">APEDA</span>
            <span class="cert-badge">EU Organic</span>
            <span class="cert-badge">NABL Tested</span>
          </div>
          <div class="sp-hero-btns">
            <a href="Contact.html#form" class="btn-gold">&#128203; Request a Quote</a>
            <a href="{cat_file}" class="btn-outline-w">&#8592; Back to {cat_name}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>'''

    # Specs section
    spec_rows = f'''<tr><td class="sl">Product</td><td class="sv">{prod_name}</td></tr>
          <tr><td class="sl">Grade / Specification</td><td class="sv">{grade}</td></tr>
          <tr><td class="sl">Origin</td><td class="sv">{origin}</td></tr>
          <tr><td class="sl">Note</td><td class="sv">{note if note else "—"}</td></tr>
          <tr><td class="sl">Variants Available</td><td class="sv">{", ".join(v["name"] for v in variants) if variants else "Single grade"}</td></tr>
          <tr><td class="sl">MOQ</td><td class="sv">25 MT (trial: 5–10 MT)</td></tr>
          <tr><td class="sl">Packaging</td><td class="sv">25 kg PP Bag · 50 kg Jute · Bulk Container</td></tr>'''

    specs_section = f'''<section style="padding:56px 0;background:#fff;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;">
      <div>
        <span class="sec-eyebrow">Specifications</span>
        <h2 class="sec-title">Product Specifications</h2>
        <div class="sec-divider"></div>
        <table class="spec-table"><tbody>
          {spec_rows}
        </tbody></table>
        <div style="margin-top:32px;">
          <span class="sec-eyebrow">Packaging Options</span>
          <div class="pkg-chips">
            <span class="pkg-chip"><i class="fas fa-box"></i> 25 kg PP Bag</span>
            <span class="pkg-chip"><i class="fas fa-box"></i> 50 kg Jute Bag</span>
            <span class="pkg-chip"><i class="fas fa-boxes"></i> 1 MT Bulk Bag</span>
            <span class="pkg-chip"><i class="fas fa-ship"></i> FCL 20'/40'</span>
          </div>
        </div>
      </div>
      <div>
        <span class="sec-eyebrow">About This Product</span>
        <h2 class="sec-title">About {prod_name}</h2>
        <div class="sec-divider"></div>
        <p style="font-family:'Open Sans',sans-serif;font-size:14.5px;color:#444;line-height:1.8;margin-bottom:16px;">
          {prod_name} is a premium export-quality product from {origin}, India. With {grade}, it meets the highest international standards for quality and consistency.
        </p>
        <p style="font-family:'Open Sans',sans-serif;font-size:14.5px;color:#444;line-height:1.8;">
          Radiance Overseas supplies {prod_name} directly from certified farms and modern processing units. All batches are tested at NABL-accredited laboratories for moisture, foreign matter, and chemical residues before shipment.
        </p>
      </div>
    </div>
  </div>
</section>'''

    # Variants grid
    variants_section = ''
    if variants:
        variant_cards = ''.join(f'''<a href="{v["file"]}" class="rel-card">
  <div class="rel-img"><img src="{IMG_URL}" alt="{v["name"]}" loading="lazy" onerror="this.parentNode.style.background='#eee';this.style.display='none'"></div>
  <div class="rel-body">
    <div class="rel-name">{v["name"]}</div>
    <div class="rel-orig"><i class="fas fa-tag"></i> {v.get("spec", "")}</div>
    <div class="rel-note">{v.get("note", "")}</div>
    <div class="rel-cta" style="color:#5a4200;">View Details ›</div>
  </div>
</a>
''' for v in variants)
        variants_section = f'''<section style="padding:48px 0;background:#f7fbf7;">
  <div class="container">
    <span class="sec-eyebrow">Available Forms</span>
    <h2 class="sec-title">Variants of {prod_name}</h2>
    <div class="sec-divider"></div>
    <div class="rel-grid">
{variant_cards}    </div>
  </div>
</section>'''

    # Related products (other products in same subcategory, max 3)
    related_section = ''
    related_products = [(n, d) for n, d in subcat_products.items()
                        if d.get('file') != prod_file][:3]
    if related_products:
        rel_cards = ''.join(f'''<a href="{d["file"]}" class="rel-card">
  <div class="rel-img"><img src="{IMG_URL}" alt="{n}" loading="lazy" onerror="this.parentNode.style.background='#eee';this.style.display='none'"></div>
  <div class="rel-body">
    <div class="rel-name">{n}</div>
    <div class="rel-orig"><i class="fas fa-map-marker-alt"></i> {d.get("origin", "India")}</div>
    <div class="rel-note">{d.get("grade", "")}</div>
    <div class="rel-cta" style="color:#5a4200;">View Details ›</div>
  </div>
</a>
''' for n, d in related_products)
        related_section = f'''<section style="padding:48px 0;background:#fff;">
  <div class="container">
    <span class="sec-eyebrow">Related Products</span>
    <h2 class="sec-title">More {subcat_name}</h2>
    <div class="sec-divider"></div>
    <div class="rel-grid">
{rel_cards}    </div>
  </div>
</section>'''

    faq_section = gen_prod_faqs(prod_name, origin, grade)
    cta = gen_sp_cta()

    return '\n'.join([
        head,
        COMMON_WRAPPER,
        '\n',
        PROD_CSS,
        '\n',
        hero,
        specs_section,
        variants_section,
        related_section,
        faq_section,
        cta,
        COMMON_FOOTER,
    ])


# ── Variant page builder ───────────────────────────────────────────────────────

def build_variant_page(variant, parent_prod_name, parent_prod_data,
                       cat_name, cat_file, subcat_name,
                       COMMON_WRAPPER, COMMON_FOOTER, PROD_CSS):
    var_name = variant['name']
    var_file = variant['file']
    var_spec = variant.get('spec', '')
    var_note = variant.get('note', '')
    parent_file = parent_prod_data['file']
    parent_grade = parent_prod_data.get('grade', '')
    parent_origin = parent_prod_data.get('origin', 'India')
    all_variants = parent_prod_data.get('variants', [])

    title = f"{var_name} Export — {var_spec} | {parent_prod_name} | Radiance Overseas"
    desc = f"Buy bulk {var_name} from India. Specification: {var_spec}. {var_note}. Parent product: {parent_prod_name}. Radiance Overseas certified exporter."
    keywords = f"{var_name.lower()} export india,{parent_prod_name.lower()} {var_name.lower()},bulk {var_name.lower()} supplier"
    canonical = var_file

    breadcrumb_schema = f'{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Home","item":"https://www.radianceoverseas.com/"}},{{"@type":"ListItem","position":2,"name":"Products","item":"https://www.radianceoverseas.com/Product.html"}},{{"@type":"ListItem","position":3,"name":"{cat_name}","item":"https://www.radianceoverseas.com/{cat_file}"}},{{"@type":"ListItem","position":4,"name":"{parent_prod_name}","item":"https://www.radianceoverseas.com/{parent_file}"}},{{"@type":"ListItem","position":5,"name":"{var_name}","item":"https://www.radianceoverseas.com/{var_file}"}}]}}'
    schemas_html = f'<script type="application/ld+json">{breadcrumb_schema}</script>'

    head = gen_head(title, desc, keywords, canonical, schemas_html)

    # Variant toggle bar showing all variants of parent product
    variant_links = ''.join(
        f'<a href="{v["file"]}" style="display:inline-flex;align-items:center;padding:6px 14px;border:1.5px solid {"rgba(255,255,255,.8)" if v["file"]==var_file else "rgba(255,255,255,.3)"};border-radius:5px;color:{"#fff" if v["file"]==var_file else "rgba(255,255,255,.7)"};font-family:Poppins,sans-serif;font-size:12px;font-weight:600;text-decoration:none;background:{"rgba(255,255,255,.2)" if v["file"]==var_file else "rgba(255,255,255,.06)"};margin:4px;">{v["name"]}</a>'
        for v in all_variants
    )

    hero = f'''<section class="sp-hero">
  <div class="sp-hero-bg" style="background-image:url('{IMG_URL}');"></div>
  <div class="sp-hero-overlay"></div>
  <div class="sp-breadcrumb">
    <div class="container">
      <ol><li><a href="index.html">Home</a></li>
        <li><span class="sep">/</span></li>
        <li><a href="Product.html">Products</a></li>
        <li><span class="sep">/</span></li>
        <li><a href="{cat_file}">{cat_name}</a></li>
        <li><span class="sep">/</span></li>
        <li><a href="{parent_file}">{parent_prod_name}</a></li>
        <li><span class="sep">/</span></li>
        <li><span class="cur">{var_name}</span></li></ol>
    </div>
  </div>
  <div class="container">
    <div class="sp-hero-inner">
      <div class="sp-hero-grid">
        <div class="sp-hero-img">
          <img src="{IMG_URL}" alt="{var_name} Export India" onerror="this.parentNode.style.background='#222';this.style.display='none'">
        </div>
        <div class="sp-hero-content">
          <span class="sp-eyebrow">{cat_name} · {subcat_name} · Variant</span>
          <h1>{var_name}</h1>
          <p class="sp-also">Part of: <a href="{parent_file}" style="color:rgba(255,255,255,.7);">{parent_prod_name}</a></p>
          <p class="sp-origin"><i class="fas fa-map-marker-alt"></i> Origin: {parent_origin}</p>
          <div class="sp-keynote">{var_spec}{" — " + var_note if var_note else ""}</div>
          <div style="margin-top:12px;">
            <strong style="color:rgba(255,255,255,.9);font-family:Poppins,sans-serif;font-size:12px;">All {parent_prod_name} Variants:</strong>
            <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">{variant_links}</div>
          </div>
          <div class="sp-certs">
            <span class="cert-badge">APEDA</span>
            <span class="cert-badge">EU Organic</span>
            <span class="cert-badge">NABL Tested</span>
          </div>
          <div class="sp-hero-btns">
            <a href="Contact.html#form" class="btn-gold">&#128203; Request a Quote</a>
            <a href="{parent_file}" class="btn-outline-w">&#8592; {parent_prod_name}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>'''

    # Specs section
    specs_section = f'''<section style="padding:56px 0;background:#fff;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;">
      <div>
        <span class="sec-eyebrow">Variant Specifications</span>
        <h2 class="sec-title">{var_name} Spec Sheet</h2>
        <div class="sec-divider"></div>
        <table class="spec-table"><tbody>
          <tr><td class="sl">Variant Name</td><td class="sv">{var_name}</td></tr>
          <tr><td class="sl">Parent Product</td><td class="sv"><a href="{parent_file}">{parent_prod_name}</a></td></tr>
          <tr><td class="sl">Specification</td><td class="sv">{var_spec}</td></tr>
          <tr><td class="sl">Quality Note</td><td class="sv">{var_note if var_note else "—"}</td></tr>
          <tr><td class="sl">Parent Grade</td><td class="sv">{parent_grade}</td></tr>
          <tr><td class="sl">Origin</td><td class="sv">{parent_origin}</td></tr>
          <tr><td class="sl">MOQ</td><td class="sv">25 MT (trial: 5–10 MT)</td></tr>
          <tr><td class="sl">Packaging</td><td class="sv">25 kg PP Bag · 50 kg Jute · Bulk Container</td></tr>
        </tbody></table>
        <div style="margin-top:32px;">
          <span class="sec-eyebrow">Packaging Options</span>
          <div class="pkg-chips">
            <span class="pkg-chip"><i class="fas fa-box"></i> 25 kg PP Bag</span>
            <span class="pkg-chip"><i class="fas fa-box"></i> 50 kg Jute Bag</span>
            <span class="pkg-chip"><i class="fas fa-boxes"></i> 1 MT Bulk Bag</span>
            <span class="pkg-chip"><i class="fas fa-ship"></i> FCL 20'/40'</span>
          </div>
        </div>
      </div>
      <div>
        <span class="sec-eyebrow">About This Variant</span>
        <h2 class="sec-title">About {var_name}</h2>
        <div class="sec-divider"></div>
        <p style="font-family:'Open Sans',sans-serif;font-size:14.5px;color:#444;line-height:1.8;margin-bottom:16px;">
          {var_name} is a variant of {parent_prod_name}, sourced from {parent_origin}, India.
          Specification: {var_spec}. {var_note}
        </p>
        <p style="font-family:'Open Sans',sans-serif;font-size:14.5px;color:#444;line-height:1.8;margin-bottom:20px;">
          All batches are tested at NABL-accredited laboratories before shipment. Full export documentation provided.
        </p>
        <a href="{parent_file}" style="display:inline-flex;align-items:center;gap:8px;background:#f5fbf5;border:1.5px solid #cde8cd;color:#1a4731;font-family:Poppins,sans-serif;font-size:13px;font-weight:700;padding:10px 20px;border-radius:7px;text-decoration:none;">
          &#8592; View All Variants of {parent_prod_name}
        </a>
      </div>
    </div>
  </div>
</section>'''

    faq_section = gen_prod_faqs(var_name, parent_origin, f"{var_spec} — {parent_grade}")
    cta = gen_sp_cta()

    return '\n'.join([
        head,
        COMMON_WRAPPER,
        '\n',
        PROD_CSS,
        '\n',
        hero,
        specs_section,
        faq_section,
        cta,
        COMMON_FOOTER,
    ])


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    # Load JSON
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        hierarchy = json.load(f)

    # Load templates
    with open(RICE_TPL, 'r', encoding='utf-8') as f:
        rice_content = f.read()

    with open(PROD_TPL, 'r', encoding='utf-8') as f:
        prod_content = f.read()

    # Extract common sections
    COMMON_WRAPPER = extract_common_wrapper(rice_content)
    COMMON_FOOTER  = extract_common_footer(rice_content)
    CAT_CSS        = extract_css_block(rice_content)
    PROD_CSS       = extract_css_block(prod_content)

    generated = 0
    skipped = 0

    # ── Category pages ──────────────────────────────────────────────────────────
    for cat_name, cat_data in hierarchy.items():
        cat_meta = None
        # Try exact match first, then fuzzy
        for key, meta in CAT_META.items():
            if key == cat_name or meta['file'] == cat_data.get('file'):
                cat_meta = meta
                break
        if cat_meta is None:
            # Build a basic meta from the JSON
            cat_meta = {
                "emoji": cat_data.get("emoji", "🌿"),
                "file": cat_data.get("file", ""),
                "desc": f"Premium {cat_name} from India",
                "badges": ["FSSAI Approved","EU Organic","MOQ 25 MT","NABL Tested"],
                "moq": "25 MT",
                "certs": ["FSSAI","EU Organic","India Organic","NABL"],
                "img_kw": "product",
            }

        cat_file = cat_data.get('file', '')
        if not cat_file:
            continue

        if cat_file in SKIP_FILES:
            skipped += 1
            print(f"Skipping (already exists): {cat_file}")
            continue

        print(f"Generating: {cat_file}")
        html = build_category_page(
            cat_name, cat_data, cat_meta,
            COMMON_WRAPPER, COMMON_FOOTER, CAT_CSS
        )
        out_path = os.path.join(BASE_DIR, cat_file)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        generated += 1

        # ── Sub-category iteration for products & variants ──────────────────────
        subcategories = cat_data.get('subcategories', {})
        for subcat_name, subcat_data in subcategories.items():
            products = subcat_data.get('products', {})

            for prod_name, prod_data in products.items():
                prod_file = prod_data.get('file', '')
                if not prod_file:
                    continue

                if prod_file in SKIP_FILES:
                    skipped += 1
                    print(f"Skipping (already exists): {prod_file}")
                    continue

                print(f"Generating: {prod_file}")
                html = build_product_page(
                    prod_name, prod_data, cat_name, cat_file, subcat_name,
                    products, COMMON_WRAPPER, COMMON_FOOTER, PROD_CSS
                )
                out_path = os.path.join(BASE_DIR, prod_file)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                generated += 1

                # ── Variants ────────────────────────────────────────────────────
                for variant in prod_data.get('variants', []):
                    var_file = variant.get('file', '')
                    if not var_file:
                        continue

                    if var_file in SKIP_FILES:
                        skipped += 1
                        print(f"Skipping (already exists): {var_file}")
                        continue

                    print(f"Generating: {var_file}")
                    html = build_variant_page(
                        variant, prod_name, prod_data,
                        cat_name, cat_file, subcat_name,
                        COMMON_WRAPPER, COMMON_FOOTER, PROD_CSS
                    )
                    out_path = os.path.join(BASE_DIR, var_file)
                    with open(out_path, 'w', encoding='utf-8') as f:
                        f.write(html)
                    generated += 1

    print(f"\nDone! Generated {generated} pages, skipped {skipped}")


if __name__ == '__main__':
    main()
