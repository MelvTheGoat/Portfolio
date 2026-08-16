# Generates the static site from the templates + content below.
# Run: python3 build.py
# Output: sibling HTML files, ready to deploy as-is (no build step needed
# after this — the generator is a convenience for editing, not a dependency
# of the deployed site).

import os

ROOT = os.path.dirname(os.path.abspath(__file__))

NAME = "Mayungbo Oluwatobi Melvyn"
EMAIL = "mlvyn.t@gmail.com"
LINKEDIN = "https://linkedin.com/in/oluwatobi-mayungbo-3a567026b"
GITHUB_PROFILE = "https://github.com/MelvTheGoat"
LOCATION = "Lagos, Nigeria"
RAG_LIVE_URL = "https://nigerian-fintech-regulation-assistant-474115007874.europe-west1.run.app"

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&'
    'family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'
)

NAV_ITEMS = [
    ("Home", "/index.html", "home"),
    ("Projects", "/projects.html", "projects"),
    ("Writing", "/writing.html", "writing"),
    ("About", "/about.html", "about"),
    ("Resume", "/resume.html", "resume"),
    ("Contact", "/contact.html", "contact"),
]


def nav(active, depth=""):
    items = []
    for label, href, key in NAV_ITEMS:
        h = (depth + href.lstrip("/"))
        current = ' aria-current="page"' if key == active else ""
        items.append(f'<li><a href="{h}"{current}>{label}</a></li>')
    return "\n        ".join(items)


def head(title, desc, depth=""):
    return f"""<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  {FONT_LINK}
  <link rel="stylesheet" href="{depth}css/style.css">
"""


def header(active, depth=""):
    return f"""  <nav class="site-nav">
    <div class="wrap">
      <a class="brand" href="{depth}index.html">{NAME.split()[0]}<span class="dot">.</span>ml</a>
      <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span></span>
      </button>
      <ul class="nav-links">
        {nav(active, depth)}
      </ul>
    </div>
  </nav>
"""


def footer(depth=""):
    return f"""  <footer>
    <div class="wrap">
      <span class="copy">&copy; 2026 {NAME} &mdash; built with calibration in mind.</span>
      <div class="foot-links">
        <a href="mailto:{EMAIL}">Email</a>
        <a href="{GITHUB_PROFILE}" target="_blank" rel="noopener">GitHub</a>
        <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </div>
  </footer>
  <script src="{depth}js/main.js"></script>
"""


