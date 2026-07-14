#!/usr/bin/env python3
"""Generate the Solutions page at site/solutions/index.html.
Original copy + Prism Automate studio design; structural inspiration only.
Two products are live in production; four are build offerings, labelled honestly."""
import os, html, json

OUT = "/Users/arunkumar/Documents/Claude/Projects/PrismEvents/site/solutions/index.html"

IMG = "https://images.unsplash.com/photo-{id}?auto=format&fit=crop&w=1600&q=80"

# status: "live" (gold badge) or "build" (violet badge)
SOL = [
 dict(slug="prism-events", name="Prism Events", status="live",
   tagline="Indoor navigation for live events",
   img="1505373877841-8d25f7d46678",
   img_full="../assets/uip/prism-events-showcase.png",
   img_alt="Three Prism Events app screens from the Unisys UIP deployment: the live agenda, the home dashboard with a live poll and venue map, and the event photo gallery.",
   desc="GPS dies the moment attendees walk indoors. Prism Events doesn't. Our Virtual Positioning System puts every visitor's live location on the floor plan and gives turn-by-turn directions to any booth, stage, or session, wrapped in a live agenda and day-tabbed galleries. Shipped and running at the Unisys Innovation Program in Bengaluru.",
   pills=["AR video-map wayfinder","Turn-by-turn routing","Live agenda","Booth & stage finder","Day photo galleries","Works where GPS won't"],
   cta=("See the deployment","../#work"), related=None),

 dict(slug="virtual-try-on", name="Virtual Try-On", status="live",
   tagline="See it before you buy it",
   img="1565849904461-04a58ad377e0",
   img_alt="A hand holding up a smartphone, its camera viewfinder glowing against a dark blue interior.",
   desc="Let shoppers see the product on themselves before they commit. Our retail AR module renders items in real time on any device, lifting confidence and cutting the returns that quietly eat margin. Built, shipped, and embeddable in an afternoon.",
   pills=["Real-time AR","Cross-device","Accurate rendering","Fewer returns","Drop-in embed","Engagement analytics"],
   cta=("Book a demo","../#contact"), related=None),

 dict(slug="ai-concierge", name="AI Concierge & Chatbot", status="build",
   tagline="A concierge that never sleeps",
   img="1531297484001-80022131f5a1",
   img_alt="A laptop open in a dark room, its screen casting a warm glow across a black surface.",
   desc="A Claude-powered assistant that answers questions, qualifies leads, and guides customers across web, app, and chat, with the prompt-injection defence and content controls the open internet demands. It talks to your systems, not just your customers.",
   pills=["Conversational AI","24/7 support","Lead qualification","Multichannel","System integrations","Prompt-injection defence"],
   cta=("Scope a build","../#contact"),
   related=("customer-facing-ai-product","Customer-Facing AI Product Build")),

 dict(slug="ai-voice-agent", name="AI Voice Agent", status="build",
   tagline="Conversations that scale, out loud",
   img="1693066867835-970840dad310",
   img_alt="A studio condenser microphone on a shock mount, lit from behind in violet against black.",
   desc="Claude on the phone, with human-like turn-taking. Voice agents field inbound calls, run outbound follow-ups, and hand the hard ones to a person, with every call transcribed, logged to your CRM, and measured. No hold music, no scripts read like a robot.",
   pills=["Natural voice","Inbound & outbound","Automated follow-ups","Live transcripts","CRM integration","Call analytics"],
   cta=("Scope a build","../#contact"),
   related=("customer-facing-ai-product","Customer-Facing AI Product Build")),

 dict(slug="agentic-platform", name="Agentic Internal Platform", status="build",
   tagline="One set of rails for every team's agents",
   img="1680992046626-418f7e910589",
   img_alt="Racks of network servers in a dark room, lit by rows of green status lights.",
   desc="One governed platform where every team ships agents on Claude: orchestration, connectors to your CRM, ERP, and help desk, memory, and paved-road templates your own engineers own and extend. Built inside your cloud, behind your SSO, with an audit trail on every action.",
   pills=["Agent orchestration","Governed connectors","Memory & tools","Paved-road templates","SSO & audit","Runs in your cloud"],
   cta=("Scope a build","../#contact"),
   related=("internal-agentic-platform","Internal Agentic Platform Build")),

 dict(slug="document-intelligence", name="Document Intelligence", status="build",
   tagline="Turn documents into data",
   img="1697791173189-d56b15df4f33",
   img_alt="A rolling ladder against towering shelves of old leather-bound books in a dim library.",
   desc="Point Claude at the contracts, invoices, and forms clogging your queue. It reads, classifies, and extracts at scale, routes the genuine exceptions to a human, and syncs clean data back to your systems, with an audit trail behind every decision.",
   pills=["Extract & classify","Any format","Human-in-the-loop","Full audit trail","System sync","Accuracy evals"],
   cta=("Scope a build","../#contact"),
   related=("internal-agentic-platform","Internal Agentic Platform Build")),
]

