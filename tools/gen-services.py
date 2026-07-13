#!/usr/bin/env python3
"""Generate one page per Claude service under site/studio/services/<slug>/index.html.
Content sourced from the recognised 14-service catalogue; design = studio identity."""
import os, html

BASE = "/Users/arunkumar/Documents/Claude/Projects/PrismEvents/site/studio/services"

CATS = {
    "strategy": "Strategy & Advisory",
    "build": "Build & Engineering",
    "deploy": "Implementation & Deployment",
    "run": "Ongoing & Managed Services",
}

S = [
 dict(slug="ai-strategy-roadmap", cat="strategy", name="AI Strategy & Roadmap",
  definition="A paid engagement that scopes your whole Claude program: where AI earns its keep, what ships first, and in what order.",
  included=[
    ("Priorities and sequencing", "A ranked program: which workflows to automate first and why, with dependencies mapped."),
    ("Model and platform choices", "Where Claude fits, which tier, and how it sits alongside the systems you already run."),
    ("A defensible roadmap", "Quarter-by-quarter plan your board can read, with costs and owners against every step."),
  ],
  steps=[("Listen", "Workshops with the people who own the workflows, not just the org chart."),
         ("Map", "Every candidate use case scored for value, effort, and risk."),
         ("Commit", "A sequenced roadmap with the first build scoped to start immediately.")],
  fit=["You know AI matters but the path from here to there is fog.",
       "Different teams are running uncoordinated AI experiments.",
       "The board wants a plan with numbers, not enthusiasm."]),

 dict(slug="ai-readiness-governance", cat="strategy", name="AI Readiness & Governance Assessment",
  definition="A paid assessment of your readiness, governance, and risk posture for adopting Claude across the organisation.",
  included=[
    ("Readiness scorecard", "Data, security, skills, and process maturity, measured against what adoption actually needs."),
    ("Governance framework", "Usage policies, review gates, and escalation paths that satisfy legal without strangling teams."),
    ("Risk register", "The failure modes that matter for your industry, each with a mitigation owner."),
  ],
  steps=[("Audit", "Interviews and systems review across security, data, and the teams who'll use AI daily."),
         ("Assess", "Findings scored against adoption-readiness criteria proven on real rollouts."),
         ("Equip", "Policies, gates, and a remediation plan you can hand to compliance.")],
  fit=["Legal or security keeps pausing your AI initiatives.",
       "You operate in a regulated industry and need the paper trail.",
       "Adoption is growing bottom-up with no guardrails."]),

 dict(slug="use-case-portfolio", cat="strategy", name="Use-Case Portfolio & Business Case",
  definition="A paid engagement that prioritises your Claude use cases and builds the business case behind each one.",
  included=[
    ("Use-case inventory", "Every candidate captured from the floor up, not invented in a slide deck."),
    ("Value modelling", "Hours saved, revenue protected, and cost avoided, quantified per use case."),
    ("Investment case", "A portfolio view finance can approve: quick wins funding the deeper builds."),
  ],
  steps=[("Harvest", "Shadow the teams and collect where hours actually go."),
         ("Model", "Attach honest numbers to each candidate, with assumptions written down."),
         ("Rank", "A portfolio ordered by return, ready to fund.")],
  fit=["You have twenty AI ideas and budget for three.",
       "Finance wants proof before the program grows.",
       "You need quick wins that pay for the long game."]),

 dict(slug="internal-agentic-platform", cat="build", name="Internal Agentic Platform Build",
  definition="We build your internal agentic platform or framework with Claude as the core model: the foundation every team builds on.",
  included=[
    ("Platform architecture", "Agent orchestration, tool access, memory, and guardrails designed for your stack."),
    ("Connectors that matter", "Your CRM, ERP, help desk, and data warehouse wired in with proper auth."),
    ("Paved-road templates", "Patterns your own developers reuse, so agent two ships faster than agent one."),
  ],
  steps=[("Design", "Architecture sized to your workloads, security model first."),
         ("Build", "The platform core plus your first production agent, shipped together."),
         ("Enable", "Your engineers onboarded; the platform becomes theirs.")],
  fit=["Multiple teams want agents and each is reinventing plumbing.",
       "Security demands one governed gateway to the model.",
       "You want AI capability in-house, not rented forever."]),

 dict(slug="customer-facing-ai-product", cat="build", name="Customer-Facing AI Product Build",
  definition="We build Claude into your external-facing product or service, from concierge experiences to entirely new AI features.",
  included=[
    ("Product-grade AI UX", "Latency, streaming, fallbacks, and tone handled so it feels like product, not demo."),
    ("Safety for strangers", "Prompt-injection defence, content filtering, and rate controls for the open internet."),
    ("Analytics loop", "Usage instrumented from day one so the feature earns its roadmap slot."),
  ],
  steps=[("Shape", "The feature scoped around one user job, with quality bars set."),
         ("Ship", "Production build behind flags, tested against adversarial inputs."),
         ("Sharpen", "Post-launch tuning against real conversations.")],
  fit=["Your customers are asking where your AI features are.",
       "A competitor just shipped theirs.",
       "You have the product team but not the applied-AI depth."]),

 dict(slug="prototype-poc", cat="build", name="Prototype & Proof of Concept",
  definition="A contracted prototype or proof of concept delivered against a defined use case, so decisions get made on evidence.",
  included=[
    ("A working system", "Real integration against your data, not a slideware mock."),
    ("Honest findings", "What worked, what didn't, and what production would actually cost."),
    ("A go/no-go you can trust", "Evidence strong enough to kill the idea or fund it properly."),
  ],
  steps=[("Frame", "One use case, one success metric, agreed up front."),
         ("Prove", "Two to four weeks of focused build against real inputs."),
         ("Decide", "Demo, findings, and a costed path to production.")],
  fit=["Stakeholders disagree about whether AI can do the job.",
       "You need evidence before a bigger budget unlocks.",
       "The use case is novel enough that nobody can quote it blind."]),

 dict(slug="rollout-activation", cat="deploy", name="Rollout & Activation",
  definition="SSO and tenant setup, seat provisioning, champion training, and go-live support: adoption treated as a project, not an email.",
  included=[
    ("Tenant done right", "SSO, workspace structure, and permissions matched to how your org actually works."),
    ("Champions programme", "Power users trained first, so help lives inside every team."),
    ("Go-live support", "We sit with you through launch week and the wobbles after it."),
  ],
  steps=[("Prepare", "Tenant, security review, and seat plan signed off."),
         ("Activate", "Staged rollout by team, champions ahead of each wave."),
         ("Embed", "Usage reviewed at 30 days; laggard teams get direct help.")],
  fit=["You bought the licences and adoption is stuck at 20%.",
       "IT wants a controlled rollout, not a free-for-all.",
       "You want employees using AI safely by next quarter."]),

 dict(slug="industry-accelerator-deployment", cat="deploy", name="Industry Solution Accelerator Deployment",
  definition="A pre-built, industry-specific Claude accelerator deployed into your environment, so you start weeks ahead instead of from zero.",
  included=[
    ("Accelerator fit-out", "The pre-built solution configured to your data, workflows, and brand."),
    ("Environment integration", "Deployed inside your cloud and security perimeter, not ours."),
    ("Handover with keys", "Your team owns and operates it; we document everything."),
  ],
  steps=[("Select", "The right accelerator matched to your industry problem."),
         ("Adapt", "Configuration and integration sprint in your environment."),
         ("Launch", "Production cutover with your operators trained.")],
  fit=["Your problem is common in your industry; no need to build bespoke.",
       "Time-to-value matters more than owning every design choice.",
       "Procurement prefers configured products over custom builds."]),

 dict(slug="platform-migration-claude", cat="deploy", name="Platform Migration to Claude",
  definition="Contracted migration of a workload from another model or provider onto Claude, without breaking what already works.",
  included=[
    ("Prompt & eval translation", "Your prompts, chains, and eval suites rebuilt for Claude's strengths."),
    ("Side-by-side proof", "Old and new run in parallel until the numbers say switch."),
    ("Zero-drama cutover", "Staged traffic shift with rollback ready at every step."),
  ],
  steps=[("Baseline", "Current behaviour measured so 'as good or better' is provable."),
         ("Port", "Prompts, tools, and guardrails migrated and tuned."),
         ("Cutover", "Traffic shifts gradually; the old path retires only when beaten.")],
  fit=["Your current provider's costs or limits stopped making sense.",
       "You want Claude's reasoning on a workload built elsewhere.",
       "Compliance needs the switch handled contractually, with evidence."]),

 dict(slug="sustained-adoption-coe", cat="run", name="Sustained Adoption & CoE Program",
  definition="We run your AI Centre of Excellence: driving usage, enablement, and governance long after the launch excitement fades.",
  included=[
    ("CoE operating rhythm", "Intake, prioritisation, and review cycles that keep the pipeline moving."),
    ("Enablement calendar", "Training, office hours, and internal showcases that keep skills compounding."),
    ("Governance in motion", "Policies enforced and updated as usage and models evolve."),
  ],
  steps=[("Stand up", "CoE structure, roles, and intake defined with your leads."),
         ("Operate", "We run the rhythm with you, quarter by quarter."),
         ("Transfer", "Your people take the chairs as capability matures.")],
  fit=["Adoption spiked at launch and slid back within months.",
       "AI requests arrive everywhere and nowhere; nobody triages.",
       "Leadership wants sustained capability, not a one-off project."]),

 dict(slug="managed-ai-operations", cat="run", name="Managed AI Operations",
  definition="Your Claude workloads operated in production as a managed service: run, monitoring, and SLAs owned by us.",
  included=[
    ("24/7-grade operations", "Monitoring, alerting, and incident response with agreed SLAs."),
    ("Quality watch", "Output drift and regression caught by evals before users notice."),
    ("Monthly ops review", "Usage, cost, incidents, and improvements in one honest report."),
  ],
  steps=[("Onboard", "Runbooks, dashboards, and alert thresholds stood up."),
         ("Operate", "We carry the pager; you get the report."),
         ("Improve", "Every incident becomes a hardening item, tracked to done.")],
  fit=["The workload matters but ops isn't your core business.",
       "You need SLAs a vendor actually signs.",
       "Your team built it and shouldn't be stuck running it."]),

 dict(slug="cowork-claude-code-support", cat="run", name="Cowork & Claude Code Support",
  definition="Ongoing tier-1/2 support and enablement for your Cowork or Claude Code user base, so builders never stall.",
  included=[
    ("Named support channel", "Real answers on Slack or Teams, with response-time commitments."),
    ("Patterns library", "Working examples for your stack, curated and kept current."),
    ("Usage clinics", "Regular sessions turning stuck users into power users."),
  ],
  steps=[("Baseline", "Where your builders are strong and where they stall."),
         ("Support", "Tier-1/2 questions handled; escalations owned to resolution."),
         ("Level up", "Clinic themes driven by the actual ticket log.")],
  fit=["Developers adopted Claude Code unevenly and momentum is patchy.",
       "Internal IT can't answer model-specific questions.",
       "You want enablement running without hiring for it."]),

 dict(slug="claude-finops-optimisation", cat="run", name="Claude Consumption & FinOps Optimisation",
  definition="Ongoing cost and consumption optimisation: model selection, caching, and rightsizing, so the bill grows slower than the value.",
  included=[
    ("Consumption map", "Who spends what, on which workloads, and which spend earns nothing."),
    ("Optimisation levers", "Model-tier fits, prompt caching, batching, and context diets applied where safe."),
    ("Guardrails on spend", "Budgets, alerts, and per-team limits before the surprise invoice."),
  ],
  steps=[("Measure", "Full consumption baseline across teams and workloads."),
         ("Optimise", "Levers applied in order of savings-to-risk."),
         ("Hold", "Monthly reviews keep efficiency from decaying.")],
  fit=["The Claude invoice doubled and nobody can say exactly why.",
       "Different teams pay different effective rates for the same work.",
       "Finance wants a forecast that survives contact with reality."]),

 dict(slug="claude-training-sessions", cat="run", name="Claude Training Sessions",
  definition="Structured training on Claude, Claude Code, or Cowork, delivered as a defined curriculum with clear learning outcomes.",
  included=[
    ("Role-based curriculum", "Different tracks for builders, analysts, and leaders; nobody sits through the wrong course."),
    ("Hands-on by design", "Exercises on your real workflows, not toy prompts."),
    ("Measured outcomes", "Pre/post assessment so the training's effect is visible."),
  ],
  steps=[("Tailor", "Curriculum shaped to your tools, data, and policies."),
         ("Teach", "Live cohorts, capped size, everything hands-on."),
         ("Certify", "Assessment, materials, and a refresher path.")],
  fit=["Licences are live but usage is shallow and repetitive.",
       "New joiners need a consistent AI onboarding.",
       "You'd rather grow skills than rent them indefinitely."]),
]

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
  <meta name="robots" content="noindex" />
  <!-- Service page in the studio design direction. noindex until a primary design
       is chosen; flip to index + add canonical when the domain goes live. -->
  <link rel="icon" type="image/png" href="../../../assets/favicon.png" />
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
        "areaServed": ["India", "United Arab Emirates", "Australia"]
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{ "@type": "ListItem", "position": 1, "name": "Prism Automate", "item": "../../" }},
          {{ "@type": "ListItem", "position": 2, "name": "{cat_name}" }},
          {{ "@type": "ListItem", "position": 3, "name": "{name}" }}
        ]
      }}
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
    .nav a.back {{ margin-left: auto; text-decoration: none; opacity: 0.75; font-size: 0.93rem; }}
    .nav a.back:hover {{ opacity: 1; }}
    .nav-cta {{ border: 1px solid currentColor; border-radius: 999px; padding: 0.5rem 1.25rem; text-decoration: none; font-size: 0.9rem; font-weight: 600; }}
    .nav-cta:hover {{ background: var(--paper); color: var(--ink); }}
    .hero {{ background: #050408; color: var(--paper); padding: 170px 0 clamp(4rem, 10vh, 6.5rem); }}
    .hero .eyebrow {{ color: var(--violet-lo); }}
    .hero h1 {{ font-family: "Hanken Grotesk", var(--font); font-weight: 200; font-size: clamp(2.6rem, 6.4vw, 5.2rem); line-height: 1.02; margin-top: 1.1rem; max-width: 15ch; }}
    .hero .lede {{ margin-top: 1.5rem; color: var(--cream-dim); font-size: clamp(1.05rem, 1.7vw, 1.25rem); max-width: 46ch; }}
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
    .btn-solid {{ background: var(--paper); color: var(--ink); text-decoration: none; padding: 1rem 2.2rem; border-radius: 999px; font-weight: 600; white-space: nowrap; }}
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
      .nav a.back {{ display: none; }}
      .nav .nav-cta {{ margin-left: auto; }}
    }}
  </style>
