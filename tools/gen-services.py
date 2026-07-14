#!/usr/bin/env python3
"""Generate one page per Claude service under site/studio/services/<slug>/index.html.
Content sourced from the recognised 14-service catalogue; design = studio identity."""
import os, html, json

BASE = "/Users/arunkumar/Documents/Claude/Projects/PrismEvents/site/services"
# Live host for canonical/sitemap. Swap to the custom domain when it goes live.
BASE_URL = "https://aru497.github.io/prism-automate-site"

CATS = {
    "strategy": "Strategy & Advisory",
    "build": "Build & Engineering",
    "deploy": "Implementation & Deployment",
    "run": "Ongoing & Managed Services",
}

S = json.load(open(os.path.join(os.path.dirname(__file__), "services-data.json"), encoding="utf-8"))

def esc(t): return html.escape(t, quote=False)

def related(svc):
    sibs = [x for x in S if x["cat"] == svc["cat"] and x["slug"] != svc["slug"]]
    return "\n".join(
        f'        <a class="rel" href="../{x["slug"]}/"><span>{esc(x["name"])}</span>'
        f'<svg width="18" height="11" viewBox="0 0 24 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M0 6h22M17 1l5 5-5 5"/></svg></a>'
        for x in sibs)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} | Claude Services | Prism Automate</title>
  <meta name="description" content="{meta_desc}" />
  <link rel="canonical" href="{canonical}" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{name} | Claude Services | Prism Automate" />
  <meta property="og:description" content="{meta_desc}" />
  <meta name="geo.placename" content="Bengaluru, India" />
  <link rel="icon" type="image/png" href="../../assets/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600;700&family=Hanken+Grotesk:wght@200;300&family=Spectral:ital,wght@1,300;1,400&display=swap" rel="stylesheet" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "Service",
        "name": "{name}",
        "serviceType": "{name}",
        "description": "{meta_desc}",
        "provider": {{ "@type": "Organization", "name": "Prism Automate" }},
        "areaServed": ["India", "United Arab Emirates", "Saudi Arabia", "Qatar", "Australia", "Singapore", "Philippines", "Rwanda", "Kenya", "Nigeria", "South Africa", "Egypt", "Brazil"]
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Prism Automate", "item": "../../" }},
          {{ "@type": "ListItem", "position": 2, "name": "{cat_name}" }},
          {{ "@type": "ListItem", "position": 3, "name": "{name}" }}
        ]
      }},
      {{ "@type": "FAQPage", "mainEntity": {faq_json} }}
    ]
  }}
  </script>
  <style>
    :root {{
      --paper: #f1f0f6; --ink: #16121f; --ink-deep: #0d0a15; --ink-soft: #6b6579;
      --line: rgba(22,18,31,0.12); --line-dk: rgba(255,255,255,0.14);
      --violet: #6a5ae0; --violet-lo: #a89ef1; --gold: #d9a86a;
      --cream-dim: rgba(255,255,255,0.6);
      --font: "Familjen Grotesk", Arial, sans-serif; --serif: "Spectral", Georgia, serif;
      --ease: cubic-bezier(0.16, 1, 0.3, 1);
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; background: var(--paper); color: var(--ink); font: 400 1.0625rem/1.6 var(--font); -webkit-font-smoothing: antialiased; }}
    h1, h2, h3 {{ margin: 0; text-wrap: balance; letter-spacing: -0.02em; }}
    p {{ margin: 0; max-width: 62ch; }}
    a {{ color: inherit; }}
    .wrap {{ max-width: 1160px; margin: 0 auto; padding-inline: clamp(1.25rem, 5vw, 3rem); }}
    .eyebrow {{ font-size: 0.72rem; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; }}
    .nav {{ position: fixed; inset: 0 0 auto 0; z-index: 40; height: 74px; display: flex; align-items: center; color: var(--paper); background: rgba(5,4,8,0.72); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid var(--line-dk); }}
    .nav .wrap {{ width: 100%; display: flex; align-items: center; gap: 2rem; }}
    .brand {{ font-size: 1.15rem; font-weight: 700; text-decoration: none; }}
    .brand b {{ color: var(--gold); font-weight: 700; }}
    .brand img {{ height: 26px; width: auto; display: block; }}
    .nav-links {{ list-style: none; margin: 0 0 0 auto; padding: 0; display: flex; gap: 1.9rem; }}
    .nav-links a {{ text-decoration: none; font-size: 0.95rem; font-weight: 500; color: rgba(241,240,246,0.72); transition: color 0.2s; }}
    .nav-links a:hover, .nav-links a.active {{ color: var(--paper); }}
    .nav-cta {{ border: 1px solid currentColor; padding: 0.55rem 1.25rem; text-decoration: none; font-size: 0.9rem; font-weight: 600; }}
    .nav-cta:hover {{ background: var(--paper); color: var(--ink); }}
    .nav-toggle {{ display: none; margin-left: auto; background: none; border: 0; padding: 0.55rem 0.3rem; cursor: pointer; color: inherit; }}
    .nav-toggle span {{ display: block; width: 25px; height: 2px; background: currentColor; transition: transform 0.3s, opacity 0.2s; }}
    .nav-toggle span + span {{ margin-top: 6px; }}
    .nav-toggle[aria-expanded="true"] span:nth-child(1) {{ transform: translateY(8px) rotate(45deg); }}
    .nav-toggle[aria-expanded="true"] span:nth-child(2) {{ opacity: 0; }}
    .nav-toggle[aria-expanded="true"] span:nth-child(3) {{ transform: translateY(-8px) rotate(-45deg); }}
    .mobile-menu {{ position: fixed; inset: 0; z-index: 45; background: rgba(5,4,8,0.98); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); display: flex; flex-direction: column; padding: 96px clamp(1.5rem,7vw,3rem) 2.4rem; opacity: 0; visibility: hidden; transform: translateY(-8px); transition: opacity 0.32s var(--ease), transform 0.32s var(--ease), visibility 0s linear 0.32s; overflow-y: auto; }}
    .mobile-menu.open {{ opacity: 1; visibility: visible; transform: none; transition-delay: 0s; }}
    .mobile-menu a.mm-link {{ color: var(--paper); text-decoration: none; font-family: "Hanken Grotesk", var(--font); font-weight: 200; font-size: clamp(1.9rem,8vw,2.7rem); letter-spacing: -0.02em; padding: 0.7rem 0; border-bottom: 1px solid var(--line-dk); display: flex; justify-content: space-between; align-items: center; }}
    .mobile-menu a.mm-link .ar {{ color: var(--violet-lo); opacity: 0.7; font-size: 0.7em; }}
    .mm-cta {{ margin-top: 2rem; background: var(--paper); color: var(--ink); text-align: center; padding: 1.05rem; font-weight: 600; text-decoration: none; }}
    .mm-foot {{ margin-top: 1.6rem; color: var(--cream-dim); font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; }}
    @media (min-width: 861px) {{ .mobile-menu {{ display: none; }} }}
    .hero {{ background: #050408; color: var(--paper); padding: 170px 0 clamp(4rem, 10vh, 6.5rem); }}
    .hero .eyebrow {{ color: var(--violet-lo); }}
    .hero h1 {{ font-family: "Hanken Grotesk", var(--font); font-weight: 200; font-size: clamp(2.6rem, 6.4vw, 5.2rem); line-height: 1.02; margin-top: 1.1rem; max-width: 15ch; }}
    .hero .lede {{ margin-top: 1.5rem; color: var(--cream-dim); font-size: clamp(1.05rem, 1.7vw, 1.25rem); max-width: 46ch; }}
    .media-band {{ background: linear-gradient(#050408 0 55%, var(--paper) 55% 100%); }}
    .media-band figure {{ margin: 0; border-radius: 0; overflow: clip; aspect-ratio: 21 / 9; box-shadow: 0 30px 80px rgba(5, 4, 8, 0.35); }}
    .media-band img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .arrow-link {{ display: inline-flex; align-items: center; gap: 0.6rem; margin-top: 2rem; text-decoration: none; font-weight: 600; color: var(--gold); }}
    .arrow-link svg {{ transition: transform 0.25s var(--ease); }}
    .arrow-link:hover svg {{ transform: translateX(6px); }}
    section {{ padding-block: clamp(3.5rem, 8vh, 6rem); }}
    .sec-label {{ color: var(--violet); font-weight: 600; font-size: 0.9rem; }}
    h2 {{ font-size: clamp(1.7rem, 3.2vw, 2.5rem); font-weight: 500; margin-top: 0.6rem; }}
    .inc-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(1.25rem, 3vw, 2.5rem); margin-top: 2.2rem; }}
    .inc h3 {{ font-size: 1.12rem; font-weight: 600; }}
    .inc h3::before {{ content: ""; display: block; width: 34px; height: 2px; background: var(--gold); margin-bottom: 0.9rem; }}
    .inc p {{ margin-top: 0.55rem; color: var(--ink-soft); font-size: 0.97rem; }}
    .steps {{ border-block: 1px solid var(--line); }}
    .step-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(1.25rem, 3vw, 2.5rem); margin-top: 2.2rem; counter-reset: st; }}
    .step {{ border-top: 1px solid var(--line); padding-top: 1.1rem; }}
    .step::before {{ counter-increment: st; content: "0" counter(st); color: var(--violet); font-weight: 600; font-size: 0.85rem; letter-spacing: 0.15em; }}
    .step h3 {{ font-family: var(--serif); font-style: italic; font-weight: 400; font-size: 1.35rem; margin-top: 0.5rem; }}
    .step p {{ margin-top: 0.5rem; color: var(--ink-soft); font-size: 0.96rem; }}
    .fit ul {{ margin: 1.6rem 0 0; padding: 0; list-style: none; display: grid; gap: 0.8rem; max-width: 56ch; }}
    .svc-faq .faq-list {{ margin-top: 2rem; max-width: 820px; }}
    .svc-faq details {{ border-bottom: 1px solid var(--line); }}
    .svc-faq summary {{ cursor: pointer; list-style: none; padding: 1.25rem 0; font-weight: 600; font-size: 1.05rem; display: flex; justify-content: space-between; align-items: center; gap: 1rem; }}
    .svc-faq summary::-webkit-details-marker {{ display: none; }}
    .svc-faq summary::after {{ content: "+"; font-size: 1.45rem; font-weight: 300; color: var(--violet); transition: transform 0.25s var(--ease); flex: none; line-height: 1; }}
    .svc-faq details[open] summary::after {{ transform: rotate(45deg); }}
    .svc-faq details p {{ color: var(--ink-soft); padding-bottom: 1.25rem; line-height: 1.7; max-width: 74ch; }}
    .fit li {{ display: flex; gap: 0.7rem; color: var(--ink-soft); }}
    .fit li::before {{ content: ""; flex: none; width: 9px; height: 9px; border-radius: 50%; background: var(--violet-lo); margin-top: 0.5rem; }}
    .rel-row {{ display: grid; gap: 0.4rem; margin-top: 2rem; max-width: 620px; }}
    .rel {{ display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1rem 0; border-bottom: 1px solid var(--line); text-decoration: none; font-weight: 600; }}
    .rel svg {{ color: var(--violet); transition: transform 0.25s var(--ease); }}
    .rel:hover svg {{ transform: translateX(6px); }}
    .cta {{ background: var(--ink-deep); color: var(--paper); }}
    .cta .wrap {{ display: grid; grid-template-columns: 1fr auto; gap: 2rem; align-items: center; }}
    .cta h2 {{ font-weight: 500; max-width: 17ch; }}
    .cta h2 em {{ font-family: var(--serif); font-style: italic; font-weight: 400; color: var(--violet-lo); }}
    .cta small {{ display: block; margin-top: 0.8rem; color: var(--cream-dim); }}
    .btn-solid {{ background: var(--paper); color: var(--ink); text-decoration: none; padding: 1rem 2.2rem; border-radius: 0; font-weight: 600; white-space: nowrap; }}
    .btn-solid:hover {{ background: var(--violet-lo); }}
    footer {{ background: var(--ink-deep); color: var(--cream-dim); border-top: 1px solid var(--line-dk); padding-block: 1.6rem; font-size: 0.86rem; }}
    footer .wrap {{ display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }}
    @supports (animation-timeline: view()) {{
      @media (prefers-reduced-motion: no-preference) {{
        .inc, .step, .fit li, .rel {{ animation: rise 1ms ease-out both; animation-timeline: view(); animation-range: entry 5% cover 32%; }}
      }}
    }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(30px); }} }}
    @media (max-width: 860px) {{
      .inc-grid, .step-grid {{ grid-template-columns: 1fr; }}
      .cta .wrap {{ grid-template-columns: 1fr; }}
      .nav-links {{ display: none; }}
      .nav-cta {{ display: none; }}
      .nav-toggle {{ display: block; }}
    }}
  </style>