def page(title, desc, active, body, depth=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(title, desc, depth)}</head>
<body>
{header(active, depth)}
{body}
{footer(depth)}
</body>
</html>
"""


def reading(label, value, unit="", small=False):
    cls = "reading sm" if small else "reading"
    unit_html = f'<span class="unit">{unit}</span>' if unit else ""
    return f"""<div class="{cls}">
              <span class="r-label">{label}</span>
              <span class="r-value">{value}{unit_html}</span>
              <span class="r-axis"></span>
            </div>"""


# ---------------------------------------------------------------------------
# Project data — every number here is from the CV / conversation record.
# GITHUB fields are marked [FILL] because exact per-project repo slugs
# were not confirmed — replace with the real URLs before publishing.
# ---------------------------------------------------------------------------

PROJECTS = [
    {
        "slug": "rag",
        "name": "Nigerian Fintech Compliance RAG Assistant",
        "short": "A regulatory Q&A system over CBN circulars and the NDPA — hybrid retrieval, citation verification, and a refusal mechanism engineered as a first-class feature. Deployed and live.",
        "tags": ["RAG", "LLM Evaluation", "Deployed", "GCP"],
        "status": "LIVE",
        "headline_label": "RECALL@5",
        "headline_value": "0.96",
        "headline_unit": "",
        "github": "https://github.com/MelvTheGoat/nigerian-fintech-compliance-rag",
        "live": RAG_LIVE_URL,
        "problem": (
            "Compliance officers and engineers at Nigerian fintechs were manually cross-referencing "
            "hundred-page CBN circulars and the NDPA to answer specific regulatory questions — a Tier "
            "1 KYC threshold, a breach-notification window — that should take seconds, not an afternoon "
            "of document search."
        ),
        "result": (
            "0.96 recall@5 and 0.842 MRR against a labelled 50-question golden set, with zero retrieval "
            "misses in the top 10. Deployed live on GCP Cloud Run within a ~225MB peak memory footprint."
        ),
        "flow": "ingest → section-aware chunk → hybrid index (BM25 + ONNX embeddings)\n  → reciprocal rank fusion → grounded generation → citation guardrail",
        "hardest_title": "Why reciprocal rank fusion, not naive score-blending",
        "hardest": (
            "BM25 scores are unbounded and can exceed 15 for a rare term; cosine similarities from a "
            "normalized embedder sit in a narrow 0.3&ndash;0.7 band. Adding them directly lets BM25 "
            "dominate every ranking purely because its numbers are bigger, not because it's more "
            "trustworthy. Min-max normalization looked like a fix but introduces its own problem: it's "
            "per-query, so one weak BM25 match on a thin-result query gets rescaled to a false 1.0. "
            "Reciprocal rank fusion keeps only each retriever's <em>rank</em>, discarding the raw score "
            "entirely &mdash; rank 1 means the same thing regardless of which retriever produced it, "
            "which sidesteps the scale mismatch instead of patching around it."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "The refusal-correctness metric came back at 0.40 in the offline evaluation &mdash; and "
            "tracing it down, the failure was in the <em>stub judge's</em> lexical-overlap heuristic, "
            "not the retrieval or guardrail logic: a question about Kenyan data-protection rules "
            "retrieved the NDPA's cross-border-transfer clause, which shares real vocabulary with the "
            "question purely by topical adjacency. That's a documented limitation of the offline stub, "
            "not a claim about the deployed system's real refusal rate &mdash; re-validating against a "
            "live provider is the explicit next step, not something papered over."
        ),
        "next": "Re-run the evaluation harness against a live provider instead of the offline stub, and expand the golden set with more adversarial and contradictory-source cases.",
        "stack": ["Python", "Streamlit", "BM25", "ONNX Runtime", "Reciprocal Rank Fusion", "FastAPI", "Docker", "GCP Cloud Run"],
    },
    {
        "slug": "fraud",
        "name": "Sequence-Based Transaction Fraud Detection",
        "short": "Three deep sequence architectures benchmarked against gradient boosting under an explicit cost model, with the sequence models' advantage isolated to robustness under drift specifically.",
        "tags": ["Deep Learning", "PyTorch", "Fraud", "Calibration"],
        "status": None,
        "headline_label": "P99 LATENCY",
        "headline_value": "5.1",
        "headline_unit": "ms",
        "github": "https://github.com/MelvTheGoat/sequence-fraud-detection",
        "live": None,
        "problem": (
            "Real-time transaction fraud detection needs to catch adaptive fraud patterns &mdash; card "
            "testing, account takeover, merchant compromise &mdash; while staying inside a strict "
            "latency budget and remaining honest about whether the added complexity of deep sequence "
            "models is actually earning its cost over a much simpler baseline."
        ),
        "result": (
            "Sequence models cut expected cost per transaction by 27% (0.0665 vs 0.0906) under an "
            "explicit cost model &mdash; but the margin came entirely from robustness to injected "
            "adversarial drift. Pre-drift, gradient boosting was marginally ahead (0.956 vs 0.950 "
            "PR-AUC). Served via ONNX Runtime at 5.1ms p99 end-to-end latency against a 50ms budget."
        ),
        "flow": "GRU / TCN / causal Transformer (<115k params each)\n  vs LightGBM baseline → focal loss / weighted sampling → temperature + isotonic calibration\n  → ONNX export → FastAPI serving",
        "hardest_title": "Why the honest pre-drift number matters more than the headline 27%",
        "hardest": (
            "Reporting only the post-drift 27% cost reduction would have been a true but misleading "
            "framing &mdash; it implies the sequence models are simply better. The pre-drift comparison "
            "(0.956 vs 0.950 PR-AUC, effectively a tie) is what actually locates <em>why</em> they win: "
            "not raw predictive power, but robustness when the fraud pattern itself shifts. That "
            "distinction changes the real recommendation &mdash; it's an argument for the added "
            "complexity specifically in a non-stationary threat environment, not a blanket "
            "'deep learning wins' claim."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "Focal loss and weighted sampling, the two standard fixes for class imbalance, failed in "
            "<em>different</em> ways rather than both simply helping: focal loss degraded probability "
            "calibration (ECE 0.0063) while weighted sampling instead cost ranking quality "
            "(&minus;0.042 PR-AUC). Neither fix was free, and knowing which one costs what let calibration "
            "be corrected surgically afterward &mdash; temperature scaling and isotonic regression "
            "brought ECE down to 0.0005 &mdash; rather than accepting whichever trade-off the first "
            "technique happened to introduce."
        ),
        "next": "Test against a wider set of injected drift patterns to check whether the robustness advantage generalizes beyond the specific drift mechanism used in evaluation.",
        "stack": ["Python", "PyTorch", "LightGBM", "ONNX Runtime", "FastAPI", "Docker", "SHAP"],
    },
    {
        "slug": "credit-risk",
        "name": "Credit Risk Decisioning & Fairness Audit",
        "short": "A full credit decisioning system prioritizing calibration over ranking, with reject inference correcting for approval-only observed outcomes and fairness treated as an explicit policy tradeoff.",
        "tags": ["Credit Risk", "Calibration", "Fairness", "Scorecards"],
        "status": None,
        "headline_label": "PRIORITIZED METRIC",
        "headline_value": "ECE",
        "headline_unit": "",
        "github": "https://github.com/MelvTheGoat/credit-risk-decisionin",
        "live": "https://credit-risk-decisioning-702657773047.europe-west1.run.app/",
        "problem": (
            "A lending decision needs a true probability of default, not just a well-ranked score "
            "&mdash; expected loss is a function of a calibrated probability multiplied by exposure, "
            "and a model that ranks applicants correctly but reports overconfident probabilities "
            "produces systematically wrong loss estimates even when its AUC looks strong."
        ),
        "result": (
            "Benchmarked gradient boosting against a traditional WOE-binned logistic scorecard on "
            "calibration quality specifically &mdash; Brier score, reliability diagrams, expected "
            "calibration error &mdash; rather than defaulting to whichever model had the higher AUC."
        ),
        "flow": "WOE scorecard vs. LightGBM → calibration diagnostics\n  → reject inference on approval-only outcomes → fairness audit across protected groups\n  → adverse-action reason codes → audit trail",
        "hardest_title": "Why calibration was prioritized over ranking metrics",
        "hardest": (
            "AUC and similar ranking metrics answer 'does the model order applicants correctly' &mdash; "
            "they say nothing about whether a stated 8% default probability is actually an 8% real-world "
            "rate. Expected loss calculations need the second property, not the first. A model can have "
            "excellent AUC and be badly miscalibrated, producing confidently wrong loss estimates that "
            "look statistically sound until you check them against reality."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "Outcomes are only observed for previously <em>approved</em> applicants &mdash; a structural "
            "selection bias that a naive model trained only on approved-applicant data inherits "
            "silently. Reject inference corrections were validated against simulated data specifically "
            "because the true outcome for a rejected applicant is, by definition, never observed in real "
            "data &mdash; there is no ground truth to check the correction against outside of a "
            "simulation built to contain one."
        ),
        "next": "Extend the fairness audit to intersectional subgroups rather than single protected attributes evaluated independently.",
        "stack": ["Python", "LightGBM", "scikit-learn", "SHAP", "WOE Scorecards", "FastAPI", "Docker"],
    },
    {
        "slug": "forecasting",
        "name": "Self-Operating Demand Forecasting Platform",
        "short": "An orchestrated, end-to-end forecasting pipeline for NYC taxi zones with asymmetric cost modeling, rolling-origin backtesting, and drift-triggered retraining gated on real cost improvement.",
        "tags": ["Forecasting", "MLOps", "Drift Monitoring"],
        "status": None,
        "headline_label": "COST REDUCTION",
        "headline_value": "25",
        "headline_unit": "%",
        "github": "https://github.com/MelvTheGoat/demand-forecasting-platform",
        "live": None,
        "problem": (
            "Point forecasts and symmetric error metrics don't reflect the real cost structure of "
            "demand planning, where under-forecasting (unmet demand) and over-forecasting (idle supply) "
            "have genuinely different costs &mdash; optimizing for the wrong metric produces a forecast "
            "that's statistically accurate and operationally expensive."
        ),
        "result": (
            "Modeled unmet demand at 3&times; the cost of idle supply and shipped the cost-optimal "
            "quantile rather than the median, cutting expected cost 25% against an identical model "
            "optimized on a symmetric metric, and beating a seasonal-naive baseline by 32%."
        ),
        "flow": "ingest → dbt/DuckDB transforms → rolling-origin backtest (6 folds)\n  → asymmetric cost-optimal quantile selection → drift monitoring (PSI/KS/MASE)\n  → champion/challenger promotion",
        "hardest_title": "Why asymmetric cost instead of MASE alone",
        "hardest": (
            "A model chosen purely to minimize MASE optimizes the wrong objective if the two error "
            "directions cost differently in the real system it feeds. Shipping the cost-optimal quantile "
            "&mdash; not the median, and not the metric-minimizing point forecast &mdash; means the "
            "model is trained toward the actual business objective rather than a proxy metric that "
            "happens to be convenient to optimize."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "Automated leakage tests were built to fail the CI build if any feature reads past the "
            "forecast origin &mdash; a structural guardrail rather than a one-time manual check, because "
            "leakage in a forecasting pipeline produces backtests that look excellent and fail silently "
            "in production. Champion/challenger promotion is gated on a 2% out-of-sample cost margin "
            "specifically so a retrained model has to prove real improvement before replacing the "
            "one in production, not just look different."
        ),
        "next": "Extend the drift-triggered retraining to detect covariate shift in the raw ingestion data itself, ahead of it surfacing in downstream forecast error.",
        "stack": ["Python", "Prefect", "dbt-core", "DuckDB", "LightGBM", "MLflow", "Evidently", "FastAPI", "Docker", "GitHub Actions"],
    },
    {
        "slug": "uplift",
        "name": "Uplift Modeling & Causal Targeting Study",
        "short": "Heterogeneous treatment effect estimation on a randomized marketing trial, validated against simulated ground truth, with a placebo-test null result reported rather than shipped as a win.",
        "tags": ["Causal Inference", "Experiment Design", "Uplift"],
        "status": None,
        "headline_label": "SAMPLE SIZE",
        "headline_value": "64,000",
        "headline_unit": "",
        "github": "https://github.com/MelvTheGoat/uplift-causal-targeting",
        "live": None,
        "problem": (
            "Standard propensity models identify customers likely to convert &mdash; not customers who "
            "convert <em>because of</em> an intervention. Targeting on propensity alone wastes spend on "
            "customers who would have converted regardless, and misses the customers an intervention "
            "would actually move."
        ),
        "result": (
            "S-, T-, and X-learners plus a causal forest, each validated against simulated data with "
            "known individual treatment effects &mdash; since true counterfactuals are unobservable and "
            "no accuracy metric exists to check an uplift model against on real data alone."
        ),
        "flow": "randomized trial (n=64,000) → S/T/X-learners + causal forest\n  → Qini curves, AUUC, decile uplift tables → placebo, covariate-balance, seed-stability tests\n  → budget-constrained targeting policy",
        "hardest_title": "Why the placebo test mattered enough to report a null result",
        "hardest": (
            "The placebo test &mdash; assigning a fake treatment and checking whether the model finds a "
            "spurious effect &mdash; showed the ranking was indistinguishable from noise on the primary "
            "arm. That's the test that actually tells you whether an uplift model is finding a real "
            "signal or an artifact of the estimator. Reporting it, rather than quietly moving on to a "
            "more flattering result, is what makes the rest of the analysis trustworthy."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "18.6% of customers were flagged as negative-uplift &mdash; predicted to respond "
            "<em>worse</em> to the intervention &mdash; and that segment measured +0.44 percentage "
            "points against the randomized holdout when checked. A negative result, reported plainly "
            "rather than shipped as a targeting win, because a decision memo that hides its own "
            "estimator's failure mode is worse than useless to whoever has to act on it."
        ),
        "next": "Re-run with a larger trial to check whether the placebo-test noise floor shrinks with more data, or reflects a genuine ceiling on detectable heterogeneity in this population.",
        "stack": ["Python", "EconML", "CausalML", "LightGBM", "scikit-learn", "Experiment Design"],
    },
]


def summary_line():
    return (
        "Machine Learning &amp; AI Engineer with a Statistics background, specializing in systems "
        "where the probability must be trustworthy and not merely the label. Experience spans "
        "classical ML and deep learning &mdash; forecasting, credit risk, and fraud pipelines through "
        "to sequence models and deployed retrieval-augmented generation &mdash; with consistent depth "
        "in temporally honest validation, calibrated decisioning, evaluation design, containerized "
        "serving, and drift monitoring."
    )


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------

def build_home():
    featured = PROJECTS[:3]  # rag, fraud, credit-risk
    cards = ""
    for p in featured:
        status = f'<span class="card-status">{p["status"]}</span>' if p["status"] else ""
        cards += f"""
        <a class="card" href="projects/{p['slug']}.html" style="text-decoration:none;">
          <div class="tags">
            {''.join(f'<span class="tag">{t}</span>' for t in p['tags'][:3])}
          </div>
          <h3>{p['name']}</h3>
          <p class="card-desc">{p['short']}</p>
          {reading(p['headline_label'], p['headline_value'], p['headline_unit'], small=True)}
          <span class="card-link">{status or 'View project &rarr;'}</span>
        </a>"""

    body = f"""  <main>
    <section class="hero">
      <div class="hero-grid" aria-hidden="true"></div>
      <div class="wrap hero-inner">
        <div class="eyebrow">Lagos, Nigeria &mdash; Open to DS / ML / DL / AI roles</div>
        <h1>I build systems where the probability has to be right, not just plausible.</h1>
        <div class="role">Machine Learning &amp; AI Engineer</div>
        <p class="lede">Forecasting, credit risk, fraud detection, causal inference, and a deployed
        RAG system &mdash; each one evaluated the way a production system is evaluated, not the way
        a portfolio project usually is.</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="{RAG_LIVE_URL}" target="_blank" rel="noopener">Try the live demo &rarr;</a>
          <a class="btn" href="projects.html">View all projects</a>
        </div>
        <div class="reading-row">
          {reading('MODELS EVALUATED AGAINST', '5', 'baselines')}
          {reading('DEPLOYED', '2', 'live system')}
          {reading('COST REDUCTION', '25&ndash;27', '%')}
        </div>
      </div>
    </section>

    <div class="wrap">
      <div class="demo-callout">
        <div>
          <div class="status"><span class="pulse"></span>Live &mdash; GCP Cloud Run</div>
          <h3>Nigerian Fintech Compliance RAG Assistant</h3>
          <p>Ask it a real regulatory question &mdash; CBN circulars, the NDPA &mdash; and get a
          grounded, cited answer. It refuses rather than guesses when the source doesn't support one.</p>
        </div>
        <a class="btn btn-primary" href="{RAG_LIVE_URL}" target="_blank" rel="noopener">Open the demo &rarr;</a>
      </div>

      <div class="demo-callout" style="margin-top: 1.5rem;">
        <div>
          <div class="status"><span class="pulse"></span>Live &mdash; GCP Cloud Run</div>
          <h3>Credit Risk Decisioning &amp; Fairness Audit</h3>
          <p>A full credit decisioning system prioritizing calibration over ranking, with reject inference correcting for approval-only observed outcomes.</p>
        </div>
        <a class="btn btn-primary" href="https://credit-risk-decisioning-702657773047.europe-west1.run.app/" target="_blank" rel="noopener">Open the demo &rarr;</a>
      </div>
    </div>

    <section>
      <div class="wrap">
        <div class="section-head">
          <h2>Featured work</h2>
          <a href="projects.html">All projects &rarr;</a>
        </div>
        <div class="project-grid">{cards}
        </div>
      </div>
    </section>

    <div class="pattern-strip">
      <div class="wrap">
        <div class="eyebrow">The pattern across all five</div>
        <h2 style="color:#fff; max-width: 24ch;">Every model earns production through a measured comparison, not a vibe.</h2>
        <div class="pattern-grid">
          <div class="pattern-item"><span class="num">01</span><p>Evaluate before modeling &mdash; the metric and the split get decided before a single model is trained.</p></div>
          <div class="pattern-item"><span class="num">02</span><p>Build the honest baseline first, and report it even when it wins.</p></div>
          <div class="pattern-item"><span class="num">03</span><p>Report the negative result &mdash; a placebo test, a limitation, a number that didn't flatter the project.</p></div>
          <div class="pattern-item"><span class="num">04</span><p>Calibration over ranking, wherever the output feeds a real decision.</p></div>
        </div>
      </div>
    </div>

    <div class="wrap">
      <div class="currently"><span class="pulse"></span>Currently teaching Machine Learning at SQI College of ICT, Ibadan &mdash; open to remote or relocation roles.</div>
    </div>
  </main>
