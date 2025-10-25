def get_demo_html() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width,initial-scale=1.0" />
<title>Transaction Trust Report</title>
<style>
    :root {
        --bg-page: #ffffff;
        --text-main: #0f172a;
        --text-subtle: #64748b;
        --surface-card: #ffffff;
        --border-card: #e2e8f0;
        --radius-card: 16px;
        --accent-blue-start: #3b82f6;
        --accent-blue-end: #2563eb;
        --risk-high: #dc2626;
        --risk-high-bg: #fee2e2;
        --risk-med: #facc15;
        --risk-low: #10b981;
        --divider: #e5e7eb;
        --font-stack: -apple-system, BlinkMacSystemFont, "Inter", "SF Pro Text", system-ui, Roboto, "Helvetica Neue", sans-serif;
    }

    body {
        background-color: var(--bg-page);
        color: var(--text-main);
        font-family: var(--font-stack);
        -webkit-font-smoothing: antialiased;
        display:flex;
        flex-direction:column;
        align-items:center;
        padding:2rem 1rem 4rem;
    }

    h1 {
        font-size:1.5rem;
        font-weight:600;
        color:var(--text-main);
        text-align:center;
        margin-bottom:0.5rem;
        letter-spacing:-0.02em;
    }
    .subhead {
        font-size:0.9rem;
        color:var(--text-subtle);
        text-align:center;
        margin:0 0 1.5rem 0;
        max-width:320px;
        line-height:1.4;
        letter-spacing:-0.02em;
    }

    .run-btn {
        background:linear-gradient(90deg,var(--accent-blue-start),var(--accent-blue-end));
        border:none;
        color:#fff;
        font-weight:600;
        font-size:0.95rem;
        border-radius:0.6rem;
        padding:0.8rem 1.25rem;
        cursor:pointer;
        box-shadow:0 18px 40px rgba(37,99,235,0.35);
        transition:transform 0.1s;
    }
    .run-btn:active {
        transform:scale(.97);
    }

    /* main result container */
    .report-shell {
        width:100%;
        max-width:900px;
        background:var(--surface-card);
        border:1px solid var(--border-card);
        border-radius:var(--radius-card);
        box-shadow:0 24px 60px rgba(0,0,0,0.07);
        margin-top:2rem;
        padding:1.5rem 1.5rem 2rem;
        display:none; /* hidden until first run */
        opacity:0;
        transform:translateY(16px);
        transition:all 400ms ease;
    }
    .report-shell.show {
        display:block;
        opacity:1;
        transform:translateY(0);
    }

    /* staged fade/slide for inner sections */
    .reveal {
        opacity: 0;
        transform: translateY(12px);
        transition: all 400ms ease;
    }
    .reveal.show {
        opacity: 1;
        transform: translateY(0);
    }

    /* layout: gauge on left, summary on right */
    .top-row {
        display:flex;
        flex-wrap:wrap;
        gap:2rem;
    }
    .gauge-col {
        flex:0 0 260px;
        display:flex;
        flex-direction:column;
        align-items:center;
    }
    .summary-col {
        flex:1;
        min-width:240px;
        display:flex;
        flex-direction:column;
        justify-content:flex-start;
    }

    .score-label {
        font-size:0.8rem;
        color:var(--text-subtle);
        text-align:center;
        margin-top:0.75rem;
        margin-bottom:0.25rem;
        letter-spacing:-0.02em;
    }

    .score-main {
        text-align:center;
        font-size:2rem;
        font-weight:600;
        line-height:1.2;
        color:var(--text-main);
        display:flex;
        flex-direction:column;
        align-items:center;
    }

    /* score fade in after needle animates */
    .score-fade {
        opacity: 0;
        transition: opacity 400ms ease;
    }
    .score-fade.show {
        opacity: 1;
    }

    .score-main .risk-tier-pill {
        display:inline-block;
        margin-top:0.4rem;
        font-size:0.7rem;
        font-weight:600;
        line-height:1.2;
        border-radius:0.4rem;
        padding:0.3rem 0.5rem;
        background:var(--risk-high-bg);
        color:var(--risk-high);
        border:1px solid var(--risk-high);
        letter-spacing:-0.02em;
    }

    .action-line {
        margin-top:0.75rem;
        font-size:0.8rem;
        color:var(--text-subtle);
        text-align:center;
        line-height:1.4;
        letter-spacing:-0.02em;
    }

    .tier-legend {
        margin-top:0.5rem;
        font-size:0.7rem;
        color:var(--text-subtle);
        text-align:center;
        line-height:1.3;
        letter-spacing:-0.02em;
    }

    /* right column summary */
    .summary-title {
        font-size:0.9rem;
        font-weight:600;
        color:var(--text-main);
        margin-bottom:0.5rem;
        line-height:1.3;
        letter-spacing:-0.02em;
    }
    .summary-body {
        font-size:0.9rem;
        color:var(--text-main);
        line-height:1.4;
        letter-spacing:-0.02em;
    }
    .summary-badge-row {
        display:flex;
        flex-wrap:wrap;
        align-items:center;
        gap:0.5rem;
        margin-top:0.75rem;
    }
    .act-badge {
        background:var(--risk-high-bg);
        color:var(--risk-high);
        border:1px solid var(--risk-high);
        font-size:0.7rem;
        font-weight:600;
        border-radius:0.4rem;
        padding:0.3rem 0.5rem;
        line-height:1.2;
        letter-spacing:-0.02em;
    }
    .latency-note {
        font-size:0.7rem;
        color:var(--text-subtle);
        line-height:1.2;
        letter-spacing:-0.02em;
    }

    /* divider */
    .divider {
        width:100%;
        height:1px;
        background:var(--divider);
        margin:1.5rem 0 1rem;
    }

    /* expandable details */
    .details-wrapper {
        border-radius:0.75rem;
        border:1px solid var(--border-card);
        background:#f8fafc;
    }
    .details-header {
        width:100%;
        background:transparent;
        display:flex;
        justify-content:space-between;
        align-items:center;
        border:none;
        cursor:pointer;
        padding:0.9rem 1rem;
        font-size:0.9rem;
        font-weight:600;
        color:var(--text-main);
        line-height:1.3;
        letter-spacing:-0.02em;
    }
    .details-header span.subtle {
        font-weight:400;
        color:var(--text-subtle);
        font-size:0.8rem;
    }
    .chevron {
        font-size:0.9rem;
        color:var(--text-subtle);
        transition:transform .2s ease;
    }
    .chevron.open {
        transform:rotate(180deg);
    }

    .details-body {
        display:none;
        padding:0 1rem 1rem;
        font-size:0.8rem;
        line-height:1.4;
        color:var(--text-main);
        letter-spacing:-0.02em;
    }
    .details-body.show {
        display:block;
    }

    .detail-block {
        margin-top:1rem;
    }
    .detail-title {
        font-weight:600;
        font-size:0.8rem;
        margin-bottom:0.3rem;
        color:var(--text-main);
        letter-spacing:-0.02em;
    }
    .detail-text {
        font-size:0.8rem;
        color:var(--text-main);
        line-height:1.4;
        letter-spacing:-0.02em;
    }

    /* gauge styles */
    .gauge-col { text-align:center; }
    .gauge-wrap {
        width:200px;
        height:100px;
        position:relative;
    }
    .gauge-arc {
        width:100%;
        height:100%;
    }
    /* needle */
    .needle {
        width:2px;
        height:80px;
        background:var(--text-main);
        position:absolute;
        left:50%;
        bottom:0;
        transform-origin:bottom center;
        transform:rotate(-90deg);
        transition:transform 0.6s cubic-bezier(.2,.7,.4,1);
        border-radius:999px;
        box-shadow:0 0 6px rgba(0,0,0,0.3);
    }
    .needle-dot {
        position:absolute;
        bottom:78px;
        left:50%;
        width:10px;
        height:10px;
        margin-left:-5px;
        background:var(--text-main);
        border-radius:50%;
        box-shadow:0 2px 4px rgba(0,0,0,0.4);
    }

    footer {
        color:var(--text-subtle);
        text-align:center;
        font-size:0.7rem;
        line-height:1.4;
        letter-spacing:-0.02em;
        margin-top:2rem;
        max-width:600px;
    }

    @media (max-width:600px){
        .top-row{flex-direction:column;align-items:center;}
        .gauge-col{flex:unset;}
        .summary-col{flex:unset;min-width:unset;text-align:center;}
        .summary-badge-row{justify-content:center;}
    }
