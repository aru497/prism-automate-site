# DESIGN.md: webandcrafts.com (WAC)

## Source
- URL: https://webandcrafts.com
- Capture date: 2026-07-12
- Evidence: Firecrawl branding format + full-page screenshot (1920x17752, `.firecrawl/wac-screenshot.png`) + page markdown

## Reference Screenshot
![Full-page screenshot of webandcrafts.com](./.firecrawl/wac-screenshot.png)

## Design Summary
Cinematic black-canvas agency site. Full-bleed video hero with a large, LIGHT-weight
grotesque headline anchored bottom-left and a small arrow-link CTA. A manifesto
statement whose words brighten from gray to white as you scroll. Service pillars as
massive ultra-thin display words (one per viewport: "Design", "Build", "Market") with
a short paragraph beneath. Case studies as large photo cards with category kicker +
long descriptive title. Stats band (700+, 600+ ...). White client logos on black.
Electric cobalt (#013BFF) reserved for links/primary actions. Generous, slow vertical
rhythm; everything breathes.

## Design Tokens

### Colors
- background: #000000 (true black; observed)
- text-primary: #FFFFFF; text-dim: rgba(255,255,255,0.55) (observed)
- accent (links/CTA): #013BFF / #013AD6 electric cobalt (observed)
- button-primary: white bg, #141414 text (observed)
- borders/hairlines: rgba(255,255,255,0.14) (inferred)

### Typography
- Family: custom grotesque (Graphik/Aeonik-class, self-hosted; hashed name in CSS).
  Substitute: "Hanken Grotesk" (Google) with light weights. (inferred substitute)
- Hero headline: ~56-64px, weight 300-400, line-height ~1.15, sentence case + period.
- Pillar display words: ~140-170px, weight 200 (ultra-light), white on black.
- Section h2: ~60px (observed h2=60px), weight 500-600.
- Body: 16px, weight 400, dim white.
- Case-study titles: ~22-26px semi-bold, long descriptive sentences.

### Spacing And Layout
- Full-width canvas, content max ~1280-1400px, generous 120-200px section padding.
- Pillar sections ≈ 100vh each. Radius: small (6px) on cards; buttons pill or square-ish.
- Case-study grid: 2-col large image cards, image ~16:10, kicker + title below.

## Components
- Nav: transparent over hero, small wordmark left, plain links, Contact button right.
- Arrow link CTA: small text + right-arrow glyph, white; hover shifts arrow.
- Primary button: white pill, dark text. Accent button: cobalt bg, white text.
- Stats: huge numeral + 2-line label, 4-across.
- Logo wall: white SVG logos on black grid.
- Big footer CTA: "Get started now! It takes less than a minute." + Request a quote.
- Mega footer: 4 link columns + contact numbers + social icons.

## Page Patterns
Video hero (headline bottom-left) → manifesto scrub → pillar words (Design/Build/
Market, one per viewport) → case studies → stats → what-we-do image cards → Gen-AI CTA
→ client logos → testimonials → careers strip → insights → footer CTA → mega footer.

## Content Style
Short punchy fragments with periods ("Experiences Powered by Intelligence.").
Case-study titles are long and concrete ("Caribou: Helping a reputed coffee chain go
digital..."). Honest big stats. Warm, confident, minimal adjectives.

## Agent Build Instructions
1. True-black page, white text, ONE accent (#013BFF) for links/buttons only.
2. Hanken Grotesk: 200 for display words, 300-400 for hero, 400 body, 600 titles.
3. Hero: full-bleed dark media, headline bottom-left, arrow CTA under it.
4. Manifesto: two-layer text; white layer clip-path widens on scroll (animation-timeline).
5. Three ~100vh pillar sections with 9-11rem weight-200 words + 40ch paragraph.
6. Case studies: 2 big photo cards, category kicker, long descriptive titles.
7. Stats band with real numbers; white logo wall; white-pill and cobalt CTAs.
8. Slow rhythm: 8-12rem section padding. No glassmorphism, no gradients on text.

## Rerun Inputs
workflow: firecrawl-website-design-clone
source_url: https://webandcrafts.com
target_stack: static HTML/CSS/JS (zero-dep)
output: DESIGN.md