"""
    return page(
        f"{NAME} &mdash; Machine Learning &amp; AI Engineer",
        "Machine Learning and AI Engineer specializing in calibrated, rigorously evaluated systems: forecasting, credit risk, fraud detection, causal inference, and a deployed RAG assistant.",
        "home", body,
    )


# ---------------------------------------------------------------------------
# PROJECTS INDEX
# ---------------------------------------------------------------------------

def build_projects_index():
    cards = ""
    for p in PROJECTS:
        status = f'<span class="card-status">{p["status"]}</span>' if p["status"] else '<span class="card-link">View &rarr;</span>'
        cards += f"""
        <a class="card" href="projects/{p['slug']}.html" style="text-decoration:none;">
          <div class="card-main">
            <div class="tags">
              {''.join(f'<span class="tag">{t}</span>' for t in p['tags'])}
            </div>
            <h3>{p['name']}</h3>
            <p class="card-desc">{p['short']}</p>
          </div>
          <div>
            {reading(p['headline_label'], p['headline_value'], p['headline_unit'])}
            <div style="margin-top:10px;">{status}</div>
          </div>
        </a>"""

    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">Five systems, one evaluation discipline</div>
        <h1>Projects</h1>
        <p class="lede" style="max-width:60ch;">Each page follows the same structure on purpose: the
        problem, the headline result, the architecture, the one decision most worth defending, and
        what the results actually showed &mdash; including the parts that didn't flatter the project.</p>
      </div>
    </section>
    <section class="tight">
      <div class="wrap">
        <div class="project-grid full">{cards}
        </div>
      </div>
    </section>
  </main>
"""
    return page(
        f"Projects &mdash; {NAME}",
        "Five ML and AI projects: demand forecasting, fraud detection, credit risk, causal inference, and a deployed RAG assistant.",
        "projects", body,
    )