</head>
<body>
  <nav class="nav" aria-label="Main">
    <div class="wrap">
      <a class="brand" href="../../"><img src="../../assets/logo-wordmark.png" alt="Prism Automate" width="115" height="30" /></a>
      <ul class="nav-links">
        <li><a href="../" class="active">Services</a></li>
        <li><a href="../../solutions/">Solutions</a></li>
        <li><a href="../../claude/">Claude</a></li>
      </ul>
      <a class="nav-cta" href="../../claude/#interest">I'm Interested</a>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
    </div>
  </nav>

  <div class="mobile-menu" id="mobile-menu" aria-hidden="true">
    <nav class="mm-nav" aria-label="Mobile">
      <a class="mm-link" href="../">Services</a>
      <a class="mm-link" href="../../solutions/">Solutions <svg class="ar" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></a>
      <a class="mm-link" href="../../claude/">Claude <svg class="ar" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></a>
      <a class="mm-cta" href="../../claude/#interest">I'm Interested</a>
    </nav>
    <p class="mm-foot">Bengaluru · Dubai · Sydney</p>
  </div>

  <header class="hero">
    <div class="wrap">
      <p class="eyebrow">{cat_name}</p>
      <h1>{name}</h1>
      <p class="lede">{definition}</p>
      <a class="arrow-link" href="../../#contact">Scope this with us
        <svg width="22" height="12" viewBox="0 0 24 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M0 6h22M17 1l5 5-5 5"/></svg>
      </a>
    </div>
  </header>
{media_html}
  <section>
    <div class="wrap">
      <span class="sec-label">What's included</span>
      <h2>What you get</h2>
      <div class="inc-grid">
{included_html}
      </div>
    </div>
  </section>

  <section class="steps">
    <div class="wrap">
      <span class="sec-label">How it runs</span>
      <h2>Three moves, no mystery</h2>
      <div class="step-grid">
{steps_html}
      </div>
    </div>
  </section>

  <section class="fit">
    <div class="wrap">
      <span class="sec-label">Is this you?</span>
      <h2>A good fit if</h2>
      <ul>
{fit_html}
      </ul>
    </div>
  </section>

  <section>
    <div class="wrap">
      <span class="sec-label">{cat_name}</span>
      <h2>Related services</h2>
      <div class="rel-row">
{related_html}
      </div>
    </div>
  </section>

  <section class="svc-faq">
    <div class="wrap">
      <span class="sec-label">Questions</span>
      <h2>Frequently asked</h2>
      <div class="faq-list">
{faq_html}
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap">
      <div>
        <h2>Let's scope <em>{name_lower}</em> for your team.</h2>
        <small>A real person replies within one business day. Bengaluru · Dubai · Sydney.</small>
      </div>
      <a class="btn-solid" href="../../#contact">Start a project</a>
    </div>
  </section>

  <footer>
    <div class="wrap">
      <span>Prism Automate © 2026 · Anthropic Claude Partner</span>
      <span><a href="../../" style="color:inherit">Home</a> · <a href="../" style="color:inherit">All services</a> · <a href="../../faq/" style="color:inherit">FAQ</a></span>
    </div>
  </footer>
  <script src="../../assets/nav.js" defer></script>
  <script src="../../assets/interest.js" defer></script>
