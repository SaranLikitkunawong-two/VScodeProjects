import Link from "next/link";
import Footer from "@/components/Footer";

export const metadata = {
  title: "Privacy Policy — Future Forward Planning",
  description:
    "How Future Forward Planning collects, uses, stores, and protects your personal information under the Australian Privacy Act 1988.",
};

export default function PrivacyPage() {
  return (
    <main id="main">
      <section className="section" style={{ paddingTop: 72 }}>
        <div className="container" style={{ maxWidth: 760 }}>
          <span className="eyebrow">Legal</span>
          <h1 style={{ fontSize: "clamp(32px, 3.4vw, 44px)" }}>Privacy Policy</h1>
          <p className="lede">
            Future Forward Planning is committed to protecting the personal information you share with us. This policy
            sets out how we collect, use, store, and disclose information in line with the{" "}
            <em>Privacy Act 1988</em> (Cth) and the Australian Privacy Principles (APPs).
          </p>
          <p style={{ fontSize: 13, color: "var(--ink-3)" }}>
            Last updated: 20 May 2026 · Effective: 20 May 2026
          </p>

          <h2 style={{ marginTop: 48 }}>1. Who we are</h2>
          <p>
            &ldquo;Future Forward Planning&rdquo; is a trading name of SC Partnering Pty Ltd (ABN 24 697 821 408), an
            Australian proprietary limited company providing NDIS plan management services. Our registered office is in
            Melbourne, Victoria. References to &ldquo;we&rdquo;, &ldquo;our&rdquo; and &ldquo;us&rdquo; in this policy
            mean SC Partnering Pty Ltd.
          </p>

          <h2 style={{ marginTop: 32 }}>2. Personal information we collect</h2>
          <p>Through this website we collect only the information you choose to give us, including:</p>
          <ul className="article-points" style={{ margin: "16px 0 24px" }}>
            <li>Your first name (required for the waitlist signup form).</li>
            <li>Your email address (required so we can contact you).</li>
            <li>Your phone number (optional, used only if you ask us to call back).</li>
            <li>How you describe your relationship to the NDIS (participant, family member, support coordinator, service provider, or other).</li>
          </ul>
          <p>
            We may also receive limited anonymous technical information (such as device type, browser, and pages viewed)
            via Vercel Analytics. This analytics service does not use cookies and does not collect any personal
            information that identifies you.
          </p>

          <h2 style={{ marginTop: 32 }}>3. How we use your information</h2>
          <p>We use the information you provide for the following purposes:</p>
          <ul className="article-points" style={{ margin: "16px 0 24px" }}>
            <li>To contact you about our plan management services and respond to your enquiry.</li>
            <li>To notify you when a place becomes available on our waitlist.</li>
            <li>To occasionally send relevant updates about NDIS plan management (only if you have asked to receive them).</li>
            <li>To improve our website and services.</li>
          </ul>
          <p>
            We do not sell, rent, or trade your personal information. We do not share your information with service
            providers, third parties, or marketing networks.
          </p>

          <h2 style={{ marginTop: 32 }}>4. Where your information is stored</h2>
          <p>
            Waitlist data is stored in a managed PostgreSQL database hosted by Supabase, with the data centre located in
            Sydney, Australia. Your information stays on Australian soil under Australian Privacy Act protections. The
            database is encrypted at rest and accessed only by authorised personnel of SC Partnering Pty Ltd.
          </p>

          <h2 style={{ marginTop: 32 }}>5. How long we keep your information</h2>
          <p>
            We keep waitlist information for as long as you remain on the waitlist or as a Future Forward Planning
            participant or contact. You can request deletion of your information at any time (see Section 7). Where we
            are required to retain records for taxation, regulatory, or NDIS compliance purposes, those retention
            obligations override deletion requests for the relevant records — currently up to 7 years for invoice-
            related records (an ATO and NDIS Commission requirement).
          </p>

          <h2 style={{ marginTop: 32 }}>6. Cookies and tracking</h2>
          <p>
            This website does not use marketing or advertising cookies. We do not run third-party tracking pixels (e.g.
            Facebook, Google Ads). Vercel Analytics provides aggregate, anonymous usage information without setting
            cookies on your browser.
          </p>

          <h2 style={{ marginTop: 32 }}>7. Your rights</h2>
          <p>You have the following rights under the Australian Privacy Principles:</p>
          <ul className="article-points" style={{ margin: "16px 0 24px" }}>
            <li>Access — request a copy of the personal information we hold about you.</li>
            <li>Correction — ask us to correct any information that is inaccurate, incomplete, or out of date.</li>
            <li>Deletion — ask us to delete your personal information, subject to lawful retention obligations.</li>
            <li>Withdraw consent — opt out of further communications at any time.</li>
            <li>Complain — raise a privacy concern directly with us, or with the Office of the Australian Information Commissioner (OAIC) at <a href="https://www.oaic.gov.au" target="_blank" rel="noreferrer">oaic.gov.au</a>.</li>
          </ul>

          <h2 style={{ marginTop: 32 }}>8. Contact us</h2>
          <p>
            To exercise any of these rights, or to ask a question about how your information is handled, please email{" "}
            <a href="mailto:saranl@futureforwardplanning.com.au">saranl@futureforwardplanning.com.au</a>. We aim to
            respond to all privacy requests within 30 days.
          </p>

          <h2 style={{ marginTop: 32 }}>9. Changes to this policy</h2>
          <p>
            We may update this Privacy Policy from time to time. The current version will always be available at this
            page, with the &ldquo;Last updated&rdquo; date reflected at the top.
          </p>

          <div style={{ marginTop: 48 }}>
            <Link className="btn btn-secondary" href="/">
              ← Back to home
            </Link>
          </div>
        </div>
      </section>
      <Footer />
    </main>
  );
}