# ---------------------------------------------------------------------------
# PROJECT DETAIL PAGES
# ---------------------------------------------------------------------------

def build_project_page(p, idx):
    live_btn = f'<a class="btn btn-primary" href="{p["live"]}" target="_blank" rel="noopener">Open live demo &rarr;</a>' if p["live"] else ""
    github_btn = f'<a class="btn" href="{p["github"]}" target="_blank" rel="noopener">View on GitHub &rarr;</a>'

    next_p = PROJECTS[(idx + 1) % len(PROJECTS)]

    body = f"""  <main>
    <section class="project-hero">
      <div class="wrap">
        <div class="tags">
          {''.join(f'<span class="tag">{t}</span>' for t in p['tags'])}
        </div>
        <h1>{p['name']}</h1>
        <p class="subtitle">{p['short']}</p>
        <div class="meta-row">
          {live_btn}
          {github_btn}
        </div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">01</span>The problem</h2>
        <p>{p['problem']}</p>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">02</span>The result</h2>
        <div class="result-banner">
          <div class="eyebrow">Headline number</div>
          <p>{p['result']}</p>
        </div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">03</span>Architecture</h2>
        <div class="flow">{p['flow']}</div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">04</span>The hardest decision</h2>
        <div class="decision-block">
          <h4>{p['hardest_title']}</h4>
          <p>{p['hardest']}</p>
        </div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">05</span>What the results actually showed</h2>
        <div class="measured-box">
          <div class="eyebrow">Measured, not assumed</div>
          <p>{p['measured']}</p>
        </div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">06</span>What's next</h2>
        <p>{p['next']}</p>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">07</span>Stack</h2>
        <div class="stack-tags">
          {''.join(f'<span class="tag">{s}</span>' for s in p['stack'])}
        </div>
      </div>
    </section>

    <div class="wrap">
      <div class="next-project">
        <span class="eyebrow" style="margin-bottom:0;">Next project</span>
        <a href="{next_p['slug']}.html">{next_p['name']} &rarr;</a>
      </div>
    </div>
  </main>
"""
    return page(
        f"{p['name']} &mdash; {NAME}",
        p['short'],
        "projects", body, depth="../",
    )


