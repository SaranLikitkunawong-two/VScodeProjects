"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowIcon, CheckIcon, InfoIcon } from "./Icons";

type Role = "" | "participant" | "family" | "support_coordinator" | "provider" | "other";

type FormValues = {
  first: string;
  email: string;
  phone: string;
  role: Role;
};

type FormErrors = Partial<Record<keyof FormValues | "submit", string>>;

export default function SignupForm() {
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [values, setValues] = useState<FormValues>({ first: "", email: "", phone: "", role: "" });
  const [errors, setErrors] = useState<FormErrors>({});

  const onChange = <K extends keyof FormValues>(k: K, v: FormValues[K]) => {
    setValues((s) => ({ ...s, [k]: v }));
    if (errors[k]) setErrors((e) => ({ ...e, [k]: undefined }));
  };

  const validate = (): FormErrors => {
    const e: FormErrors = {};
    if (!values.first.trim()) e.first = "Please enter your first name.";
    if (!values.email.trim()) e.email = "Please enter your email.";
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(values.email.trim())) e.email = "That doesn't look like a valid email.";
    if (values.phone && !/^[\d\s+()-]{6,}$/.test(values.phone.trim())) e.phone = "Use digits, spaces, +, -, () only.";
    if (!values.role) e.role = "Please tell us which best describes you.";
    return e;
  };

  const submit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    const e = validate();
    setErrors(e);
    if (Object.keys(e).length) {
      const first = Object.keys(e)[0] as keyof FormValues;
      document.getElementById(`signup-${first}`)?.focus();
      return;
    }
    setSubmitting(true);
    try {
      const res = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          firstName: values.first.trim(),
          email: values.email.trim(),
          phone: values.phone.trim() || null,
          role: values.role,
        }),
      });
      const data = await res.json();
      if (!res.ok || !data.success) {
        setErrors({ submit: data.error || "Something went wrong. Please try again." });
        setSubmitting(false);
        return;
      }
      setSubmitted(true);
    } catch {
      setErrors({ submit: "Network error. Please try again." });
      setSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="form-card">
        <div className="success" role="status" aria-live="polite">
          <div className="check">
            <CheckIcon width="28" height="28" />
          </div>
          <h2>You&apos;re on the list.</h2>
          <p>
            Thanks{values.first ? `, ${values.first}` : ""} — we&apos;ve got your details. We&apos;ll email{" "}
            {values.email || "you"} as soon as a spot opens up.
          </p>
          <div style={{ display: "flex", gap: 10, marginTop: 20, flexWrap: "wrap" }}>
            <Link className="btn btn-secondary" href="/">
              Back to home
            </Link>
            <Link className="btn btn-ghost" href="/news">
              Read our updates <ArrowIcon />
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="form-card">
      <form onSubmit={submit} noValidate>
        <h2>Register your interest</h2>
        <p className="sub">Takes under a minute.</p>

        <div className="field">
          <label htmlFor="signup-first">First name</label>
          <input
            id="signup-first"
            type="text"
            autoComplete="given-name"
            className={`input ${errors.first ? "has-error" : ""}`}
            value={values.first}
            onChange={(e) => onChange("first", e.target.value)}
            aria-invalid={!!errors.first}
            aria-describedby={errors.first ? "err-first" : undefined}
          />
          {errors.first && (
            <div id="err-first" className="error">
              <InfoIcon />
              {errors.first}
            </div>
          )}
        </div>

        <div className="field">
          <label htmlFor="signup-email">Email</label>
          <input
            id="signup-email"
            type="email"
            autoComplete="email"
            inputMode="email"
            className={`input ${errors.email ? "has-error" : ""}`}
            value={values.email}
            onChange={(e) => onChange("email", e.target.value)}
            placeholder="you@example.com"
            aria-invalid={!!errors.email}
            aria-describedby={errors.email ? "err-email" : undefined}
          />
          {errors.email && (
            <div id="err-email" className="error">
              <InfoIcon />
              {errors.email}
            </div>
          )}
        </div>

        <div className="field">
          <label htmlFor="signup-role">I am a&hellip;</label>
          <select
            id="signup-role"
            className={`input ${errors.role ? "has-error" : ""}`}
            value={values.role}
            onChange={(e) => onChange("role", e.target.value as Role)}
            aria-invalid={!!errors.role}
            aria-describedby={errors.role ? "err-role" : undefined}
          >
            <option value="">Select one&hellip;</option>
            <option value="participant">NDIS participant</option>
            <option value="family">Family member or carer</option>
            <option value="support_coordinator">Support coordinator</option>
            <option value="provider">Service provider</option>
            <option value="other">Something else</option>
          </select>
          {errors.role && (
            <div id="err-role" className="error">
              <InfoIcon />
              {errors.role}
            </div>
          )}
        </div>

        <div className="field">
          <label htmlFor="signup-phone">
            Phone <span style={{ color: "var(--ink-3)", fontWeight: 400 }}>(optional)</span>
          </label>
          <input
            id="signup-phone"
            type="tel"
            autoComplete="tel"
            inputMode="tel"
            className={`input ${errors.phone ? "has-error" : ""}`}
            value={values.phone}
            onChange={(e) => onChange("phone", e.target.value)}
            placeholder="04xx xxx xxx"
            aria-invalid={!!errors.phone}
            aria-describedby={errors.phone ? "err-phone" : "hint-phone"}
          />
          {errors.phone ? (
            <div id="err-phone" className="error">
              <InfoIcon />
              {errors.phone}
            </div>
          ) : (
            <div id="hint-phone" className="hint" style={{ marginTop: 6 }}>
              If you&apos;d prefer a call back.
            </div>
          )}
        </div>

        <button type="submit" className="btn btn-primary btn-lg btn-block" disabled={submitting}>
          {submitting ? "Submitting…" : (<>Join the waitlist <ArrowIcon /></>)}
        </button>

        {errors.submit && (
          <div className="error" style={{ marginTop: 12 }}>
            <InfoIcon />
            {errors.submit}
          </div>
        )}

        <p className="form-meta">
          By registering, you agree to receive occasional updates from Future Forward Planning. We&apos;ll never share
          your information and you can unsubscribe any time. See our <Link href="/privacy">Privacy Policy</Link>.
        </p>
      </form>
    </div>
  );
}
