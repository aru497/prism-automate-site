# Prism Automate / Prism Events

## What this is
Redesigned company site (SEO funnel) for **Prism Automate**, replacing the old Framer
template at intelligent-customers-109307.framer.app. The company brand and logo stay
Prism Automate; the site sells its flagship product, **Prism Events**. Part of the Prism
partner network (prismscale.com, designhq.io).

## The offering
Anthropic Claude partner with a 14-service catalogue in four groups: Strategy &
Advisory, Build & Engineering, Implementation & Deployment, Ongoing & Managed
Services (shown as pill lists in the solutions bento; mirrored in JSON-LD
hasOfferCatalog).

Shipped solutions featured in "Built, shipped, and running live":
- **Prism Events**: Virtual Positioning System for events. Turn-by-turn indoor
  navigation, booth/session discovery, crowd-flow analytics, Claude concierge.
- **Virtual try-on for retail**: browser-based apparel try-on module, developed
  and executed for production e-commerce.

## Audience
Event organizers, venue operations teams, corporate event producers. Enterprise B2B.
Proof points: work delivered for Google and Unisys.

## Register
brand (landing page; design IS the product)

## Voice
Precise, confident, operational. Three brand-voice words: calibrated, wayfinding, assured.

## Visual language
Preserved from the original Framer site (Bima template), per client request:
deep navy-ink base (#030212), Plus Jakarta Sans, lavender (#a89ef1) highlight
words in headings, violet-to-gold gradient hero words, glassy pill buttons
(white primary, dark glossy secondary), corner-bracket floating pain cards,
light-beam hero overlay (assets/ring-hero.png from the Framer CDN), and a
watermark footer with the glowing ring mark. Brand lockup: recreated
segmented-ring SVG + stacked two-line wordmark (lavender/gold).
Cartographic motifs kept in the Prism Events spotlight: floor-plan map, routes,
positioning markers. Radius system: cards 20px, interactive pills.
Hero + footer use the original site's glassy 3D ring WEBM videos (assets/ring-b.webm,
ring-a.webm) with mix-blend screen + radial edge masks. "Is this you?" pins and pops
each question on scroll (named view-timeline, 300vh). Tech-stack section: fanned card
deck (Python, LangChain, Claude, Zapier, Airtable). Smooth scrolling: vendored Lenis.
Scroll reveals are pure CSS (animation-timeline: view()) so content is never gated
on JS (crawler/headless safe). Static HTML/CSS/JS, no build step.

## Funnel goal
Primary CTA everywhere: "Book a demo" (contact form at #contact).
Secondary: anchor to how-it-works. FAQ carries FAQPage JSON-LD for AEO.

## Placeholders to confirm with the client
- Final domain (canonical URLs, sitemap use https://prismevents.example placeholder)
- Contact form backend / email
- Real metrics for the results band
- Real client quote (current one is marked placeholder)