# ---------------------------------------------------------------------------
# WRITING
# ---------------------------------------------------------------------------

def build_writing():
    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">Notes on building this way</div>
        <h1>Writing</h1>
        <p class="lede" style="max-width:60ch;">Longer-form pieces on the reasoning behind these
        projects &mdash; written for anyone deciding whether to trust a number, including future me.</p>
      </div>
    </section>
    <section class="tight">
      <div class="wrap">

        <div class="post-card">
          <span class="post-date">[FILL: publish date]</span>
          <h3>Building a RAG system that refuses on purpose</h3>
          <p>[FILL: 1&ndash;2 sentence summary of the RAG writeup &mdash; use the outline already
          drafted for this post. Covers hybrid retrieval, the citation guardrail, and the honest
          refusal-correctness limitation found in evaluation.]</p>
          <a class="card-link" href="#">Read the full post &rarr; [FILL: link once published]</a>
        </div>

        <div class="post-card">
          <span class="post-date">[FILL: publish date]</span>
          <h3>Why I evaluate before I model</h3>
          <p>[FILL: a generalized piece on the pattern across all five projects &mdash; honest
          baselines, calibration over ranking, reporting the negative result. This is the piece that
          ties the whole portfolio together into one argument.]</p>
          <a class="card-link" href="#">Read the full post &rarr; [FILL: link once published]</a>
        </div>

        <div class="empty-note">
          More writing in progress &mdash; two posts published, more planned as each project's
          evaluation work matures.
        </div>

      </div>
    </section>
  </main>
