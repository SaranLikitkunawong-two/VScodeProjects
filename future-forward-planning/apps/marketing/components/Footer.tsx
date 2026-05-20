import Link from "next/link";

function Brand() {
  return (
    <Link className="brand" href="/">
      <span className="brand-mark" aria-hidden></span>
      <span>Future Forward Planning</span>
    </Link>
  );
}

export default function Footer() {
  return (
    <footer className="footer" role="contentinfo">
      <div className="container">
        <div className="cols">
          <div>
            <Brand />
            <p className="fine" style={{ marginTop: 12 }}>
              Independent NDIS plan management for Australian participants. Future Forward Planning
              pays your providers, tracks your plan, and keeps your records straight.
            </p>
          </div>
          <div>
            <h5>Product</h5>
            <Link href="/#how">How we help</Link>
            <Link href="/#calc">Budget tool</Link>
            <Link href="/signup">Join the waitlist</Link>
          </div>
          <div>
            <h5>Resources</h5>
            <Link href="/news">News &amp; updates</Link>
            <Link href="/news">Participant guides</Link>
            <Link href="/news">For referrers</Link>
            <Link href="/privacy">Privacy policy</Link>
          </div>
          <div>
            <h5>Contact</h5>
            <a href="mailto:saranl@futureforwardplanning.com.au">saranl@futureforwardplanning.com.au</a>
            <span style={{ display: "block", padding: "6px 0", fontSize: 14 }}>Melbourne, VIC</span>
          </div>
        </div>
        <div className="bottom">
          <span>© 2026 SC Partnering Pty Ltd trading as Future Forward Planning. ABN 24 697 821 408.</span>
          <span>Registered NDIS plan manager (coming soon)</span>
        </div>
      </div>
    </footer>
  );
}
