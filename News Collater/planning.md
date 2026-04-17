# News Collater — Project Planning

## Goal

Automatically collect, filter, and summarise news relevant to me and deliver a digest to my inbox on a scheduled basis.

---

## Key Questions to Answer Before Building

### 1. Content — What news do I want?
- [ ] What topics / keywords matter to me? (e.g. AI, finance, sport, specific industries)
- [ ] Which sources should be included? (e.g. BBC, Reuters, Hacker News, Reddit, niche blogs)
- [ ] What should be excluded / filtered out?
- [ ] How many stories per digest — a short top-5 or a longer briefing?

### 2. Delivery — How should it reach me?
- [ ] Email provider I want to send from (Gmail, Outlook, SendGrid, Mailgun…)
- [ ] Recipient address
- [ ] Digest format — plain text, HTML email, or both?

### 3. Schedule — When should it run?
- [ ] Frequency: daily, twice-daily, weekly?
- [ ] Preferred delivery time (e.g. 07:00 local time)

### 4. Enrichment — How much processing?
- [ ] Headlines + links only
- [ ] One-sentence AI summary per article
- [ ] Full digest summary written by an LLM (Claude API)

---

## Proposed Architecture

```
┌─────────────────────────────────────────┐
│            Scheduler (cron)             │
└────────────────┬────────────────────────┘
                 │ triggers
┌────────────────▼────────────────────────┐
│          Fetcher / Scraper              │
│  - RSS feeds                            │
│  - News APIs (NewsAPI, GDELT, etc.)     │
│  - Reddit / HN via API                  │
└────────────────┬────────────────────────┘
                 │ raw articles
┌────────────────▼────────────────────────┐
│          Filter & Ranker                │
│  - Keyword / topic matching             │
│  - Deduplicate stories                  │
│  - Score by relevance                   │
└────────────────┬────────────────────────┘
                 │ filtered articles
┌────────────────▼────────────────────────┐
│        Summariser (optional)            │
│  - Claude API to write digest           │
└────────────────┬────────────────────────┘
                 │ digest content
┌────────────────▼────────────────────────┐
│          Email Dispatcher               │
│  - Renders HTML/text template           │
│  - Sends via SMTP or email API          │
└─────────────────────────────────────────┘
```

---

## Potential Tech Stack

| Concern | Options |
|---|---|
| Language | Python (preferred — rich ecosystem) |
| News data | NewsAPI.org · RSS (`feedparser`) · GDELT |
| Summarisation | Claude API (`claude-sonnet-4-6`) |
| Email sending | smtplib (Gmail) · SendGrid · Mailgun |
| Scheduling | GitHub Actions (free, no server) · cron on a VPS · Windows Task Scheduler |
| Storage (dedup) | SQLite (lightweight, local) |

---

## Phased Delivery

### Phase 1 — MVP (manual trigger)
- Fetch from 2-3 RSS feeds
- Basic keyword filter
- Send plain-text email with headlines + links

### Phase 2 — Enrichment
- Add more sources (NewsAPI, Reddit)
- Claude API writes a short digest intro
- Switch to HTML email template

### Phase 3 — Automation & Persistence
- Scheduled runs (GitHub Actions or cron)
- SQLite to deduplicate across runs
- Configurable topics via a simple config file (YAML/JSON)

---

## Open Decisions

| Decision | Status |
|---|---|
| News sources | Pending |
| Topics / keywords | Pending |
| Email provider | Pending |
| Hosting / scheduler | Pending |
| AI summarisation | Optional |

---

## Next Steps

1. Answer the key questions above
2. Scaffold the project structure
3. Build Phase 1 MVP