STANDARD = [
 ("Claude-native","Built on Anthropic's Claude as an official partner, not bolted onto a model we don't understand."),
 ("Production-grade","Latency, fallbacks, safety, and evals handled, so it survives real users, not just a demo."),
 ("Owned end-to-end","One accountable team from the first roadmap to the pager at 2am. No hand-offs, no finger-pointing."),
 ("Secure by design","Runs in your cloud, behind your SSO, with audit trails and prompt-injection defence built in."),
 ("Ships in weeks","A first scoped solution reaches production in weeks, then grows from proof, not slideware."),
 ("Multi-region","Delivered across Bengaluru, Dubai and the GCC, and Sydney. Remote-first, on-site when it counts."),
]

def esc(t): return html.escape(t, quote=False)
def escq(t): return html.escape(t, quote=True)

def badge(status):
    if status == "live":
        return '<span class="badge live">Live in production</span>'
    return '<span class="badge build">We build this</span>'

def sol_section(s, i):
    pills = "\n".join(f'          <li>{esc(p)}</li>' for p in s["pills"])
    rel = ""
    if s["related"]:
        rslug, rname = s["related"]
        rel = (f'\n        <a class="rel-svc" href="../services/{rslug}/">Part of our '
               f'{esc(rname)} service'
               f'<svg width="16" height="10" viewBox="0 0 24 12" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M0 6h22M17 1l5 5-5 5"/></svg></a>')
    cta_txt, cta_href = s["cta"]
    rev = " rev" if i % 2 == 1 else ""
    return f"""  <section class="sol{rev}" id="{s['slug']}">
    <div class="wrap sol-grid">
      <div class="sol-rail">
        <span class="sol-num">{i+1:02d}</span>
        <h2 class="sol-name">{esc(s['name'])}</h2>
        {badge(s['status'])}
        <a class="sol-cta" href="{cta_href}">{esc(cta_txt)}
          <svg width="20" height="12" viewBox="0 0 24 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M0 6h22M17 1l5 5-5 5"/></svg>
        </a>
      </div>
      <div class="sol-main">
        <figure class="sol-media"><img src="{s.get('img_full') or IMG.format(id=s['img'])}" alt="{escq(s['img_alt'])}" loading="lazy" /></figure>
        <p class="sol-tag">{esc(s['tagline'])}</p>
        <p class="sol-desc">{esc(s['desc'])}</p>
        <ul class="pills">
{pills}
        </ul>{rel}
      </div>
    </div>
  </section>"""

def std_card(t, d):
    return f"""        <div class="std">
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </div>"""

# JSON-LD: BreadcrumbList + ItemList of solutions
items = []
for i, s in enumerate(SOL):
    items.append({
        "@type": "ListItem", "position": i+1,
        "item": {
            "@type": "Service",
            "name": s["name"],
            "description": s["desc"],
            "provider": {"@type": "Organization", "name": "Prism Automate"},
            "areaServed": ["India", "United Arab Emirates", "Australia"],
        }
    })