"""
    return page(
        f"Writing &mdash; {NAME}",
        "Notes on evaluation, calibration, and building ML/AI systems that report their own limitations honestly.",
        "writing", body,
    )


# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------

def build_about():
    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">About</div>
        <h1>{NAME}</h1>
      </div>
    </section>
    <section class="tight">
      <div class="wrap two-col">
        <div>
          <div class="avatar-box"><img src="assets/photo_2026-08-16_14-26-22.jpg" alt="{NAME}" style="width: 100%; height: auto; border-radius: 4px;"></div>
        </div>
        <div>
          <p class="lede">{summary_line()}</p>

          <h3>Path</h3>
          <p>B.Sc. in Statistics from the University of Ibadan (2021&ndash;2025), then a deliberate,
          self-directed move into machine learning and AI &mdash; now formalized through a Professional
          Diploma in Artificial Intelligence at SQI College of ICT. Not the traditional CS-degree route
          into ML, and I don't treat that as something to explain away &mdash; the five projects on this
          site are the actual evidence of whether it worked.</p>

          <h3>Why Statistics shapes how I build</h3>
          <p>Every project on this site prioritizes calibration &mdash; a true probability, not just a
          well-ranked score &mdash; over a flashier ranking metric wherever the output feeds a real
          decision. That instinct traces directly back to a Statistics background, not something picked
          up from an ML tutorial. It shows up as reliability diagrams in the credit risk project,
          temperature scaling in the fraud model, and a placebo test reported honestly, even when it
          came back null, in the uplift study.</p>

          <h3>Teaching</h3>
          <p>Currently a Machine Learning Instructor at SQI College of ICT, teaching predictive
          modeling, algorithm selection, and evaluation metrics to monthly cohorts. Teaching has
          sharpened something specific: the ability to explain a technical decision clearly to someone
          who wasn't in the room when it was made &mdash; which is exactly what every project writeup
          on this site is trying to do.</p>

          <h3>Building from Lagos</h3>
          <p>Every architectural decision in the RAG project &mdash; ONNX over PyTorch, brute-force
          search instead of a vector database, single-threaded inference &mdash; traces back to
          designing for a genuinely constrained memory budget rather than assuming unlimited cloud
          resources by default. That's not a workaround; it's an engineering instinct that's harder to
          develop when infrastructure is never actually the constraint.</p>
        </div>
      </div>
    </section>
  </main>
"""
    return page(
        f"About &mdash; {NAME}",
        f"Statistics background, self-directed path into ML/AI, currently teaching at SQI College of ICT, based in {LOCATION}.",
        "about", body,
    )


