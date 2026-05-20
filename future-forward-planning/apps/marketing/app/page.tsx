import Link from "next/link";
import { ArrowIcon } from "@/components/Icons";
import HeroArt from "@/components/HeroArt";
import BudgetCalculator from "@/components/BudgetCalculator";
import Footer from "@/components/Footer";

export default function HomePage() {
  return (
    <main id="main">
      <section className="hero" aria-labelledby="hero-title">
        <div className="container">
          <div className="hero-inner">
            <div>
              <span className="eyebrow eyebrow-on-slate">NDIS plan management</span>
              <h1 id="hero-title">A calmer way to run your NDIS plan.</h1>
              <p className="lede">
                Future Forward Planning is an independent plan manager for Australian NDIS participants. We pay your
                providers within two business days, keep your budget in plain view, and answer when you call — so you
                can focus on the supports that matter.
              </p>
              <div className="hero-cta">
                <Link className="btn btn-primary btn-lg" href="/signup">
                  Join the waitlist <ArrowIcon />
                </Link>
                <Link className="btn btn-on-slate btn-lg" href="#how">
                  See how it works
                </Link>
              </div>
              <div className="hero-meta">
                <span>
                  <span className="dot"></span>Self-managed &amp; plan-managed budgets
                </span>
                <span>
                  <span className="dot"></span>Two-day invoice turnaround
                </span>
                <span>
                  <span className="dot"></span>No cost to participants
                </span>
              </div>
            </div>
            <HeroArt variant="plan" />
          </div>
        </div>
      </section>

      <section className="section" id="calc" aria-labelledby="calc-title">
        <div className="container">
          <div style={{ maxWidth: 640, marginBottom: 40 }}>
            <span className="eyebrow">Budget tool</span>
            <h2 id="calc-title">Track spending with more confidence.</h2>
            <p className="lede">
              See your whole plan at a glance, then drill into Core, Capacity, or Capital supports — each with the
              cadence that actually fits how it&apos;s used.
            </p>
          </div>
          <BudgetCalculator />
          <p style={{ fontSize: 13, color: "var(--ink-3)", marginTop: 16, maxWidth: 640 }}>
            Calculator is illustrative only. Actual plan spending depends on category limits, provider rates, and the
            NDIA&apos;s current pricing arrangements.
          </p>
        </div>
      </section>

      <section className="section" id="how" aria-labelledby="how-title">
        <div className="container">
          <span className="eyebrow">How we help</span>
          <h2 id="how-title" style={{ maxWidth: "20ch" }}>
            Three things a good plan manager should do — and we do them well.
          </h2>
          <p className="lede" style={{ marginBottom: 48 }}>
            Plan management is mostly invoices, records, and timely answers. We&apos;ve built Future Forward Planning
            around doing those three things carefully.
          </p>
          <div className="grid-3">
            <article className="card card-pad help-card">
              <div className="num">01</div>
              <h3>Pay providers, promptly</h3>
              <p>
                Forward an invoice and we handle claims with the NDIA and pay providers within two business days.
                You&apos;ll see every payment as it happens.
              </p>
            </article>
            <article className="card card-pad help-card">
              <div className="num">02</div>
              <h3>Keep your budget visible</h3>
              <p>
                A clear monthly statement, live category balances, and a simple projection so you know whether
                you&apos;re on pace — not only when a review comes up.
              </p>
            </article>
            <article className="card card-pad help-card">
              <div className="num">03</div>
              <h3>Answer when you call</h3>
              <p>
                A named plan manager who knows your situation. No ticket queues, no bouncing between agents. Phone or
                email during business hours.
              </p>
            </article>
          </div>
        </div>
      </section>

      <section className="section-tight" style={{ background: "var(--slate-50)" }} aria-labelledby="pm-title">
        <div className="container">
          <div className="split">
            <div>
              <span className="eyebrow">The basics</span>
              <h2 id="pm-title">What is NDIS plan management?</h2>
              <p className="lede">
                Plan management is a funded support under your NDIS plan. A plan manager sits between you and your
                providers — we claim from the NDIA, pay invoices, and keep your records — while you keep full choice
                over who you work with.
              </p>
              <p style={{ color: "var(--ink-3)" }}>
                It&apos;s free for participants. When your plan is built, ask your planner to include &ldquo;Improved
                Life Choices&rdquo; (the category that funds plan management) and you can choose Future Forward Planning
                — or switch to us at any time.
              </p>
            </div>
            <div className="card card-pad">
              <h3 style={{ marginBottom: 8 }}>What&apos;s included</h3>
              <ul className="checklist">
                <li>Claim and pay invoices from any registered or unregistered provider</li>
                <li>Monthly statements plus real-time balances by category</li>
                <li>A named plan manager, reachable by phone or email</li>
                <li>Help reading your plan and understanding your categories</li>
                <li>Reminders before your plan review so nothing is rushed</li>
                <li>Secure record-keeping for audits and reassessments</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <section className="section-tight about-bg" aria-labelledby="about-title">
        <div className="container">
          <div className="split">
            <div>
              <span className="eyebrow">About us</span>
              <h2 id="about-title">Independent, local, and built for the long haul.</h2>
            </div>
            <div className="about-body">
              <p>
                Future Forward Planning is run by Saran Likitkunawong, a Chartered Accountant (CA ANZ) based in
                Melbourne. After years working with small businesses on the financial controls and reporting that keep
                them honest, the decision to build a plan management practice came from a simple observation: the
                discipline that good accountants bring to record-keeping and reconciliation is exactly what NDIS
                participants need from a plan manager.
              </p>
              <p>
                We&apos;re deliberately small. Every participant has a single, named point of contact — not a ticket
                queue — and a portal that shows the same numbers we&apos;re looking at. No black-box dashboards, no
                surprise statements, and no &ldquo;your invoice is in the system somewhere&rdquo; phone calls. If we
                approve it, you see it. If we hold it, you see why.
              </p>
              <div className="about-meta">
                <div className="stat">
                  <div className="k">Founded</div>
                  <div className="v">2026</div>
                </div>
                <div className="stat">
                  <div className="k">Based in</div>
                  <div className="v">Melbourne</div>
                </div>
                <div className="stat">
                  <div className="k">Team</div>
                  <div className="v">Small &amp; growing</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section-tight" aria-labelledby="cta-title">
        <div className="container">
          <div className="cta-band">
            <div>
              <h2 id="cta-title">We&apos;re opening to a small group of participants first.</h2>
              <p>Join the waitlist and we&apos;ll be in touch when we&apos;re ready for new plans in your area.</p>
            </div>
            <div className="cta-actions">
              <Link className="btn btn-on-slate btn-lg" href="/signup">
                Register interest <ArrowIcon />
              </Link>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </main>
  );
}