ldjson = {
    "@context": "https://schema.org",
    "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Prism Automate", "item": "../"},
            {"@type": "ListItem", "position": 2, "name": "Solutions"},
        ]},
        {"@type": "CollectionPage",
         "name": "Solutions | Prism Automate",
         "description": "AI solutions from Prism Automate, an Anthropic Claude partner: Prism Events indoor navigation and a retail virtual try-on, both live in production, plus AI concierge, voice agents, agentic platforms, and document intelligence built on Claude for teams in India, the GCC, and Australia.",
         "mainEntity": {"@type": "ItemList", "itemListElement": items}},
    ],
}

sections = "\n".join(sol_section(s, i) for i, s in enumerate(SOL))
standards = "\n".join(std_card(t, d) for t, d in STANDARD)
chips = "\n".join(
    f'          <a href="#{s["slug"]}">{esc(s["name"])}</a>' for s in SOL)

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Solutions | AI Products Built on Claude | Prism Automate</title>
  <meta name="description" content="AI solutions from Prism Automate, an Anthropic Claude partner: Prism Events indoor event navigation and a retail virtual try-on, both live in production, plus AI concierge, voice agents, agentic platforms, and document intelligence for teams in India, the GCC, and Australia." />
  <!-- TODO: add canonical + og:url once the production domain is confirmed -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Solutions | AI Products Built on Claude | Prism Automate" />
  <meta property="og:description" content="Two products live in production and four we build on Claude, for teams across India, the GCC, and Australia." />
  <meta property="og:image" content="{IMG.format(id=SOL[0]['img'])}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="theme-color" content="#050408" />
  <link rel="icon" type="image/png" href="../assets/favicon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <script type="application/ld+json">
{json.dumps(ldjson, indent=2)}
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400;500;600;700&family=Hanken+Grotesk:wght@200;300&family=Spectral:ital,wght@0,300;1,300;1,400&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --paper: #f1f0f6; --paper-2: #e7e5f0; --ink: #16121f; --ink-deep: #0d0a15;
      --ink-soft: #6b6579; --black: #050408;
      --line: rgba(22,18,31,0.12); --line-dk: rgba(255,255,255,0.14);
      --violet: #6a5ae0; --violet-lo: #a89ef1; --gold: #d9a86a;
      --cream-dim: rgba(255,255,255,0.6);
      --font: "Familjen Grotesk", "Helvetica Neue", Arial, sans-serif;
      --serif: "Spectral", Georgia, serif; --ease: cubic-bezier(0.16, 1, 0.3, 1);
    }}
    * {{ box-sizing: border-box; }}
    html.inertia-scroll {{ scroll-behavior: auto; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; background: var(--black); color: var(--paper); font: 400 1.0625rem/1.6 var(--font); -webkit-font-smoothing: antialiased; overflow-x: clip; }}
    img, video {{ max-width: 100%; display: block; }}
    h1, h2, h3 {{ margin: 0; text-wrap: balance; letter-spacing: -0.02em; }}
    p {{ margin: 0; }}
    a {{ color: inherit; }}
    .wrap {{ max-width: 1200px; margin: 0 auto; padding-inline: clamp(1.25rem, 5vw, 3rem); }}
    .eyebrow {{ font-size: 0.72rem; font-weight: 600; letter-spacing: 0.22em; text-transform: uppercase; color: var(--violet-lo); }}

    /* Nav */
    .nav {{ position: fixed; inset: 0 0 auto 0; z-index: 40; height: 74px; display: flex; align-items: center; color: var(--paper); transition: background 0.35s var(--ease), border-color 0.35s var(--ease); border-bottom: 1px solid transparent; }}
    .nav.is-solid {{ background: rgba(13,10,21,0.72); backdrop-filter: blur(16px) saturate(150%); -webkit-backdrop-filter: blur(16px) saturate(150%); border-color: var(--line-dk); }}
    .nav .wrap {{ width: 100%; display: flex; align-items: center; gap: 2.2rem; }}
    .brand {{ text-decoration: none; }}
    .brand img {{ height: 28px; width: auto; }}
    .nav-links {{ list-style: none; margin: 0; padding: 0; display: flex; gap: 1.7rem; margin-left: auto; }}
    .nav-links a {{ text-decoration: none; font-size: 0.95rem; color: rgba(241,240,246,0.82); transition: color 0.2s; }}
    .nav-links a:hover, .nav-links a.active {{ color: var(--paper); }}
    .nav-cta {{ border: 1px solid rgba(241,240,246,0.4); border-radius: 999px; padding: 0.5rem 1.2rem; text-decoration: none; font-size: 0.9rem; font-weight: 600; transition: background 0.2s, color 0.2s; }}
    .nav-cta:hover {{ background: var(--paper); color: var(--ink); border-color: var(--paper); }}
    @media (max-width: 820px) {{ .nav-links {{ display: none; }} .nav-cta {{ margin-left: auto; }} }}

    /* Hero */
    .hero {{ position: relative; min-height: 90vh; display: flex; align-items: center; overflow: clip; padding: 120px 0 6rem; }}
    .hero-bg {{ position: absolute; inset: 0; z-index: 0; }}
    .hero-bg video {{ width: 100%; height: 100%; object-fit: cover; opacity: 0.45; }}
    .hero-bg::after {{ content: ""; position: absolute; inset: 0; background: radial-gradient(120% 90% at 70% 30%, transparent, var(--black) 72%), linear-gradient(180deg, rgba(5,4,8,0.4), var(--black)); }}
    .hero .wrap {{ position: relative; z-index: 1; }}
    .hero h1 {{ font-family: "Hanken Grotesk", var(--font); font-weight: 200; font-size: clamp(3rem, 9vw, 8rem); line-height: 0.98; margin-top: 1.2rem; max-width: 15ch; }}
    .hero h1 em {{ font-family: var(--serif); font-style: italic; font-weight: 300; color: var(--violet-lo); }}
    .hero .lede {{ margin-top: 1.8rem; color: rgba(241,240,246,0.78); font-size: clamp(1.1rem, 1.7vw, 1.4rem); line-height: 1.55; max-width: 48ch; }}
    .chips {{ margin-top: 2.6rem; display: flex; flex-wrap: wrap; gap: 0.6rem; }}
    .chips a {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border: 1px solid var(--line-dk); border-radius: 999px; text-decoration: none; font-size: 0.88rem; color: rgba(241,240,246,0.85); transition: border-color 0.2s, background 0.2s; }}
    .chips a::before {{ content: ""; width: 6px; height: 6px; border-radius: 50%; background: var(--violet-lo); }}
    .chips a:hover {{ border-color: var(--violet-lo); background: rgba(168,158,241,0.08); }}

    /* Solution sections */
    .sol {{ border-top: 1px solid var(--line-dk); }}
    .sol-grid {{ display: grid; grid-template-columns: 0.82fr 1.18fr; gap: clamp(2rem, 5vw, 5rem); padding-block: clamp(4rem, 10vh, 7.5rem); align-items: start; }}
    .sol.rev .sol-rail {{ order: 2; }}
    .sol-rail {{ position: sticky; top: 108px; }}
    .sol-num {{ font-size: 0.85rem; font-weight: 600; letter-spacing: 0.15em; color: var(--violet); }}
    .sol-name {{ font-family: "Hanken Grotesk", var(--font); font-weight: 200; font-size: clamp(2.4rem, 4.6vw, 4rem); line-height: 1; margin-top: 0.7rem; }}
    .badge {{ display: inline-flex; align-items: center; gap: 0.5rem; margin-top: 1.3rem; padding: 0.4rem 0.95rem; border-radius: 999px; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.02em; border: 1px solid transparent; }}
    .badge::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; }}
    .badge.live {{ color: var(--gold); border-color: rgba(217,168,106,0.4); background: rgba(217,168,106,0.08); }}
    .badge.live::before {{ background: var(--gold); box-shadow: 0 0 8px var(--gold); }}
    .badge.build {{ color: var(--violet-lo); border-color: rgba(168,158,241,0.4); background: rgba(168,158,241,0.08); }}
    .badge.build::before {{ background: var(--violet-lo); }}
    .sol-cta {{ display: flex; align-items: center; gap: 0.6rem; margin-top: 1.8rem; text-decoration: none; font-weight: 600; color: var(--paper); width: fit-content; }}
    .sol-cta svg {{ transition: transform 0.25s var(--ease); }}
    .sol-cta:hover svg {{ transform: translateX(6px); }}
    .sol-media {{ margin: 0; border-radius: 18px; overflow: clip; aspect-ratio: 16 / 10; box-shadow: 0 30px 90px rgba(0,0,0,0.5); }}
    .sol-media img {{ width: 100%; height: 100%; object-fit: cover; }}
    .sol-tag {{ margin-top: 1.6rem; font-family: var(--serif); font-style: italic; font-weight: 300; font-size: clamp(1.3rem, 2.4vw, 1.9rem); color: var(--violet-lo); }}
    .sol-desc {{ margin-top: 1rem; color: rgba(241,240,246,0.76); font-size: 1.06rem; line-height: 1.7; max-width: 60ch; }}
    .pills {{ list-style: none; margin: 1.8rem 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 0.55rem; }}
    .pills li {{ padding: 0.5rem 0.95rem; border: 1px solid var(--line-dk); border-radius: 10px; font-size: 0.88rem; color: rgba(241,240,246,0.82); background: rgba(255,255,255,0.02); }}
    .rel-svc {{ display: inline-flex; align-items: center; gap: 0.5rem; margin-top: 1.6rem; text-decoration: none; font-size: 0.92rem; color: var(--violet-lo); }}
    .rel-svc svg {{ transition: transform 0.25s var(--ease); }}
    .rel-svc:hover svg {{ transform: translateX(5px); }}
    @media (max-width: 900px) {{
      .sol-grid {{ grid-template-columns: 1fr; gap: 1.8rem; }}
      .sol.rev .sol-rail {{ order: 0; }}
      .sol-rail {{ position: static; }}
    }}

    /* Standard */
    .standard {{ border-top: 1px solid var(--line-dk); padding-block: clamp(4.5rem, 11vh, 8rem); }}
    .standard .head {{ max-width: 30ch; }}
    .standard h2 {{ font-family: "Hanken Grotesk", var(--font); font-weight: 200; font-size: clamp(2.4rem, 5vw, 4rem); line-height: 1; }}
    .standard .head p {{ margin-top: 1rem; color: var(--cream-dim); font-size: 1.1rem; }}
    .std-grid {{ margin-top: 3rem; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: var(--line-dk); border: 1px solid var(--line-dk); border-radius: 16px; overflow: clip; }}
    .std {{ background: var(--black); padding: clamp(1.6rem, 3vw, 2.4rem); }}
    .std h3 {{ font-size: 1.2rem; font-weight: 600; }}
    .std h3::before {{ content: ""; display: block; width: 34px; height: 2px; background: var(--gold); margin-bottom: 1rem; }}
    .std p {{ margin-top: 0.7rem; color: var(--cream-dim); font-size: 0.97rem; line-height: 1.6; }}
    @media (max-width: 820px) {{ .std-grid {{ grid-template-columns: 1fr; }} }}

    /* Clients */
    .clients {{ border-top: 1px solid var(--line-dk); padding-block: clamp(3.5rem, 8vh, 5.5rem); text-align: center; }}
    .clients .eyebrow {{ color: var(--cream-dim); }}
    .logo-row {{ margin-top: 2rem; display: flex; justify-content: center; align-items: center; gap: clamp(2.5rem, 7vw, 5.5rem); flex-wrap: wrap; opacity: 0.85; }}
    .logo-row img {{ height: 26px; }}
    .logo-row .word {{ font-size: 1.35rem; font-weight: 700; letter-spacing: 0.02em; }}

    /* CTA */
    .cta {{ border-top: 1px solid var(--line-dk); padding-block: clamp(5rem, 13vh, 9rem); text-align: center; }}
    .cta h2 {{ font-family: var(--serif); font-style: italic; font-weight: 300; font-size: clamp(2.2rem, 5.5vw, 4rem); line-height: 1.12; max-width: 20ch; margin: 0 auto; }}
    .cta h2 b {{ font-style: normal; font-weight: 300; color: var(--violet-lo); }}
    .cta .btn {{ display: inline-block; margin-top: 2.4rem; background: var(--paper); color: var(--ink); text-decoration: none; padding: 1.05rem 2.4rem; border-radius: 999px; font-weight: 600; transition: background 0.2s, transform 0.15s var(--ease); }}
    .cta .btn:hover {{ background: var(--violet-lo); }}
    .cta small {{ display: block; margin-top: 1.3rem; color: var(--cream-dim); font-size: 0.92rem; }}

    /* Footer */
    footer {{ background: var(--ink-deep); border-top: 1px solid var(--line-dk); padding-block: 3rem 2.2rem; }}
    .foot {{ display: flex; justify-content: space-between; gap: 2.5rem; flex-wrap: wrap; }}
    .foot img {{ height: 32px; }}
    .foot .cols {{ display: flex; gap: 3.5rem; flex-wrap: wrap; }}
    .foot a {{ display: block; color: var(--cream-dim); text-decoration: none; font-size: 0.93rem; line-height: 2.1; }}
    .foot a:hover {{ color: var(--paper); }}
    .foot .t {{ color: var(--paper); font-weight: 600; margin-bottom: 0.3rem; font-size: 0.9rem; }}
    .foot-base {{ margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--line-dk); display: flex; justify-content: space-between; gap: 1rem; flex-wrap: wrap; color: var(--ink-soft); font-size: 0.85rem; }}

    @supports (animation-timeline: view()) {{
      @media (prefers-reduced-motion: no-preference) {{
        .sol-main > *, .std, .chips {{ animation: rise 1ms both; animation-timeline: view(); animation-range: entry 4% cover 30%; }}
      }}
    }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(30px); }} }}
    /* Guard: keep the vh-based hero sane on very tall viewports (headless capture). */
    @media (min-height: 1400px) {{ .hero {{ min-height: 840px; }} }}
  </style>