# ---------------------------------------------------------------------------
# RESUME
# ---------------------------------------------------------------------------

def build_resume():
    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">Resume</div>
        <h1>CV</h1>
        <div class="btn-row" style="margin-top:18px;">
          <a class="btn btn-primary" href="assets/resume.pdf" download>Download PDF</a>
        </div>
      </div>
    </section>
    <section class="tight">
      <div class="wrap">
        <div class="resume-embed">
          <iframe src="assets/resume.pdf" title="Resume"></iframe>
        </div>
        <p class="empty-note" style="margin-top:16px;">
          [FILL: place your current resume PDF at <span class="mono">/assets/resume.pdf</span>.
          The embed and download button above both point there already &mdash; nothing else to wire up.]
        </p>
      </div>
    </section>
  </main>
"""
    return page(
        f"Resume &mdash; {NAME}",
        "Download or view the current resume.",
        "resume", body,
    )


# ---------------------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------------------

def build_contact():
    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">Get in touch</div>
        <h1>Contact</h1>
        <p class="lede" style="max-width:56ch;">Happy to talk about a role, a project, or just the
        reasoning behind any of the evaluation decisions on this site.</p>
        <div class="contact-grid">
          <div class="contact-card">
            <div class="eyebrow">Email</div>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
          </div>
          <div class="contact-card">
            <div class="eyebrow">LinkedIn</div>
            <a href="{LINKEDIN}" target="_blank" rel="noopener">oluwatobi-mayungbo</a>
          </div>
          <div class="contact-card">
            <div class="eyebrow">GitHub</div>
            <a href="{GITHUB_PROFILE}" target="_blank" rel="noopener">MelvTheGoat</a>
          </div>
        </div>
        <div style="margin-top: 28px;">
          <a class="btn btn-primary" href="https://calendly.com/mlvyn-t" target="_blank" rel="noopener">Book a Chat on Calendly &rarr;</a>
        </div>
      </div>
    </section>
  </main>
"""
    return page(
        f"Contact &mdash; {NAME}",
        f"Get in touch &mdash; {EMAIL}",
        "contact", body,
    )


# ---------------------------------------------------------------------------
# Write everything
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def main():
    write("index.html", build_home())
    write("projects.html", build_projects_index())
    write("writing.html", build_writing())
    write("about.html", build_about())
    write("resume.html", build_resume())
    write("contact.html", build_contact())
    for i, p in enumerate(PROJECTS):
        write(f"projects/{p['slug']}.html", build_project_page(p, i))
    print("\nDone. Open index.html in a browser, or deploy the whole folder as-is.")


if __name__ == "__main__":
    main()