</style>
</head>
<body>

    <h1>Transaction Trust Report</h1>
    <p class="subhead">AI risk assessment for this purchase attempt</p>

    <button class="run-btn" id="runBtn">Run Fraud Attempt Simulation</button>

    <section class="report-shell" id="reportShell">
        <div class="top-row">

            <!-- LEFT: Gauge / Risk -->
            <div class="gauge-col reveal" id="gaugeReveal">
                <div class="gauge-wrap">
                    <!-- semicircle arc background -->
                    <svg class="gauge-arc" viewBox="0 0 100 50" preserveAspectRatio="xMidYMid meet">
                        <!-- green zone -->
                        <path d="M10 50 A40 40 0 0 1 50 10"
                              stroke="#10b981" stroke-width="8" fill="none" stroke-linecap="round"/>
                        <!-- yellow zone -->
                        <path d="M50 10 A40 40 0 0 1 75 20"
                              stroke="#facc15" stroke-width="8" fill="none" stroke-linecap="round"/>
                        <!-- red zone -->
                        <path d="M75 20 A40 40 0 0 1 90 50"
                              stroke="#dc2626" stroke-width="8" fill="none" stroke-linecap="round"/>
                    </svg>

                    <!-- needle -->
                    <div class="needle" id="needle">
                        <div class="needle-dot"></div>
                    </div>
                </div>

                <div class="score-label">Fraud Risk</div>

                <div class="score-main">
                    <div class="score-fade" id="scoreFadeWrapper">
                        <span id="scoreValue">--</span>
                        <span style="font-size:1rem;font-weight:500;color:var(--text-subtle);"> /100</span>
                    </div>
                    <div class="risk-tier-pill" id="riskTierPill">HIGH</div>
                </div>

                <div class="action-line" id="actionLine">
                    Action taken: —
                </div>

                <div class="tier-legend">
                    Low → approve &nbsp;|&nbsp;
                    Medium → verify &nbsp;|&nbsp;
                    High → block
                </div>
            </div>

            <!-- RIGHT: Summary -->
            <div class="summary-col reveal" id="summaryReveal">
                <div class="summary-title">Summary</div>
                <div class="summary-body" id="summaryBody">
                    —
                </div>
                <div class="summary-badge-row">
                    <div class="act-badge" id="actBadge">—</div>
                    <div class="latency-note" id="latencyNote">—</div>
                </div>
            </div>

        </div>

        <div class="divider"></div>

        <!-- expandable details -->
        <div class="details-wrapper reveal" id="detailsReveal">
            <button class="details-header" id="detailsToggle">
                <div>
                    Why was this flagged?
                    <br />
                    <span class="subtle">Tap to view signals, privacy, and network protection</span>
                </div>
                <div class="chevron" id="chevron">▼</div>
            </button>

            <div class="details-body" id="detailsBody">
                <div class="detail-block">
                    <div class="detail-title">What happened</div>
                    <div class="detail-text" id="opsMsg">
                        We saw a purchase attempt from Madrid only 5 minutes after your last confirmed
                        purchase in New York, from a different device. That physical jump is not possible
                        for a real person, which strongly suggests someone copied your card details and
                        tried to use them.
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-title">How we protected you</div>
                    <div class="detail-text" id="privacyMsg">
                        We automatically stopped the transaction before any money could leave your
                        account and marked that device and location as high risk. We made this decision
                        using behavior signals — location, timing, and device — without storing your
                        full card number or other personal identity data.
                    </div>
                </div>

                <div class="detail-block">
                    <div class="detail-title">How this helps everyone</div>
                    <div class="detail-text" id="shareMsg">
                        We generate an anonymized alert about this pattern — sudden foreign attempt
                        right after a domestic purchase, on a new device — and share only that pattern
                        with partner banks. That helps them stop the same attacker without sharing who
                        you are.
                    </div>
                </div>
            </div>
        </div>
    </section>

    <footer>
        Adaptive fraud defense: real-time scoring, minimal customer friction, encrypted behavioral analytics, and anonymized signal sharing.
    </footer>