</head>
<body id="top">
  <nav class="nav" aria-label="Main">
    <div class="wrap">
      <a class="brand" href="../"><img src="../assets/logo-wordmark.png" alt="Prism Automate" width="115" height="30" /></a>
      <ul class="nav-links">
        <li><a href="../">Home</a></li>
        <li><a href="../services/">Services</a></li>
        <li><a href="#top" class="active">Solutions</a></li>
        <li><a href="../#work">Work</a></li>
        <li><a href="../#faq">FAQ</a></li>
      </ul>
      <a class="nav-cta" href="../#contact">Start a project</a>
    </div>
  </nav>

  <header class="hero">
    <div class="hero-bg"><video src="../assets/ring-b.webm" autoplay muted loop playsinline preload="auto" aria-hidden="true"></video></div>
    <div class="wrap">
      <p class="eyebrow">Solutions</p>
      <h1>AI solutions, built to <em>ship</em>.</h1>
      <p class="lede">Two products already live in the field, and four more we build on Claude for teams across India, the GCC, and Australia. Every one designed to reach production, not the demo shelf.</p>
      <nav class="chips" aria-label="Jump to a solution">
{chips}
      </nav>
    </div>
  </header>

{sections}

  <section class="standard">
    <div class="wrap">
      <div class="head">
        <h2>The Prism standard</h2>
        <p>What every solution on this page has in common.</p>
      </div>
      <div class="std-grid">
{standards}
      </div>
    </div>
  </section>

  <section class="clients">
    <div class="wrap">
      <p class="eyebrow">Delivered for teams at</p>
      <div class="logo-row">
        <img src="https://cdn.simpleicons.org/google/f1f0f6" alt="Google" loading="lazy" />
        <span class="word">UNISYS</span>
        <img src="https://cdn.simpleicons.org/anthropic/f1f0f6" alt="Anthropic" loading="lazy" />
      </div>
    </div>
  </section>

  <section class="cta">
    <div class="wrap">
      <h2>Have a workflow that should be a <b>solution</b>?</h2>
      <a class="btn" href="../#contact">Start a project</a>
      <small>A real person replies within one business day. Bengaluru · Dubai · Sydney.</small>
    </div>
  </section>

  <footer>
    <div class="wrap">
      <div class="foot">
        <a class="brand" href="../"><img src="../assets/logo-wordmark.png" alt="Prism Automate" width="115" height="30" /></a>
        <div class="cols">
          <div>
            <span class="t">Explore</span>
            <a href="../">Home</a>
            <a href="../services/">All services</a>
            <a href="#top">Solutions</a>
          </div>
          <div>
            <span class="t">Company</span>
            <a href="../#story">Our story</a>
            <a href="../#work">Work</a>
            <a href="../#contact">Contact</a>
          </div>
          <div>
            <span class="t">Partners</span>
            <a href="https://www.anthropic.com" target="_blank" rel="noopener">Anthropic · Claude</a>
            <a href="https://prismscale.com" target="_blank" rel="noopener">Prismscale</a>
            <a href="https://www.designhq.io" target="_blank" rel="noopener">DesignHQ</a>
          </div>
        </div>
      </div>
      <div class="foot-base">
        <span>Prism Automate © 2026 · Anthropic Claude Partner</span>
        <span>Bengaluru · Dubai · Sydney</span>
      </div>
    </div>
  </footer>

  <script src="../assets/vendor/gsap.min.js"></script>
  <script src="../assets/vendor/ScrollTrigger.min.js"></script>
  <script src="../assets/lenis.min.js"></script>
  <script>
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Nav solid after hero.
    const nav = document.querySelector('.nav');
    const sentinel = document.createElement('div');
    Object.assign(sentinel.style, {{ position: 'absolute', top: '0', height: '80vh', width: '1px', pointerEvents: 'none' }});
    document.body.appendChild(sentinel);
    new IntersectionObserver(([e]) => nav.classList.toggle('is-solid', !e.isIntersecting)).observe(sentinel);

    if (reduce || typeof gsap === 'undefined' || typeof Lenis === 'undefined') {{
      document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {{
        const t = document.querySelector(a.getAttribute('href')); if (!t) return;
        e.preventDefault(); t.scrollIntoView({{ behavior: reduce ? 'auto' : 'smooth' }});
      }}));
    }} else {{
      gsap.registerPlugin(ScrollTrigger);
      document.documentElement.classList.add('inertia-scroll');
      const lenis = window.__lenis = new Lenis({{ duration: 1.2, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), smoothWheel: true, touchMultiplier: 2 }});
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(t => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
      document.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', e => {{
        const id = a.getAttribute('href'); const t = document.querySelector(id);
        if (!t) return; e.preventDefault(); lenis.scrollTo(t, {{ offset: id === '#top' ? -200 : -80, duration: 1.2 }});
      }}));
      // Subtle parallax on each solution image.
      gsap.utils.toArray('.sol-media img').forEach(img => {{
        gsap.fromTo(img, {{ yPercent: -6 }}, {{ yPercent: 6, ease: 'none', scrollTrigger: {{ trigger: img.closest('.sol-media'), start: 'top bottom', end: 'bottom top', scrub: 0.8 }} }});
      }});
    }}
  </script>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(PAGE)
print("wrote", OUT, "-", len(SOL), "solutions,", len(PAGE), "bytes")
