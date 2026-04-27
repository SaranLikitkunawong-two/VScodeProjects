# NDIS Plan Management — Marketing and Client Acquisition Plan

**Business:** [Business Name]
**ABN:** 20 931 095 007
**Location:** Melbourne, Victoria
**Date:** April 2026
**Version:** 1.0

> **Compliance note:** All marketing activities must comply with Policy PM-POL-016 (Marketing, Referrals and Anti-Inducement). No referral fees, no inducements, no predatory outreach. The NDIS Amendment (Integrity and Safeguarding) Act 2025 gives the NDIS Commission power to issue anti-promotion orders. Every channel and tactic in this plan is compliant.

---

## Strategic Context

**Timing:** This plan activates toward the end of the registration process — ideally 4–6 weeks before your audit outcome is expected, so your online presence is live and polished when your registration is confirmed.

**Your unfair advantages:**
1. **CA ANZ qualified** — Most plan managers are bookkeepers. Being a Chartered Accountant is a genuine credential differentiator that participants and support coordinators notice.
2. **Custom participant portal** (Next.js + Supabase + Google Document AI) — Real-time budget visibility and OCR invoice processing. No competitor in your size category has this. It is your single most powerful marketing point.
3. **Small and responsive** — Participants get the actual qualified person managing their plan, not a call centre. Sole-operator responsiveness is a real advantage against the large platforms (My Plan Manager, Plan Partners, etc.).
4. **Melbourne-based** — Local presence matters to many participants and families.

**Your target market:**
- NDIS participants (any disability, any age) who are currently NDIA-managed and want more provider flexibility
- NDIS participants currently with a large, impersonal plan manager who want a more responsive service
- New NDIS participants setting up their first plan management arrangement
- Participants referred by support coordinators or LACs in the Melbourne metro area

**Realistic growth target:**
- Months 1–3: 0–5 participants (referrals, word of mouth, profile listings going live)
- Months 4–12: 10–30 participants (content marketing building, Google profile gaining reviews)
- Year 2: 30–80 participants (SEO content maturing, referral network established)

> The plan management support item pays approximately $124.57/month per participant (verify current PAPL rate). 50 participants = ~$6,200/month recurring revenue before any other income.

---

## Phase Overview

| Phase | Timing | Focus | Cost |
|-------|--------|-------|------|
| 1 — Foundation | Weeks 1–4 (pre-audit outcome) | Domain, website, Google Business Profile | ~$50–200 |
| 2 — Content & SEO | Weeks 3–16 | Knowledge articles, on-page SEO | Time only |
| 3 — Directories & Profiles | Weeks 2–8 | NDIS directories, LinkedIn, Facebook | Free |
| 4 — Referral Network | Weeks 6–ongoing | Support coordinators, LACs, DIA network | Time only |
| 5 — Community | Weeks 8–ongoing | Expos, Facebook groups, local networks | $200–500/event |

---

---

# Phase 1: Online Foundation

## 1.1 Domain Name

Register your domain before your business name is finalised if possible — domains are cheap and you can redirect later.

**Recommended approach:**
- Use Namecheap or Cloudflare Registrar (~$15–20 AUD/year for a `.com.au`)
- Target: `[businessname].com.au` — the `.com.au` signals Australian business and ranks better locally
- Fallback: `[businessname].com.au` taken → try `[businessname]planmanagement.com.au` or similar

**What to avoid in your domain:**
- Don't use competitor names
- Don't use "NDIS" as a standalone word if it might imply NDIA affiliation
- Keep it short and spellable over the phone

---

## 1.2 Website

Since you're building the participant portal in Next.js, your marketing website can be the same codebase or a separate static site. Given that the portal is an internal tool, a separate lightweight public site is cleaner.

**Recommended stack for the marketing site:**
- **Next.js 15** (you already know it) with static export, deployed to Vercel
- Free on Vercel for a personal/small project — no hosting cost
- Custom domain connected via Cloudflare (free DNS + SSL)

### Website Page Structure

| Page | URL | Primary Purpose | SEO Target |
|------|-----|----------------|-----------|
| Home | `/` | First impression, value proposition, CTA | "NDIS plan manager Melbourne" |
| How It Works | `/how-it-works` | Explain plan management, build trust | "how does NDIS plan management work" |
| Why Us | `/about` | CA ANZ credential, portal tech, personal story | Brand/trust |
| Our Technology | `/portal` | The participant portal as a differentiator | "NDIS plan management portal real-time" |
| Pricing & Fees | `/pricing` | Transparency — no out-of-pocket fees | "NDIS plan management fees" |
| FAQ | `/faq` | Answer common questions, reduce friction | Long-tail keyword capture |
| Resources / Blog | `/resources` | Knowledge articles — SEO engine | Multiple article-specific keywords |
| Contact / Get Started | `/contact` | Lead capture | "NDIS plan manager contact Melbourne" |
| Privacy Policy | `/privacy` | Legal requirement | — |

