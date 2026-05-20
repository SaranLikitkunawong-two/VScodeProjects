/* Sign up page */

function SignupPage() {
  const [submitted, setSubmitted] = React.useState(false);
  const [submitting, setSubmitting] = React.useState(false);
  const [values, setValues] = React.useState({ first: '', email: '', phone: '' });
  const [errors, setErrors] = React.useState({});

  const onChange = (k, v) => {
    setValues(s => ({...s, [k]: v}));
    if (errors[k]) setErrors(e => ({...e, [k]: null}));
  };

  const validate = () => {
    const e = {};
    if (!values.first.trim()) e.first = 'Please enter your first name.';
    if (!values.email.trim()) e.email = 'Please enter your email.';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email.trim())) e.email = 'That doesn\u2019t look like a valid email.';
    if (values.phone && !/^[\d\s+()-]{6,}$/.test(values.phone.trim())) e.phone = 'Use digits, spaces, +, -, () only.';
    return e;
  };

  const submit = (ev) => {
    ev.preventDefault();
    const e = validate();
    setErrors(e);
    if (Object.keys(e).length) {
      const first = Object.keys(e)[0];
      document.getElementById(`signup-${first}`)?.focus();
      return;
    }
    setSubmitting(true);
    // Simulate network
    setTimeout(() => {
      setSubmitting(false);
      setSubmitted(true);
    }, 700);
  };

  return (
    <main id="main">
      <section className="section">
        <div className="container">
          <div className="signup-wrap">
            <div className="signup-copy">
              <span className="eyebrow">Join the waitlist</span>
              <h1>Be among the first to try Future Forward Planning.</h1>
              <p className="lede">
                We're onboarding a small group of participants this quarter.
                Share a few details and we'll reach out when a spot opens in your area.
              </p>
              <ul className="signup-list">
                <li><span className="tick"><Icon.check/></span>No cost to you — plan management is fully NDIS-funded.</li>
                <li><span className="tick"><Icon.check/></span>A 15-minute intro call, no commitment.</li>
                <li><span className="tick"><Icon.check/></span>We'll never share your details with providers.</li>
              </ul>
            </div>

            <div className="form-card">
              {!submitted ? (
                <form onSubmit={submit} noValidate>
                  <h2>Register your interest</h2>
                  <p className="sub">Takes under a minute.</p>

                  <div className="field">
                    <label htmlFor="signup-first">First name</label>
                    <input
                      id="signup-first" type="text" autoComplete="given-name"
                      className={`input ${errors.first?'has-error':''}`}
                      value={values.first}
                      onChange={e => onChange('first', e.target.value)}
                      aria-invalid={!!errors.first}
                      aria-describedby={errors.first?'err-first':undefined}
                    />
                    {errors.first && <div id="err-first" className="error"><Icon.info/>{errors.first}</div>}
                  </div>

                  <div className="field">
                    <label htmlFor="signup-email">Email</label>
                    <input
                      id="signup-email" type="email" autoComplete="email" inputMode="email"
                      className={`input ${errors.email?'has-error':''}`}
                      value={values.email}
                      onChange={e => onChange('email', e.target.value)}
                      placeholder="you@example.com"
                      aria-invalid={!!errors.email}
                      aria-describedby={errors.email?'err-email':undefined}
                    />
                    {errors.email && <div id="err-email" className="error"><Icon.info/>{errors.email}</div>}
                  </div>

                  <div className="field">
                    <label htmlFor="signup-phone">
                      Phone <span style={{color:'var(--ink-3)', fontWeight: 400}}>(optional)</span>
                    </label>
                    <input
                      id="signup-phone" type="tel" autoComplete="tel" inputMode="tel"
                      className={`input ${errors.phone?'has-error':''}`}
                      value={values.phone}
                      onChange={e => onChange('phone', e.target.value)}
                      placeholder="04xx xxx xxx"
                      aria-invalid={!!errors.phone}
                      aria-describedby={errors.phone?'err-phone':'hint-phone'}
                    />
                    {errors.phone
                      ? <div id="err-phone" className="error"><Icon.info/>{errors.phone}</div>
                      : <div id="hint-phone" className="hint" style={{marginTop: 6}}>If you'd prefer a call back.</div>}
                  </div>

                  <button type="submit" className="btn btn-primary btn-lg btn-block" disabled={submitting}>
                    {submitting ? 'Submitting\u2026' : <>Join the waitlist <Icon.arrow/></>}
                  </button>

                  <p className="form-meta">
                    By registering, you agree to receive occasional updates from Future Forward Planning.
                    We'll never share your information and you can unsubscribe any time.
                  </p>
                </form>
              ) : (
                <div className="success" role="status" aria-live="polite">
                  <div className="check"><Icon.check width="28" height="28"/></div>
                  <h2>You're on the list.</h2>
                  <p>
                    Thanks{values.first ? `, ${values.first}` : ''} — we've got your details.
                    We'll email {values.email || 'you'} as soon as a spot opens up.
                  </p>
                  <div style={{display:'flex', gap: 10, marginTop: 20, flexWrap:'wrap'}}>
                    <a className="btn btn-secondary" href="#/" onClick={(e)=>{e.preventDefault(); window.navigate('home');}}>
                      Back to home
                    </a>
                    <a className="btn btn-ghost" href="#/news" onClick={(e)=>{e.preventDefault(); window.navigate('news');}}>
                      Read our updates <Icon.arrow/>
                    </a>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </main>
  );
}

Object.assign(window, { SignupPage });