</body>
</html>
"""

for svc in S:
    inc = "\n".join(
        f'        <div class="inc"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for t, d in svc["included"])
    steps = "\n".join(
        f'        <div class="step"><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for t, d in svc["steps"])
    fit = "\n".join(f'        <li>{esc(x)}</li>' for x in svc["fit"])
    faq_pairs = svc.get("faq", [])
    faq_html = "\n".join(
        f'        <details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>'
        for q, a in faq_pairs)
    faq_json = json.dumps(
        [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
         for q, a in faq_pairs], ensure_ascii=False)
    meta = svc["definition"] + " Delivered by Prism Automate, an Anthropic Claude partner serving India, the Middle East, and Australia."
    media = ""
    if svc.get("img"):
        media = (
            '\n  <div class="media-band" aria-hidden="false">\n'
            f'    <div class="wrap"><figure><img src="{html.escape(svc["img"], quote=True)}" '
            f'alt="{html.escape(svc.get("img_alt", svc["name"]), quote=True)}" loading="lazy" /></figure></div>\n'
            '  </div>\n')
    page = PAGE.format(
        name=esc(svc["name"]), name_lower=esc(svc["name"][0].lower() + svc["name"][1:]),
        cat_name=esc(CATS[svc["cat"]]), definition=esc(svc["definition"]),
        meta_desc=esc(meta.replace('"', "'")),
        canonical=f"{BASE_URL}/services/{svc['slug']}/",
        media_html=media, faq_html=faq_html, faq_json=faq_json,
        included_html=inc, steps_html=steps, fit_html=fit, related_html=related(svc))
    outdir = os.path.join(BASE, svc["slug"])
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w").write(page)
    print("wrote", svc["slug"])

print(f"\n{len(S)} service pages generated")


# ---------- Services overview page (/studio/services/) ----------
OV_CARD = """        <a class="svc" href="{slug}/">
          <span class="svc-name">{name}</span>
          <span class="svc-def">{definition}</span>
          <svg width="18" height="11" viewBox="0 0 24 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M0 6h22M17 1l5 5-5 5"/></svg>
        </a>"""

cat_order = ["strategy", "build", "deploy", "run"]
cat_blurbs = {
    "strategy": "Start with the business case, not the hype.",
    "build": "Agents that reach production, not another pilot.",
    "deploy": "Rollout that survives contact with real users.",
    "run": "Someone owns it after launch.",
}
groups = ""
for c in cat_order:
    cards = "\n".join(OV_CARD.format(slug=x["slug"], name=esc(x["name"]), definition=esc(x["definition"])) for x in S if x["cat"] == c)
    groups += f"""
    <section class="cat">
      <div class="wrap">
        <div class="cat-head">
          <h2>{esc(CATS[c])}</h2>
          <p class="ser">{esc(cat_blurbs[c])}</p>
        </div>
        <div class="svc-grid">
{cards}
        </div>
      </div>
    </section>