---

### Page Content Guide

#### Home Page

**Hero section:**
```
Headline: "NDIS Plan Management — Handled by a Chartered Accountant"
Subheadline: "Real-time budget tracking, fast invoice processing, and a human
              you can actually call. Based in Melbourne."
CTA Button: "Get Started — It's Free" → /contact
```

**Three value pillars (icons + short copy):**
1. **CA ANZ Qualified** — Your plan budget is managed by a qualified Chartered Accountant, not a call centre.
2. **Real-Time Portal** — Log in anytime to see exactly how your NDIS budget is tracking — by category, live.
3. **Fast Payments** — Providers are paid within 3–5 business days. No waiting, no chasing.

**How it works (3-step summary):**
1. Sign up — takes 15 minutes, no paperwork hassle
2. Connect your NDIS plan — we get access through the NDIA portal
3. We handle your invoices — you focus on your life

**Social proof section (once you have participants):**
- Testimonials with consent (see PM-POL-016 Section 6) — see Appendix A for example testimonial copy and format
- Number of participants managed, invoices processed

**Final CTA:**
```
"Plan management is included in your NDIS plan at no out-of-pocket cost.
 Switch today — or start fresh. Takes 15 minutes."
[Get Started Button]
```

---

#### How It Works Page

Cover the three key questions every new participant has:

**Section 1: What is plan management?**
- The NDIA pays a plan manager to handle your invoices and track your budget
- You keep control of your plan; we handle the admin
- You can use both registered AND unregistered providers (this is a key benefit vs NDIA-managed)