</head>
<body>
  <nav class="nav" aria-label="Main">
    <div class="wrap">
      <a class="brand" href="../../">Prism<b>Automate</b></a>
      <a class="back" href="../../">← All services</a>
      <a class="nav-cta" href="../../../#contact">Start a project</a>
    </div>
  </nav>

  <header class="hero">
    <div class="wrap">
      <p class="eyebrow">{cat_name}</p>
      <h1>{name}</h1>
      <p class="lede">{definition}</p>
      <a class="arrow-link" href="../../../#contact">Scope this with us
        <svg width="22" height="12" viewBox="0 0 24 12" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M0 6h22M17 1l5 5-5 5"/></svg>
      </a>
    </div>
  </header>

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

  <section class="cta">
    <div class="wrap">
      <div>
        <h2>Let's scope <em>{name_lower}</em> for your team.</h2>
        <small>A real person replies within one business day. Bengaluru · Dubai · Sydney.</small>
      </div>
      <a class="btn-solid" href="../../../#contact">Start a project</a>
    </div>
  </section>

  <footer>
    <div class="wrap">
      <span>Prism Automate © 2026 · Anthropic Claude Partner</span>
      <span><a href="../../" style="color:inherit">Studio</a> · <a href="../../../" style="color:inherit">Main site</a></span>
    </div>
  </footer>
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
    meta = svc["definition"] + " Delivered by Prism Automate, an Anthropic Claude partner serving India, the Middle East, and Australia."
    page = PAGE.format(
        name=esc(svc["name"]), name_lower=esc(svc["name"][0].lower() + svc["name"][1:]),
        cat_name=esc(CATS[svc["cat"]]), definition=esc(svc["definition"]),
        meta_desc=esc(meta.replace('"', "'")),
        included_html=inc, steps_html=steps, fit_html=fit, related_html=related(svc))
    outdir = os.path.join(BASE, svc["slug"])
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w").write(page)
    print("wrote", svc["slug"])

print(f"\n{len(S)} service pages generated")
