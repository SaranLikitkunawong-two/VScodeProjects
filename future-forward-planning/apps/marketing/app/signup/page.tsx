import { CheckIcon } from "@/components/Icons";
import Footer from "@/components/Footer";
import SignupForm from "@/components/SignupForm";

export default function SignupPage() {
  return (
    <main id="main">
      <section className="section">
        <div className="container">
          <div className="signup-wrap">
            <div className="signup-copy">
              <span className="eyebrow">Join the waitlist</span>
              <h1>Be among the first to try Future Forward Planning.</h1>
              <p className="lede">
                We&apos;re onboarding a small group of participants this quarter. Share a few details and we&apos;ll
                reach out when a spot opens in your area.
              </p>
              <ul className="signup-list">
                <li>
                  <span className="tick">
                    <CheckIcon />
                  </span>
                  No cost to you — plan management is fully NDIS-funded.
                </li>
                <li>
                  <span className="tick">
                    <CheckIcon />
                  </span>
                  A 15-minute intro call, no commitment.
                </li>
                <li>
                  <span className="tick">
                    <CheckIcon />
                  </span>
                  We&apos;ll never share your details with providers.
                </li>
              </ul>
            </div>

            <SignupForm />
          </div>
        </div>
      </section>
      <Footer />
    </main>
  );
}