<script>
(function(){
    const runBtn = document.getElementById("runBtn");
    const shell = document.getElementById("reportShell");

    const needleEl = document.getElementById("needle");
    const scoreEl = document.getElementById("scoreValue");
    const scoreFadeWrapper = document.getElementById("scoreFadeWrapper");
    const tierPill = document.getElementById("riskTierPill");
    const actionLine = document.getElementById("actionLine");
    const summaryBody = document.getElementById("summaryBody");
    const actBadge = document.getElementById("actBadge");
    const latencyNote = document.getElementById("latencyNote");

    const opsMsg = document.getElementById("opsMsg");
    const privacyMsg = document.getElementById("privacyMsg");
    const shareMsg = document.getElementById("shareMsg");

    const detailsToggle = document.getElementById("detailsToggle");
    const detailsBody = document.getElementById("detailsBody");
    const chevron = document.getElementById("chevron");

    const gaugeReveal = document.getElementById("gaugeReveal");
    const summaryReveal = document.getElementById("summaryReveal");
    const detailsReveal = document.getElementById("detailsReveal");

    // expand/collapse deep dive
    detailsToggle.addEventListener("click", () => {
        const open = detailsBody.classList.toggle("show");
        chevron.classList.toggle("open", open);
    });

    runBtn.addEventListener("click", async () => {
        runBtn.disabled = true;
        runBtn.textContent = "Running...";

        const resp = await fetch("/scenario_impossible_travel");
        const data = await resp.json();

        runBtn.disabled = false;
        runBtn.textContent = "Run Fraud Attempt Simulation";

        // 1. reveal main card shell
        shell.classList.add("show");

        // hide inner sections initially for staged reveal
        gaugeReveal.classList.remove("show");
        summaryReveal.classList.remove("show");
        detailsReveal.classList.remove("show");

        // reset needle + score visuals
        const rawScore = data.score || 0;
        const score100 = Math.round(rawScore * 100);

        needleEl.style.transform = "rotate(-90deg)"; // far left
        scoreEl.textContent = "0";
        scoreFadeWrapper.classList.remove("show");

        // 2. set content for summary and details (so it's ready before reveal)
        // risk tier pill + action line
        tierPill.textContent = data.risk_tier || "HIGH";

        if (data.risk_tier === "LOW") {
            tierPill.style.background = "#ecfdf5";
            tierPill.style.color = "#065f46";
            tierPill.style.border = "1px solid #10b981";
            actionLine.style.color = "#065f46";
            actionLine.textContent = "Action taken: Approved normally";
        } else if (data.risk_tier === "MEDIUM") {
            tierPill.style.background = "#fffbeb";
            tierPill.style.color = "#78350f";
            tierPill.style.border = "1px solid #facc15";
            actionLine.style.color = "#78350f";
            actionLine.textContent = "Action taken: Step-up verification";
        } else {
            tierPill.style.background = "#fee2e2";
            tierPill.style.color = "#dc2626";
            tierPill.style.border = "1px solid #dc2626";
            actionLine.style.color = "#dc2626";
            actionLine.textContent = "Action taken: Blocked automatically";
        }

        // high-level summary for the customer
        // we show what happened and reassure them
        summaryBody.textContent = data.customer_message ||
            "We blocked a high-risk purchase attempt from a new location. Your card is safe and no money left your account.";

        // badge: BLOCKED / etc.
        actBadge.textContent = (data.decision || "BLOCKED").toUpperCase();
        latencyNote.textContent = "Decision time: 2 ms";

        // deep dive sections (expanded area)
        opsMsg.textContent = data.ops_view ||
            "We saw a purchase attempt from Madrid only 5 minutes after your last confirmed purchase in New York, from a different device. That physical jump is not possible for a real person, which strongly suggests someone copied your card details and tried to use them.";

        privacyMsg.textContent = data.privacy_info ||
            "We automatically stopped the transaction before any money could leave your account and marked that device and location as high risk. We did this using behavior signals — location, timing, and device — without storing your full card number or other personal identity data.";

        shareMsg.textContent = data.collaboration_note ||
            "We generate an anonymized alert about this pattern — sudden foreign attempt right after a domestic purchase, on a new device — and share only that pattern with partner banks. That helps them stop the same attacker without sharing who you are.";

        // 3. animate needle sweep to final angle
        // map score 0..100 to -90..+90 degrees
        const finalAngle = -90 + (score100 / 100) * 180;
        setTimeout(() => {
            needleEl.style.transform = "rotate(" + finalAngle + "deg)";
        }, 50);

        // 4. after needle lands (~600ms), fade in score and count up
        setTimeout(() => {
            scoreFadeWrapper.classList.add("show");

            let current = 0;
            const step = Math.max(1, Math.round(score100 / 20)); // ~20 increments
            const interval = setInterval(() => {
                current += step;
                if (current >= score100) {
                    current = score100;
                    clearInterval(interval);
                }
                scoreEl.textContent = current.toString();
            }, 20);
        }, 650);

        // 5. stagger content reveal for drama
        setTimeout(() => {
            gaugeReveal.classList.add("show");
        }, 200);
        setTimeout(() => {
            summaryReveal.classList.add("show");
        }, 400);
        setTimeout(() => {
            detailsReveal.classList.add("show");
        }, 600);
    });
})();
</script>

</body>
</html>
    """