**Section 2: What does a plan manager actually do?**
- Receive and verify invoices from your providers
- Submit claims to the NDIA on your behalf
- Pay your providers directly (you don't need to pay and claim back)
- Send you a monthly statement showing every transaction
- Alert you when a budget category is getting low
- Answer your questions about your budget

**Section 3: How do I get plan management?**
- If plan management isn't already in your plan, ask your LAC or planner to include "Improved Life Choices — Plan Management" in your next plan
- If it's already in your plan: contact us to switch or start

**Section 4: What does it cost?**
- Nothing out of pocket. The NDIA funds your plan management at a set rate (~$124.57/month — verify current PAPL)
- We claim our fee from your plan management budget line — you never pay us directly

---

#### Our Technology Page

This is where your portal becomes your competitive weapon. No small plan manager has this.

**Headline:** "Your NDIS budget — live, transparent, and always in your hands"

**What your participants see in the portal:**
- Real-time budget by support category (not waiting for a monthly PDF)
- Every transaction as it happens — provider name, amount, date, category
- Budget tracking progress bars showing % remaining per category
- Invoice submission (participant can photograph and submit invoices via mobile)
- OCR-powered invoice processing — provider invoices are read automatically, reducing errors and delays

**Comparison table:**

| Feature | [Business Name] | Typical Large Plan Manager |
|---------|----------------|--------------------------|
| Budget visibility | Real-time, any time | Monthly statement only |
| Invoice processing | OCR-automated, 3–5 days | Manual, 5–10 days |
| Communication | Direct to qualified CA | Call centre / ticket system |
| Melbourne-based | Yes | Usually interstate operations |
| Who manages your plan | Named Chartered Accountant | Rotated staff |

---

#### Pricing & Fees Page

**Headline:** "Plan management costs you nothing out of pocket — ever"

**Explain clearly:**
- The NDIA sets the plan management fee (setup ~$233.45 + monthly ~$124.57 — verify current PAPL)
- This comes from your "Improved Life Choices" budget — a separate line item in your plan
- [Business Name] charges only the standard NDIS rate — no hidden fees, no add-ons
- If you don't currently have plan management in your plan, we can help you request it

**What's included:**
- Invoice receipt and verification
- NDIS claims submission (PACE portal)
- Provider payment within 3–5 business days
- Monthly financial statements
- Budget monitoring and alerts
- Real-time portal access (participant and nominee)
- Direct email/phone support from a qualified Chartered Accountant

---

#### FAQ Page

Write these as real questions you expect to be asked (each one is also an SEO entry point):

1. Can I switch plan managers without waiting for my plan renewal?
2. What providers can I use with plan management?
3. What's the difference between plan management and support coordination?
4. How quickly will my providers get paid?
5. What happens if my budget runs out before my plan renews?
6. Can a family member or carer manage the plan management relationship on my behalf?
7. Do I need to approve every invoice before it gets paid?
8. What happens to my records if I switch plan managers?
9. Is my personal information secure?
10. How do I sign up?
11. Can I use plan management if I'm already self-managing part of my plan?
12. What if a provider charges more than the NDIS price limit?

---

#### Contact / Get Started Page

**Keep it simple:**
- Short form: Name, email, phone, NDIS number (optional), current plan management arrangement (NDIA-managed / existing plan manager / new to NDIS)
- Set expectation: "We'll be in touch within 1 business day"
- Secondary option: Book a call via Calendly (free plan)

**Reassure them:**
- "Switching is free and easy — we handle the admin"
- "No lock-in contracts"
- "Takes about 15 minutes to get started"

---

## 1.3 Google Business Profile

Google Business Profile (GBP) is the single most important free marketing tool for a local service business. When someone searches "NDIS plan manager Melbourne," the map listings appear above organic results.

### Setup Steps

1. Go to business.google.com — sign in with your business Google account
2. Add business name: [Business Name]
3. **Business category:** Start with "Financial Planner" as the primary (there is no specific NDIS Plan Manager category). Add "Disability Services Australia" as a secondary if available in your region.
4. Add your Melbourne service area (you serve Greater Melbourne — do not add a physical storefront address unless you have a physical office; GBP supports service-area-only businesses)
5. Add phone number, website URL, and business hours
6. Add business description (see below)
7. Upload a profile photo (professional headshot or logo) and a cover photo
8. Add services: "NDIS Plan Management", "NDIS Budget Tracking", "NDIS Invoice Processing"

### Business Description (150 words, optimised for Google)

```
[Business Name] provides NDIS plan management services across Greater Melbourne.
Managed by a qualified Chartered Accountant (CA ANZ), we handle invoice processing,
NDIS claims, and provider payments on behalf of participants — at no out-of-pocket cost.

Our custom participant portal gives you real-time visibility of your NDIS budget, 24/7
— not just a monthly statement. Providers are paid within 3–5 business days.

We work with participants of all ages and disability types across Melbourne, processing
invoices from both registered and unregistered NDIS providers.

Plan management is funded through your NDIS plan at no cost to you.
Switching from another plan manager is straightforward and takes 15 minutes.

Contact us today to get started or ask a question — we respond within 1 business day.
```

### Getting Google Reviews

Reviews are the primary ranking factor for local Google Business results. Strategy:
- Ask every participant to leave a review after 1–2 months of smooth service
- Make it easy: send them the direct Google review link (get it from your GBP dashboard)
- Respond to every review (positive and negative) within 24 hours — Google ranks businesses that engage
- Target: 10+ reviews in the first 6 months; 20+ by end of Year 1

> **Compliance reminder (PM-POL-016):** Never offer anything in exchange for a review. Never write fake reviews. Never ask family or friends who aren't actual participants. Google and the NDIS Commission both treat fake reviews seriously.

### Google Business Profile — Ongoing Maintenance

- Post an update at least once per fortnight (share a knowledge article, NDIS tip, or business news)
- Add photos periodically (office, team, events — never participant photos without explicit written consent)
- Answer the Q&A section — Google allows anyone to ask questions on your profile; answer them promptly
- Monitor and respond to reviews weekly

---

---

# Phase 2: Knowledge Articles (SEO and Credibility)

## Why Knowledge Articles Work for NDIS Plan Management

NDIS participants, their families, and carers search Google constantly with questions like:
- "how do I switch NDIS plan managers"
- "what is the NDIS Pricing Arrangements"
- "can I use unregistered providers NDIS"

Most search results for these terms are dominated by the NDIA's own website, large plan management companies (My Plan Manager, Plan Partners), and generic disability sites. A small, well-written article from a CA-qualified Melbourne plan manager can rank for these terms — particularly the more specific, long-tail queries.

Articles also build credibility with support coordinators and LACs who refer participants. A support coordinator who Googles your name and finds well-written, accurate resources is far more likely to refer than one who finds nothing.

---

## Article Strategy

**Publishing cadence:** 1 article per fortnight for the first 6 months (12 articles). Then 1 per month ongoing.

**Length:** 1,000–2,000 words per article. Longer than competitors = better rankings + more trust.

**Format:** Each article should have:
- A clear headline with the keyword in it
- Subheadings (H2/H3) breaking the article into sections
- At least one table, list, or diagram
- A clear call to action at the end ("Have questions about your NDIS plan? Contact us.")
- Internal links to other articles on your site once you have 3+

**Distribution after publishing:**
- Share on your LinkedIn personal profile with a brief personal commentary
- Share on your Facebook Business Page
- Post as a Google Business Profile update
- Email to your existing participant list (once you have one)

---

## Article Outlines — 12 Articles to Write

---

### Article 1: "NDIS Plan Management Explained: What It Is and Why It's Free"

**Target keyword:** "NDIS plan management explained" / "what is NDIS plan management"
**Search intent:** Participants or families who have heard about plan management but don't fully understand it

**Outline:**
- What is plan management? (The plain English answer)
- The 3 ways to manage your NDIS funding (NDIA-managed, plan-managed, self-managed)
- Table comparing all 3 options across: provider choice, admin burden, flexibility, cost
- Why plan management costs you nothing extra (funded from your plan's Improved Life Choices budget)
- Who can have plan management (any participant — subject to plan inclusions)
- How to get plan management added to your plan if you don't have it yet
- CTA: "Want to start with a plan manager? Here's how it works."

---

### Article 2: "How to Switch NDIS Plan Managers: A Step-by-Step Guide"

**Target keyword:** "how to switch NDIS plan manager" / "change NDIS plan manager"
**Search intent:** Participants unhappy with their current plan manager

**Outline:**
- Can you switch plan managers? (Yes, at any time — you don't need to wait for plan renewal)
- Common reasons participants switch (slow payments, poor communication, no portal access, impersonal service)
- Step-by-step switching guide:
  1. Choose your new plan manager
  2. Sign a new service agreement
  3. New plan manager contacts current plan manager (or you notify NDIA via myplace/PACE)
  4. Transition of outstanding invoices
  5. New plan manager confirmed in PACE portal
- What happens to your records and outstanding invoices
- How long it takes (typically 5–10 business days)
- CTA: "Thinking of switching? Here's what to expect when you come to [Business Name]."

---

### Article 3: "10 Questions to Ask Before Choosing an NDIS Plan Manager"

**Target keyword:** "choosing NDIS plan manager" / "best NDIS plan manager Melbourne"
**Search intent:** Participants actively comparing plan managers

**Outline:**
- Introduction: Not all plan managers are the same — here's how to evaluate them
- The 10 questions (each with 2–3 sentences explaining what a good answer looks like):
  1. Are you a registered NDIS provider? (Should be yes — check the NDIS register)
  2. What are your qualifications? (Look for accounting, finance, or CA/CPA credentials)
  3. How quickly do you pay providers?
  4. Do you have a participant portal for real-time budget visibility?
  5. Who will actually be managing my plan — one person or a team?
  6. How do you handle budget alerts?
  7. What is your response time for queries?
  8. How do I submit invoices?
  9. Are there any fees beyond the NDIS plan management rate?
  10. What happens to my plan management if you close your business?
- CTA: "How does [Business Name] answer these questions? Here's our response to every one."

---

### Article 4: "Registered vs Unregistered NDIS Providers: What You Need to Know"

**Target keyword:** "unregistered NDIS provider plan management" / "registered vs unregistered NDIS"
**Search intent:** Participants who want to use providers not on the NDIS register

**Outline:**
- What is a registered NDIS provider?
- What is an unregistered NDIS provider?
- Which management type allows unregistered providers? (Plan-managed and self-managed — NOT NDIA-managed — this is a key reason to choose plan management)
- What supports can unregistered providers deliver?
- What plan managers check before paying an unregistered provider (ABN verification, banning register, participant confirmation)
- Common examples of unregistered providers (local cleaners, community transport, some allied health)
- The risks and how a good plan manager mitigates them
- CTA: "[Business Name] processes payments to both registered and unregistered providers — here's how."

---

### Article 5: "Understanding Your NDIS Plan Budget Categories"

**Target keyword:** "NDIS plan budget categories explained" / "NDIS core supports capacity building"
**Search intent:** Participants trying to understand their plan

**Outline:**
- Why understanding your categories matters (spending outside category = claim rejected)
- The three main budget types with their subcategories:
  - **Core Supports:** Daily Activities, Community Participation, Consumables, Assistance with Social, Economic & Community Participation
  - **Capacity Building:** Improved Daily Living, Improved Living Arrangements, Improved Life Choices (plan management), Improved Health and Wellbeing, Improved Learning, Improved Relations, Improved Employment, Support Coordination, Improved Life Choices
  - **Capital Supports:** Assistive Technology, Home Modifications
- Table: which categories are flexible across subcategories and which are locked
- How plan management fits in (Improved Life Choices — funded separately)
- What happens if you overspend a category before plan end
- CTA: "Not sure which category an invoice should go under? Your plan manager handles this — contact us."

---

### Article 6: "What is the NDIS Pricing Arrangements and Price Limits (PAPL)?"

**Target keyword:** "NDIS price guide" / "NDIS Pricing Arrangements Price Limits explained"
**Search intent:** Participants (and providers) trying to understand NDIS pricing rules

**Outline:**
- What the PAPL is and why it exists (price ceiling, not a price list)
- How often it changes (updated by NDIA, typically annually in July + ad hoc)
- How to find the current PAPL (link to NDIA page)
- Key pricing concepts: hourly rates, public holiday loadings, cancellation rules
- What happens if a provider charges over the PAPL (plan manager should reject the invoice)
- How plan managers protect participants from overcharging
- Why the price limit is a maximum, not a target — participants can negotiate lower
- CTA: "[Business Name] checks every invoice against the current PAPL before payment."

---

### Article 7: "NDIS Plan Review: How to Prepare and What Happens to Your Budget"

**Target keyword:** "NDIS plan review how to prepare" / "NDIS plan renewal what to expect"
**Search intent:** Participants approaching their plan end date or wanting a review

**Outline:**
- What is a plan review? (Scheduled vs unscheduled)
- When to request an unscheduled review (budget exhausted early, significant change in circumstances, new diagnosis)
- How to prepare: evidence checklist
  - Reports from therapists and providers
  - Your monthly statements from your plan manager (showing what was spent and on what)
  - Functional assessments
  - Your goals and how they've changed
- What your plan manager can provide for a review (12 months of budget data, spending patterns, alerts history)
- The role of your support coordinator vs your plan manager at review time
- What happens to remaining budget at plan end
- CTA: "Need your spending history for a plan review? We can provide a full summary."

---

### Article 8: "What Happens If My NDIS Budget Runs Out Before My Plan Ends?"

**Target keyword:** "NDIS budget run out before plan ends" / "NDIS plan budget exhausted"
**Search intent:** Participants in budget stress or wanting to prevent it

**Outline:**
- What actually happens when a category is exhausted (NDIA rejects further claims)
- The difference between: category exhausted vs total plan exhausted
- The 80% / 20% budget alert — how a good plan manager catches this early
- Options when budget is running low:
  1. Reduce service frequency until plan renewal
  2. Request an unscheduled plan review
  3. Discuss with support coordinator re: plan amendment
  4. Look at other categories that might flex (Core is flexible across subcategories)
- What a plan manager cannot do (cannot shift funds between Core and Capacity Building)
- Prevention: tracking and alerts from month 1 of the plan
- CTA: "We alert you at 80% utilisation — and again at 20% remaining. Here's how our monitoring works."

---

### Article 9: "NDIS Fraud: How Your Plan Manager Protects Your Funding"

**Target keyword:** "NDIS fraud plan management" / "how to protect NDIS funding"
**Search intent:** Participants and families concerned about fraud or wanting to understand safeguards

**Outline:**
- The scale of NDIS fraud (NDIA regularly investigates and recovers funds)
- Common types of NDIS fraud relevant to participants:
  - Providers charging for services not delivered
  - Overcharging beyond PAPL rates
  - Duplicate invoice submission
  - Identity fraud and false plan creation
- How a registered plan manager protects participants:
  - Invoice verification against PAPL
  - Provider registration check before first payment
  - ABN verification
  - Duplicate invoice detection
  - Monthly statements (participants can spot unusual transactions)
  - Fraud tip-off reporting to NDIA (1800 650 717)
- What to do if you suspect fraud
- The difference between self-managed (no invoice checks) vs plan-managed (checks in place)
- CTA: "[Business Name]'s fraud prevention controls explained."

---

### Article 10: "Real-Time NDIS Budget Tracking: Why Monthly Statements Aren't Enough"

**Target keyword:** "NDIS budget tracking real time" / "NDIS plan management portal"
**Search intent:** Tech-aware participants or those frustrated by delayed information

**Outline:**
- The problem: most plan managers send a monthly PDF statement — by the time you receive it, 4 weeks of spending has already happened
- Why this matters: you can't course-correct on month-old data
- What real-time budget tracking looks like:
  - See every claim as it's submitted to NDIA
  - Live remaining balance by support category
  - Invoice status tracker (received → verified → claimed → paid)
  - Mobile-friendly access for participants and nominees
- How OCR (document scanning) speeds up invoice processing
- What to look for in a plan management portal
- [Business Name]'s portal — built specifically for this (brief, non-salesy description; link to /portal page)
- CTA: "Want to see your budget in real time? Get started today."

---

### Article 11: "Moving to Melbourne with an NDIS Plan: What You Need to Know"

**Target keyword:** "NDIS plan Melbourne interstate" / "moving to Melbourne NDIS"
**Search intent:** People relocating to Melbourne with existing NDIS plans

**Outline:**
- NDIS plans are portable — they follow you when you move
- What changes when you move to a new state/city (LAC, support coordinator, providers)
- How to find new providers in Melbourne
- Whether you need a new plan manager when you move (no — but you might want a local one)
- Using a Melbourne-based plan manager: local knowledge, same timezone, understands Melbourne provider landscape
- Steps to update your address and contact details in myplace/PACE
- CTA: "Moving to Melbourne? [Business Name] can take over your plan management from day one."

---

### Article 12: "The Difference Between a Support Coordinator and a Plan Manager"

**Target keyword:** "NDIS support coordinator vs plan manager" / "difference plan manager support coordinator"
**Search intent:** Participants confused about the two roles

**Outline:**
- The confusion is common — both roles help participants, but in completely different ways
- **Support Coordinator:** Helps you find and connect with services, builds your capacity to implement your plan, manages provider relationships and crises. Funded from Capacity Building.
- **Plan Manager:** Handles the financial administration — invoices, payments, statements. Funded from Improved Life Choices. Does NOT choose your providers for you.
- Table: Role comparison across 10 dimensions
- Can one person do both? (Possible but the NDIS Commission has rules about conflicts of interest — see PM-POL-012)
- Do you need both? (Many participants have both — they complement each other)
- What happens if you have plan management but no support coordinator (you work directly with your plan manager and LAC)
- CTA: "Questions about how plan management fits with your other NDIS supports? We're happy to explain."

---

---

# Phase 3: NDIS Directories and Profile Listings

## 3.1 NDIS Provider Finder (Official)

Once registered, your business will appear automatically in the NDIA's Provider Finder (findaprovider.ndis.gov.au). This is the highest-trust directory because it only lists registered providers.

**To optimise your listing:**
- Your business description in the NDIA system (when you submit your registration application) becomes your Provider Finder description — write it with participants in mind, not just the Commission
- Include the words "plan management", "Melbourne", "real-time portal", "CA ANZ qualified"
- Keep your contact details current — outdated contact info is a common problem in the directory

## 3.2 My Care Space

**URL:** mycarespace.com.au
**What it is:** One of Australia's largest NDIS provider directories, used heavily by participants and families
**Cost:** Free basic listing; paid featured listings available
**Action:** Create a free listing with your service description, contact details, and website link

## 3.3 Clickability

**URL:** ndis.clickability.com.au
**What it is:** NDIS-specific review and directory platform
**Cost:** Free basic listing
**Action:** Create listing; once you have participant consent, encourage reviews here too

## 3.4 Hireup / Better Caring / Mable

These platforms are primarily for support workers, not plan managers — skip for now.

## 3.5 Infoxchange Service Seeker (Ask Izzy)

**URL:** askizzy.org.au
**What it is:** The largest free national social service directory; widely used by social workers, LACs, and support coordinators
**Cost:** Free
**Action:** Submit your service to Ask Izzy — support coordinators use this to find services for their clients

## 3.6 NDS (National Disability Services) Provider Directory

**URL:** nds.org.au
**What it is:** Industry peak body — providers who are NDS members appear in their directory
**Cost:** NDS membership (~$300–600/year for small organisations)
**Consider:** Worth joining in Year 2 for the directory listing + sector advocacy + resources access

---

---

# Phase 4: LinkedIn and Facebook Strategy

## 4.1 LinkedIn

LinkedIn is your primary channel for building referral relationships with support coordinators, LACs, and allied health professionals. These are the people who recommend plan managers to their clients.

**Profile setup:**
- Professional headshot
- Headline: "NDIS Plan Manager | Chartered Accountant (CA ANZ) | Melbourne"
- About section: same core value proposition as your website bio
- Add "Plan Management" as a skill; get CA ANZ members you know to endorse it
- Add your business under "Experience" once it's registered

**Content strategy — post 2–3 times per week:**

| Post Type | Example | Purpose |
|-----------|---------|---------|
| Article share | "Just published: How to switch plan managers — read it here [link]" | Drive traffic + credibility |
| NDIS tip | "Did you know you can use unregistered providers with plan management? Here's how it works." | Build expertise reputation |
| Personal story | "Why I left corporate accounting to start an NDIS plan management business" | Build trust with referrers |
| Industry update | "NDIS PAPL updated from 1 July — here's what changes for plan managers" | Position as informed |
| Behind the tech | "Our participant portal shows real-time budgets — here's a screenshot of the dashboard [mock/demo]" | Differentiation |

**Connection strategy:**
- Connect with every support coordinator, LAC, OT, and allied health professional in Melbourne you can find
- Join LinkedIn groups: "NDIS Providers Australia", "Disability Support Professionals Australia"
- Comment thoughtfully on posts from large plan management companies — you appear in front of their audience
- Do NOT message-bomb connections with sales pitches — build relationships through content

## 4.2 Facebook Business Page

Facebook is used heavily by NDIS participants and their families (particularly parents of participants with significant support needs).

**Page setup:**
- Business page (not personal profile)
- Category: "Financial Service" or "Disability Service"
- Cover photo and profile photo (logo or professional headshot)
- Full "About" section with website, phone, hours
- Pin your most important post (e.g., "How plan management works" article)

**Content strategy — post 2–3 times per week:**
- Share your knowledge articles with participant-friendly intros
- NDIS tips in plain English (shorter than LinkedIn posts)
- Seasonal reminders: "Plan ending in June? Here's what to do before your renewal"
- Share NDIA official updates with your brief explanation

**Facebook Groups — engage, don't spam:**
The following Melbourne/Australian NDIS Facebook groups have large, active memberships. **Do not post advertisements**. Engage genuinely by answering questions. Build a reputation, then mention your business only when directly relevant.

- "NDIS Participants Australia" (~40,000+ members)
- "NDIS Plan Management Questions and Answers"
- "Disability Support Melbourne" (and similar local groups)
- "NDIS Families Support Group Australia"

Meaningful engagement: answer a question about plan management → your name and business become associated with helpful, accurate advice → members look you up → convert.

## 4.3 Reddit — Organic Recommendation Campaign

Reddit is where NDIS participants, carers, and families go when they want unfiltered, peer-to-peer advice. "Which plan manager do you recommend?" threads appear regularly in r/NDIS, often with hundreds of upvotes and dozens of replies. A single well-timed, genuine comment in one of these threads can reach thousands of readers and drive direct inbound enquiries — at zero cost.

**The approach: be genuinely helpful first, business second.**

Reddit users can immediately spot promotional content and will downvote or report it. The goal is to build a reputation as a knowledgeable, honest participant in the community. Your business name enters naturally once trust is established.

**Target subreddits:**

| Subreddit | Size | Why it matters |
|-----------|------|----------------|
| r/NDIS | 30,000+ | The primary Australian NDIS community — participants, carers, coordinators |
| r/australia | 600,000+ | Broad NDIS questions surface here from people who don't know r/NDIS exists |
| r/disability | 60,000+ | International but significant AU participation; plan management questions appear |
| r/ausfinance | 500,000+ | Occasionally: NDIS participants asking about money management and plan management |

**Account setup:**
- Use your own Reddit account (or create a persistent one under your name/business name) — do not use throwaway accounts. Reddit's algorithms and users distrust new accounts with no history. Post in other threads (general NDIS questions, unrelated topics) to build a natural account history before engaging in recommendation threads.
- Add your business name and website link to your Reddit profile bio once the site is live.

**When to engage:**

Search Reddit regularly (set a Google Alert: `site:reddit.com NDIS plan manager recommend`) for threads asking:
- "Which plan manager do you recommend in Melbourne / Victoria?"
- "Is [large plan manager name] any good?"
- "Looking for a new plan manager — who do people like?"
- "My plan manager is terrible, looking for recommendations"

**Key positioning phrase — use this (or a natural variation) when people ask for recommendations:**

> "I think the experience most people have is that a small plan manager works really great, so they keep getting business. But they reach a point around the 100 client mark where they start hiring people and standards drop, or they need better software. The plan managers I'd steer people toward are the ones who are still small enough to pick up the phone, but have invested in proper systems so they don't fall behind."

Then, if it fits naturally: *"I run a small plan management practice in Melbourne — CA ANZ qualified, built our own participant portal so clients can see their budget in real time. Happy to answer any questions here or DM me."*

**Rules of engagement:**
- Never post the business name as your first comment in a thread — answer the question genuinely first
- Never badmouth specific plan managers by name (defamation risk, and it reads as unprofessional)
- Disclose that you run a plan management business if you're recommending yourself — Reddit communities expect transparency and will call it out if you don't
- Upvote other helpful comments; be a good community member, not just a poster

**Volume target:** Engage in 2–4 threads per week across all subreddits. Quality over quantity — one insightful comment in a high-traffic thread is worth more than ten low-effort replies.

---

---

# Phase 5: Referral Network (Support Coordinators and LACs)

Support coordinators and LACs (Local Area Coordinators) are your highest-quality referral source. They actively recommend plan managers to every participant they work with.

**The rules (PM-POL-016):**
- You cannot pay referral fees or commissions
- You cannot offer gifts or incentives for referrals
- You CAN build genuine professional relationships and be recommended on merit

**How to build these relationships:**

1. **LinkedIn outreach:** Connect with Melbourne support coordinators. Share relevant articles. Comment on their posts. After building a genuine connection (weeks, not days), introduce your business briefly and offer to answer any questions.

2. **DIA membership (Disability Intermediaries Australia):** Join DIA (intermediaries.org.au). Their events and forums connect you with support coordinators who attend the same spaces. Being a DIA member signals to support coordinators that you're serious about the sector.

3. **Be the helpful plan manager:** When a support coordinator refers a participant to you, be exceptionally responsive, process invoices fast, and never create problems for them. Word travels fast in the disability sector. One excellent experience creates multiple referrals.

4. **Produce useful resources:** A support coordinator who finds your article about "plan management vs support coordination" useful will share it — and associate your name with that expertise.

5. **NDIS community events:** Melbourne Disability Expo, various community events hosted by Scope, Yooralla, genU etc. Attend. Have a simple printed card (not a brochure — a card). Talk to people.

6. **Allied health networks:** OTs, physiotherapists, and speech pathologists frequently help participants set up their NDIS plans and often recommend plan managers. Same relationship-building approach applies.

---

---

# Phase 6: Tracking and Measurement

## Metrics to Track Monthly

| Metric | Tool | Target (Year 1) |
|--------|------|----------------|
| Website visits | Google Analytics (free) | 200+ visits/month by Month 6 |
| Google Business Profile views | GBP Insights (free) | 100+ views/month by Month 6 |
| Articles published | Manual count | 12 in first 6 months |
| Google reviews | GBP | 10+ by Month 12 |
| Directory listings active | Manual count | 5+ by Month 3 |
| LinkedIn followers | LinkedIn Analytics | 200+ by Month 12 |
| Enquiries received | CRM / email count | 3–5/month by Month 6 |
| New participants onboarded | Internal | 2–3/month by Month 6 |

## Google Search Console (Free)

Set this up from day one. Google Search Console shows you exactly which search queries are bringing people to your site, which pages rank, and where you have opportunities to improve. It is the single most valuable free SEO tool available.

Setup: search.google.com/search-console — verify your domain, submit your sitemap.

## Setting Up Google Analytics (Free)

Install Google Analytics 4 on your Next.js site (use the `@next/third-parties` package or a custom `Script` tag). Track:
- Page views and top pages
- Traffic sources (organic search vs direct vs social)
- Contact form completions (conversion events)
- Time on page for knowledge articles (>2 minutes = engaged reader)

---

---

# Launch Sequence

When your NDIS registration is confirmed, execute in this order:

| Week | Action |
|------|--------|
| Week 1 | Register domain; set up Google Workspace email (business@[yourdomain].com.au) |
| Week 1 | Publish website (at minimum: Home, How It Works, About, Pricing, Contact) |
| Week 1 | Set up Google Business Profile; verify via postcard or phone |
| Week 1 | Set up Google Analytics + Google Search Console |
| Week 2 | Publish Article 1 ("NDIS Plan Management Explained") |
| Week 2 | Create LinkedIn personal profile update and Facebook Business Page |
| Week 2 | Submit to My Care Space and Clickability directories |
| Week 2 | Submit to Ask Izzy (Service Seeker) |
| Week 3 | Publish Article 2 ("How to Switch NDIS Plan Managers") |
| Week 3 | Begin LinkedIn connection campaign with Melbourne support coordinators |
| Week 4 | Publish Article 3 ("10 Questions to Ask Your Plan Manager") |
| Week 4 | Google Business Profile: make first update post linking to Article 1 |
| Week 5+ | One article per fortnight; two LinkedIn/Facebook posts per week; GBP update weekly |
| Month 2 | Review Google Search Console data; identify which articles are getting impressions and optimise |
| Month 3 | Request Google reviews from first participants (after 4–6 weeks of smooth service) |

---

*Document prepared: April 2026 | Review: October 2026 (adjust based on actual growth data)*

---

# Appendix A: Mock Testimonial Examples

> **These are fictional examples only — for internal use to illustrate tone, format, and positioning. Do not use these publicly. All real testimonials must be unsolicited, genuine, and given with explicit written consent per PM-POL-016.**

These examples show what strong testimonials look like from the three key audiences. Use them as a reference when coaching participants, support coordinators, and support workers on what to include in a review, or as copy inspiration when designing the website testimonial section.

---

## From a Support Coordinator

> "I refer a lot of my clients to plan managers, and I've learned to be quite selective. What stands out with [Business Name] is the responsiveness — when I send through a support letter or a new service agreement, I actually get a reply the same day. That doesn't happen with the big players.
>
> A few of my clients have also commented that they can log in and see their budget in real time, which means they're not calling me to ask how much is left in their Core support. That alone saves me about half an hour a week. I'll keep recommending them."
>
> — **Priya M.**, Support Coordinator, Melbourne (inner north)

---

## From an NDIS Participant

> "I've been through three plan managers in four years. The first one took two weeks to pay a single invoice. The second one was fine but I never knew where my money was going — I'd just get a PDF at the end of the month that I didn't really understand.
>
> With [Business Name] it's completely different. I can log into the portal and see exactly what's been claimed, what's been paid, and how much is left in each support category. My OT got paid in three days last week. I actually feel like I'm in control of my plan for the first time, which is kind of the whole point isn't it."
>
> — **James K.**, NDIS Participant, Melbourne (south-east)

---

## From a Support Worker

> "Getting paid on time sounds like a low bar but honestly, for support workers it's a big deal. I've had clients with plan managers who take three or four weeks to process an invoice, which means I'm chasing it up, my client's embarrassed, and the whole thing becomes awkward.
>
> [Business Name] has been the smoothest experience I've had. I submit the invoice, and within a few days it's done. My client told me their plan manager actually messaged them when the invoice came in, just to let them know it was being processed. That kind of communication makes the whole support relationship easier."
>
> — **Tanya R.**, Independent Support Worker, Melbourne (western suburbs)

---

### Notes on collecting real testimonials

When the time comes to collect genuine testimonials:
- Ask open-ended questions: *"What's been the most useful thing about having us as your plan manager?"* — don't suggest answers
- Request written consent (email confirmation is sufficient) before publishing anywhere
- Offer to draft based on a conversation and let them approve the wording
- Never offer incentives of any kind (gift cards, discounts, etc.) — this violates PM-POL-016 and NDIS anti-inducement rules
- Google reviews (written directly by participants) do not require a separate consent process but must remain voluntary