"""

OVERVIEW = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Services | The Full Claude Catalogue | Prism Automate</title>
  <meta name="description" content="All fourteen recognised Claude services delivered by Prism Automate, an Anthropic Claude partner: strategy, build, deployment, and managed operations for teams in India, the Middle East, and Australia." />
  <link rel="canonical" href="https://aru497.github.io/prism-automate-site/services/" />
  <meta name="robots" content="index, follow, max-image-preview:large" />
  <meta name="geo.placename" content="Bengaluru, India" />
  <link rel="icon" type="image/png" href="../assets/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600;700&family=Hanken+Grotesk:wght@200;300&family=Spectral:ital,wght@1,300;1,400&display=swap" rel="stylesheet" />
  <style>
    :root {
      --paper: #f1f0f6; --ink: #16121f; --ink-deep: #0d0a15; --ink-soft: #6b6579;
      --line: rgba(22,18,31,0.12); --line-dk: rgba(255,255,255,0.14);
      --violet: #6a5ae0; --violet-lo: #a89ef1; --gold: #d9a86a;
      --cream-dim: rgba(255,255,255,0.6);
      --font: "Familjen Grotesk", Arial, sans-serif; --serif: "Spectral", Georgia, serif;
      --ease: cubic-bezier(0.16, 1, 0.3, 1);
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--paper); color: var(--ink); font: 400 1.0625rem/1.6 var(--font); -webkit-font-smoothing: antialiased; }
    h1, h2 { margin: 0; letter-spacing: -0.02em; text-wrap: balance; }
    p { margin: 0; }
    a { color: inherit; }
    .ser { font-family: var(--serif); font-style: italic; color: var(--violet); }
    .wrap { max-width: 1160px; margin: 0 auto; padding-inline: clamp(1.25rem, 5vw, 3rem); }
    .nav { position: fixed; inset: 0 0 auto 0; z-index: 40; height: 74px; display: flex; align-items: center; color: var(--paper); background: rgba(5,4,8,0.72); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border-bottom: 1px solid var(--line-dk); }
    .nav .wrap { width: 100%; display: flex; align-items: center; gap: 2rem; }
    .brand { font-size: 1.15rem; font-weight: 700; text-decoration: none; }
    .brand b { color: var(--gold); }
    .brand img { height: 26px; width: auto; display: block; }
    .media-band { background: linear-gradient(#050408 0 55%, var(--paper) 55% 100%); }
    .media-band figure { margin: 0; border-radius: 0; overflow: clip; aspect-ratio: 21 / 9; box-shadow: 0 30px 80px rgba(5, 4, 8, 0.35); }
    .media-band img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .nav-links { list-style: none; margin: 0 0 0 auto; padding: 0; display: flex; gap: 1.9rem; }
    .nav-links a { text-decoration: none; font-size: 0.95rem; font-weight: 500; color: rgba(241,240,246,0.72); transition: color 0.2s; }
    .nav-links a:hover, .nav-links a.active { color: var(--paper); }
    .nav-cta { border: 1px solid currentColor; padding: 0.55rem 1.25rem; text-decoration: none; font-size: 0.9rem; font-weight: 600; }
    .nav-cta:hover { background: var(--paper); color: var(--ink); }
    .nav-toggle { display: none; margin-left: auto; background: none; border: 0; padding: 0.55rem 0.3rem; cursor: pointer; color: inherit; }
    .nav-toggle span { display: block; width: 25px; height: 2px; background: currentColor; transition: transform 0.3s, opacity 0.2s; }
    .nav-toggle span + span { margin-top: 6px; }
    .nav-toggle[aria-expanded="true"] span:nth-child(1) { transform: translateY(8px) rotate(45deg); }
    .nav-toggle[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
    .nav-toggle[aria-expanded="true"] span:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }
    .mobile-menu { position: fixed; inset: 0; z-index: 45; background: rgba(5,4,8,0.98); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); display: flex; flex-direction: column; padding: 96px clamp(1.5rem,7vw,3rem) 2.4rem; opacity: 0; visibility: hidden; transform: translateY(-8px); transition: opacity 0.32s ease, transform 0.32s ease, visibility 0s linear 0.32s; overflow-y: auto; }
    .mobile-menu.open { opacity: 1; visibility: visible; transform: none; transition-delay: 0s; }
    .mobile-menu a.mm-link { color: var(--paper); text-decoration: none; font-family: "Hanken Grotesk", var(--font); font-weight: 200; font-size: clamp(1.9rem,8vw,2.7rem); letter-spacing: -0.02em; padding: 0.7rem 0; border-bottom: 1px solid var(--line-dk); display: flex; justify-content: space-between; align-items: center; }
    .mobile-menu a.mm-link .ar { color: var(--violet-lo); opacity: 0.7; font-size: 0.7em; }
    .mm-cta { margin-top: 2rem; background: var(--paper); color: var(--ink); text-align: center; padding: 1.05rem; font-weight: 600; text-decoration: none; }
    .mm-foot { margin-top: 1.6rem; color: var(--cream-dim); font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; }
    @media (min-width: 861px) { .mobile-menu { display: none; } }
    .hero { background: #050408; color: var(--paper); padding: 170px 0 clamp(4rem, 9vh, 6rem); }
    .hero .eyebrow { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: var(--violet-lo); }
    .hero h1 { font-family: "Hanken Grotesk", var(--font); font-weight: 200; font-size: clamp(2.8rem, 7vw, 5.6rem); line-height: 1; margin-top: 1.1rem; }
    .hero p.lede { margin-top: 1.4rem; color: var(--cream-dim); max-width: 52ch; font-size: 1.1rem; }
    .cat { padding-block: clamp(3rem, 7vh, 5rem); border-bottom: 1px solid var(--line); }
    .cat-head { display: flex; align-items: baseline; justify-content: space-between; gap: 1.5rem; flex-wrap: wrap; }
    .cat-head h2 { font-size: clamp(1.6rem, 3vw, 2.3rem); font-weight: 500; }
    .cat-head .ser { font-size: 1.1rem; }
    .svc-grid { margin-top: 1.8rem; display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; }
    .svc { display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 0.4rem 1.2rem; padding: 1.15rem 1.35rem; border: 1px solid var(--line); border-radius: 0; text-decoration: none; background: #fff; transition: border-color 0.25s var(--ease), transform 0.25s var(--ease); }
    .svc:hover { border-color: var(--violet); transform: translateY(-2px); }
    .svc-name { font-weight: 600; }
    .svc-def { grid-column: 1 / -1; color: var(--ink-soft); font-size: 0.92rem; }
    .svc svg { color: var(--violet); }
    .cta { background: var(--ink-deep); color: var(--paper); padding-block: clamp(3.5rem, 8vh, 5.5rem); }
    .cta .wrap { display: grid; grid-template-columns: 1fr auto; gap: 2rem; align-items: center; }
    .cta h2 { font-weight: 500; }
    .btn-solid { background: var(--paper); color: var(--ink); text-decoration: none; padding: 1rem 2.2rem; border-radius: 0; font-weight: 600; white-space: nowrap; }
    .btn-solid:hover { background: var(--violet-lo); }
    footer { background: var(--ink-deep); color: var(--cream-dim); border-top: 1px solid var(--line-dk); padding-block: 1.6rem; font-size: 0.86rem; }
    footer .wrap { display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; }
    @supports (animation-timeline: view()) {
      @media (prefers-reduced-motion: no-preference) {
        .svc { animation: rise 1ms ease-out both; animation-timeline: view(); animation-range: entry 4% cover 26%; }
      }
    }
    @keyframes rise { from { opacity: 0; transform: translateY(26px); } }
    @media (max-width: 820px) { .svc-grid { grid-template-columns: 1fr; } .cta .wrap { grid-template-columns: 1fr; } .nav-links { display: none; } .nav-cta { display: none; } .nav-toggle { display: block; } }
  </style>
</head>
<body>
  <nav class="nav" aria-label="Main">
    <div class="wrap">
      <a class="brand" href="../"><img src="../assets/logo-wordmark.png" alt="Prism Automate" width="115" height="30" /></a>
      <ul class="nav-links">
        <li><a href="./" class="active">Services</a></li>
        <li><a href="../solutions/">Solutions</a></li>
        <li><a href="../claude/">Claude</a></li>
      </ul>
      <a class="nav-cta" href="../claude/#interest">I'm Interested</a>
      <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
    </div>
  </nav>

  <div class="mobile-menu" id="mobile-menu" aria-hidden="true">
    <nav class="mm-nav" aria-label="Mobile">
      <a class="mm-link" href="./">Services</a>
      <a class="mm-link" href="../solutions/">Solutions <svg class="ar" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></a>
      <a class="mm-link" href="../claude/">Claude <svg class="ar" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></a>
      <a class="mm-cta" href="../claude/#interest">I'm Interested</a>
    </nav>
    <p class="mm-foot">Bengaluru · Dubai · Sydney</p>
  </div>
  <header class="hero">
    <div class="wrap">
      <p class="eyebrow">Anthropic Claude Partner</p>
      <h1>Fourteen services. One studio.</h1>
      <p class="lede">The full recognised Claude catalogue across strategy, build, deploy, and run: from the first roadmap to workloads running under SLAs, delivered by an Anthropic partner to teams in India, the GCC, and Australia.</p>
    </div>
  </header>
OV_MEDIA_TOKEN
GROUPS_TOKEN
  <section class="cta">
    <div class="wrap">
      <h2>Not sure where to start? That's the first service.</h2>
      <a class="btn-solid" href="../#contact">Start a project</a>
    </div>
  </section>
  <footer>
    <div class="wrap">
      <span>Prism Automate © 2026 · Anthropic Claude Partner</span>
      <span><a href="../" style="color:inherit">Home</a> · <a href="../faq/" style="color:inherit">FAQ</a></span>
    </div>
  </footer>
  <script src="../assets/nav.js" defer></script>
  <script src="../assets/interest.js" defer></script>
</body>
</html>
"""

OV_IMG = None  # set to dict(url=..., alt=...) to show a hero image band on the overview
ov_media = ""
if OV_IMG:
    ov_media = (
        '  <div class="media-band">\n'
        f'    <div class="wrap"><figure><img src="{html.escape(OV_IMG["url"], quote=True)}" '
        f'alt="{html.escape(OV_IMG["alt"], quote=True)}" loading="lazy" /></figure></div>\n'
        '  </div>')
open(os.path.join(BASE, "index.html"), "w").write(
    OVERVIEW.replace("OV_MEDIA_TOKEN", ov_media).replace("GROUPS_TOKEN", groups))
print("wrote services overview index")
