# Module: Budget Dashboard and Reporting
> **Portal:** NDIS Plan Management Portal
> **Owner:** Saran Likitkunawong
> **Last updated:** April 2026
> **Portal phases covered:** Phase 3 (admin charts), Phase 5 (participant portal), Phase 6 (Metabase)

---

## Table of Contents
1. [Module Overview](#1-module-overview)
2. [Architecture and Dependencies](#2-architecture-and-dependencies)
3. [Database Schema](#3-database-schema)
4. [Row Level Security (RLS)](#4-row-level-security-rls)
5. [Data Layer — Supabase Queries and SQL Functions](#5-data-layer--supabase-queries-and-sql-functions)
6. [API Routes](#6-api-routes)
7. [Shared Utilities](#7-shared-utilities)
8. [Components — Participant Portal](#8-components--participant-portal)
   - [BudgetOverviewCards](#81-budgetoverviewcards)
   - [SpendingTrendChart](#82-spendingtrendchart)
   - [CategoryBreakdown](#83-categorybreakdown)
   - [RecentTransactions](#84-recenttransactions)
   - [RealtimeBudgetWatcher](#85-realtimebudgetwatcher)
9. [Dashboard Page Composition](#9-dashboard-page-composition)
10. [Admin Analytics — Metabase](#10-admin-analytics--metabase)
11. [File Structure](#11-file-structure)
12. [Environment Variables](#12-environment-variables)
13. [Dependencies](#13-dependencies)
14. [Build Checklist](#14-build-checklist)

---

## 1. Module Overview

### Purpose

Provides interactive budget reporting for two audiences:

| Audience | Interface | Technology | Purpose |
|----------|-----------|-----------|---------|
| Participants | Portal dashboard (`/dashboard`) | shadcn/ui Charts (Recharts) | Real-time view of their own plan budget, spending trend, category utilisation, and transaction history |
| Plan manager (admin) | Admin panel (`/admin/analytics`) | Metabase embedded | Cross-participant analytics, risk flagging, invoice pipeline, provider spend — built via drag-and-drop GUI with no extra code |

### Why not Power BI Embedded

Power BI Embedded minimum cost is ~AUD $263–735/month (Microsoft Fabric F2 / Azure A1 SKU). It also requires Azure Active Directory, a service principal, and a separate data pipeline from Supabase into Power BI datasets. Disproportionate for a small plan management business.

This module achieves equivalent visual quality using:
- **Recharts** (free, React-native) for the participant portal — fully integrated with Next.js server components, Supabase RLS, and real-time subscriptions
- **Metabase** (free open source, self-hosted ~$10/month on Railway) for admin BI — reads live from Supabase PostgreSQL, produces interactive dashboards with filters, drill-downs, and cross-participant views

### Key features

- Real-time updates: participant charts refresh automatically when an invoice is processed in the admin panel (Supabase `postgres_changes` subscription)
- Burn rate projection: linear extrapolation shows whether budget will last the full plan period
- Budget alerts: categories at ≥80% utilisation shown with amber styling; depleted categories shown in red
- Per-category progress bars with spent / remaining dollar amounts
- Stacked area chart showing monthly spend across all support categories for the full plan year
- Filterable transaction history with provider, category, amount, date, and claim reference
- Admin Metabase dashboard with signed JWT embedding (no Metabase login required for admin users)

---

## 2. Architecture and Dependencies

```
Supabase PostgreSQL (source of truth)
        │
        ├── RLS policies (participant sees only their own data)
        │
        ├── SQL function: get_monthly_spending()
        │
        ├── Direct connection → Metabase (admin analytics, self-hosted)
        │
        └── Supabase JS client → Next.js
                │
                ├── Server components (initial data fetch — SSR)
                │       └── lib/budget.ts → getParticipantBudget()
                │
                ├── Client components (charts — Recharts)
                │       ├── BudgetOverviewCards
                │       ├── SpendingTrendChart
                │       ├── CategoryBreakdown
                │       └── RecentTransactions
                │
                └── Realtime client (Supabase channel subscription)
                        └── RealtimeBudgetWatcher → router.refresh()
```

**Data flow for participant:**
1. Participant visits `/dashboard`
2. Next.js server component calls `getParticipantBudget()` — fetches categories, monthly trend, and plan summary from Supabase in parallel
3. Data passed as props to client chart components (no client-side fetching for initial render)
4. `RealtimeBudgetWatcher` subscribes to `transactions` table changes for this participant
5. On any INSERT (new invoice processed by admin) → `router.refresh()` re-runs the server component, updating all charts without a full page reload

**Data flow for admin:**
1. Admin visits `/admin/participants/[id]/analytics`
2. Next.js API route generates a signed Metabase JWT (10-minute expiry) locked to the participant ID
3. Metabase iframe renders with the participant's dashboard pre-filtered — no Metabase login required

---

## 3. Database Schema

> These tables extend the core schema from `Plan Management Start.md`. Only the tables relevant to this module are shown.

```sql
-- ============================================================
-- plans
-- ============================================================
CREATE TABLE plans (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  participant_id   uuid NOT NULL REFERENCES participants(id) ON DELETE CASCADE,
  start_date       date NOT NULL,
  end_date         date NOT NULL,
  total_budget     numeric(12,2) NOT NULL,
  is_active        boolean NOT NULL DEFAULT true,
  ndia_plan_number text,
  created_at       timestamptz DEFAULT now(),
  updated_at       timestamptz DEFAULT now()
);

-- ============================================================
-- budget_categories
-- One row per support category per plan
-- ============================================================
CREATE TYPE category_code AS ENUM (
  'DAILY_ACT',      -- Core: Daily Activities
  'COMMUNITY',      -- Core: Community Participation
  'CONSUMABLES',    -- Core: Consumables
  'SOCIAL_ECON',    -- Core: Social, Economic & Community Participation
  'CAP_DAILY',      -- Capacity Building: Improved Daily Living
  'CAP_LIVING',     -- Capacity Building: Improved Living Arrangements
  'PLAN_MGMT',      -- Capacity Building: Improved Life Choices (Plan Management)
  'HEALTH',         -- Capacity Building: Health and Wellbeing
  'LEARNING',       -- Capacity Building: Improved Learning
  'RELATIONS',      -- Capacity Building: Improved Relations
  'EMPLOYMENT',     -- Capacity Building: Improved Employment
  'SUPPORT_COORD',  -- Capacity Building: Support Coordination
  'CAPITAL_AT',     -- Capital: Assistive Technology
  'CAPITAL_HM'      -- Capital: Home Modifications
);

CREATE TABLE budget_categories (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  plan_id          uuid NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
  category_code    category_code NOT NULL,
  category_name    text NOT NULL,         -- Display name e.g. "Daily Activities"
  allocated_amount numeric(12,2) NOT NULL,
  created_at       timestamptz DEFAULT now(),
  UNIQUE (plan_id, category_code)
);

-- ============================================================
-- transactions
-- One row per processed invoice payment
-- ============================================================
CREATE TYPE transaction_status AS ENUM (
  'received',     -- Invoice received, not yet verified
  'verified',     -- Passed all checks, pending PACE claim
  'claimed',      -- PACE claim submitted
  'paid',         -- Provider payment made
  'rejected',     -- Failed verification (over PAPL, wrong category, etc.)
  'on_hold'       -- Fraud concern or participant dispute
);

CREATE TABLE transactions (
  id               uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  participant_id   uuid NOT NULL REFERENCES participants(id),
  category_id      uuid NOT NULL REFERENCES budget_categories(id),
  provider_id      uuid REFERENCES providers(id),
  provider_name    text NOT NULL,          -- Denormalised for display even if provider deleted
  invoice_number   text,
  invoice_date     date,
  service_date     date NOT NULL,
  amount           numeric(10,2) NOT NULL,
  status           transaction_status NOT NULL DEFAULT 'received',
  pace_claim_ref   text,                   -- e.g. PAC-2026-09-00123
  pace_claimed_at  timestamptz,
  paid_at          timestamptz,
  notes            text,
  created_at       timestamptz DEFAULT now(),
  updated_at       timestamptz DEFAULT now()
);

-- Index for dashboard queries
CREATE INDEX idx_transactions_participant ON transactions(participant_id);
CREATE INDEX idx_transactions_service_date ON transactions(service_date);
CREATE INDEX idx_transactions_status ON transactions(status);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = now(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_transactions_updated_at
  BEFORE UPDATE ON transactions
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

---

## 4. Row Level Security (RLS)

Participants must only ever see their own data. Enable RLS on all relevant tables and define policies.

```sql
-- Enable RLS
ALTER TABLE plans             ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions      ENABLE ROW LEVEL SECURITY;

-- Helper: resolve the participant_id linked to the authenticated user
CREATE OR REPLACE FUNCTION auth_participant_id()
RETURNS uuid AS $$
  SELECT id FROM participants WHERE user_id = auth.uid() LIMIT 1;
$$ LANGUAGE sql SECURITY DEFINER STABLE;

-- plans: participants see only their active plan
CREATE POLICY "participant_own_plans" ON plans
  FOR SELECT USING (participant_id = auth_participant_id());

-- budget_categories: accessible if the linked plan belongs to the participant
CREATE POLICY "participant_own_categories" ON budget_categories
  FOR SELECT USING (
    plan_id IN (SELECT id FROM plans WHERE participant_id = auth_participant_id())
  );

-- transactions: participants see only their own transactions
CREATE POLICY "participant_own_transactions" ON transactions
  FOR SELECT USING (participant_id = auth_participant_id());

-- Admin role (service_role key or custom 'admin' role) bypasses RLS
-- Use the Supabase service_role key in server-side admin routes only —
-- never expose it to the client.
```

---

## 5. Data Layer — Supabase Queries and SQL Functions

### SQL function — monthly spending trend

```sql
-- supabase/migrations/YYYYMMDD_add_monthly_spending_fn.sql

CREATE OR REPLACE FUNCTION get_monthly_spending(p_participant_id uuid)
RETURNS TABLE (
  month        text,      -- "2026-07"
  label        text,      -- "Jul"
  total_spent  numeric,
  daily_act    numeric,
  community    numeric,
  consumables  numeric,
  cap_daily    numeric,
  plan_mgmt    numeric,
  support_coord numeric,
  other        numeric    -- all remaining categories summed
) AS $$
  SELECT
    TO_CHAR(DATE_TRUNC('month', t.service_date), 'YYYY-MM'),
    TO_CHAR(DATE_TRUNC('month', t.service_date), 'Mon'),
    SUM(t.amount),
    SUM(CASE WHEN bc.category_code = 'DAILY_ACT'     THEN t.amount ELSE 0 END),
    SUM(CASE WHEN bc.category_code = 'COMMUNITY'     THEN t.amount ELSE 0 END),
    SUM(CASE WHEN bc.category_code = 'CONSUMABLES'   THEN t.amount ELSE 0 END),
    SUM(CASE WHEN bc.category_code = 'CAP_DAILY'     THEN t.amount ELSE 0 END),
    SUM(CASE WHEN bc.category_code = 'PLAN_MGMT'     THEN t.amount ELSE 0 END),
    SUM(CASE WHEN bc.category_code = 'SUPPORT_COORD' THEN t.amount ELSE 0 END),
    SUM(CASE WHEN bc.category_code NOT IN (
      'DAILY_ACT','COMMUNITY','CONSUMABLES','CAP_DAILY','PLAN_MGMT','SUPPORT_COORD'
    ) THEN t.amount ELSE 0 END)
  FROM transactions t
  JOIN budget_categories bc ON t.category_id = bc.id
  JOIN plans p ON bc.plan_id = p.id
  WHERE p.participant_id = p_participant_id
    AND p.is_active = true
    AND t.status = 'paid'
    AND t.service_date >= (
      SELECT start_date FROM plans
      WHERE participant_id = p_participant_id AND is_active = true
      LIMIT 1
    )
  GROUP BY DATE_TRUNC('month', t.service_date)
  ORDER BY DATE_TRUNC('month', t.service_date)
$$ LANGUAGE sql SECURITY DEFINER;
```

### TypeScript data layer

```typescript
// lib/budget.ts
import { createClient } from '@/lib/supabase/server'

// ── Types ────────────────────────────────────────────────────────────────────

export type CategoryBudget = {
  id:               string
  category_code:    string
  category_name:    string
  allocated_amount: number
  spent_amount:     number
  remaining_amount: number
  utilisation_pct:  number
}

export type MonthlySpend = {
  month:        string   // "2026-07"
  label:        string   // "Jul"
  total_spent:  number
  daily_act:    number
  community:    number
  consumables:  number
  cap_daily:    number
  plan_mgmt:    number
  support_coord:number
  other:        number
}

export type PlanSummary = {
  id:                  string
  start_date:          string
  end_date:            string
  total_budget:        number
  days_remaining:      number
  days_elapsed:        number
  total_days:          number
  pct_time_elapsed:    number
}

export type RecentTransaction = {
  id:             string
  provider_name:  string
  category_name:  string
  service_date:   string
  amount:         number
  status:         string
  pace_claim_ref: string | null
  paid_at:        string | null
}

export type ParticipantBudgetData = {
  plan:        PlanSummary
  categories:  CategoryBudget[]
  monthly:     MonthlySpend[]
  recent:      RecentTransaction[]
}

// ── Main query ────────────────────────────────────────────────────────────────

export async function getParticipantBudget(
  participantId: string
): Promise<ParticipantBudgetData | null> {
  const supabase = await createClient()

  // Run all queries in parallel
  const [planResult, categoryResult, monthlyResult, recentResult] = await Promise.all([

    // Active plan
    supabase
      .from('plans')
      .select('id, start_date, end_date, total_budget')
      .eq('participant_id', participantId)
      .eq('is_active', true)
      .single(),

    // Budget categories with rolled-up spend from paid transactions
    supabase
      .from('budget_categories')
      .select(`
        id,
        category_code,
        category_name,
        allocated_amount,
        transactions!inner (amount, status)
      `)
      .eq('plan.participant_id', participantId)
      .eq('transactions.status', 'paid'),

    // Monthly trend via RPC
    supabase.rpc('get_monthly_spending', { p_participant_id: participantId }),

    // 20 most recent transactions
    supabase
      .from('transactions')
      .select(`
        id,
        provider_name,
        budget_categories ( category_name ),
        service_date,
        amount,
        status,
        pace_claim_ref,
        paid_at
      `)
      .eq('participant_id', participantId)
      .order('service_date', { ascending: false })
      .limit(20),
  ])

  if (planResult.error || !planResult.data) return null

  const plan = planResult.data
  const today      = new Date()
  const start      = new Date(plan.start_date)
  const end        = new Date(plan.end_date)
  const msPerDay   = 1000 * 60 * 60 * 24
  const daysElapsed   = Math.max(Math.floor((today.getTime() - start.getTime()) / msPerDay), 1)
  const daysRemaining = Math.max(Math.floor((end.getTime() - today.getTime()) / msPerDay), 0)
  const totalDays     = Math.floor((end.getTime() - start.getTime()) / msPerDay)

  // Aggregate spend per category (handle the joined transactions array)
  const categories: CategoryBudget[] = (categoryResult.data ?? []).map((cat) => {
    const spent = (cat.transactions as { amount: number }[])
      .reduce((sum, t) => sum + t.amount, 0)
    return {
      id:               cat.id,
      category_code:    cat.category_code,
      category_name:    cat.category_name,
      allocated_amount: cat.allocated_amount,
      spent_amount:     spent,
      remaining_amount: cat.allocated_amount - spent,
      utilisation_pct:  Math.round((spent / cat.allocated_amount) * 100),
    }
  })

  const recent: RecentTransaction[] = (recentResult.data ?? []).map((t) => ({
    id:             t.id,
    provider_name:  t.provider_name,
    category_name:  (t.budget_categories as { category_name: string })?.category_name ?? '—',
    service_date:   t.service_date,
    amount:         t.amount,
    status:         t.status,
    pace_claim_ref: t.pace_claim_ref,
    paid_at:        t.paid_at,
  }))

  return {
    plan: {
      id:                plan.id,
      start_date:        plan.start_date,
      end_date:          plan.end_date,
      total_budget:      plan.total_budget,
      days_remaining:    daysRemaining,
      days_elapsed:      daysElapsed,
      total_days:        totalDays,
      pct_time_elapsed:  Math.round((daysElapsed / totalDays) * 100),
    },
    categories,
    monthly:  monthlyResult.data ?? [],
    recent,
  }
}
```

---

## 6. API Routes

### Metabase signed embed token

```typescript
// app/api/metabase-embed-token/route.ts
import { NextRequest, NextResponse } from 'next/server'
import jwt from 'jsonwebtoken'
import { createClient } from '@/lib/supabase/server'

const METABASE_SITE_URL = process.env.METABASE_SITE_URL!
const METABASE_SECRET   = process.env.METABASE_SECRET_KEY!
const DASHBOARD_ID      = Number(process.env.METABASE_PARTICIPANT_DASHBOARD_ID ?? '1')

export async function GET(request: NextRequest) {
  // Verify the caller is an authenticated admin
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user?.id)
    .single()

  if (!user || profile?.role !== 'admin') {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
  }

  const participantId = request.nextUrl.searchParams.get('participantId')
  if (!participantId) {
    return NextResponse.json({ error: 'participantId required' }, { status: 400 })
  }

  const payload = {
    resource: { dashboard: DASHBOARD_ID },
    params:   { participant_id: participantId },
    exp:      Math.round(Date.now() / 1000) + 600, // 10 min
  }

  const token    = jwt.sign(payload, METABASE_SECRET)
  const iframeUrl = `${METABASE_SITE_URL}/embed/dashboard/${token}` +
    `#bordered=false&titled=false&theme=transparent`

  return NextResponse.json({ iframeUrl })
}
```

---

## 7. Shared Utilities

```typescript
// lib/format.ts

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-AU', {
    style:    'currency',
    currency: 'AUD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-AU', {
    day:   'numeric',
    month: 'short',
    year:  'numeric',
  })
}

export function projectedExhaustion(
  totalRemaining: number,
  dailyBurnRate:  number,
  daysRemaining:  number
): { isAtRisk: boolean; daysUntilEmpty: number } {
  if (dailyBurnRate <= 0) return { isAtRisk: false, daysUntilEmpty: Infinity }
  const daysUntilEmpty = totalRemaining / dailyBurnRate
  return {
    isAtRisk:     daysUntilEmpty < daysRemaining * 0.9,
    daysUntilEmpty: Math.round(daysUntilEmpty),
  }
}
```

---

## 8. Components — Participant Portal

Install dependencies first:

```bash
npx shadcn@latest add card badge progress table
npx shadcn@latest add chart
npm install recharts date-fns
```

Chart config (add to `components/ui/chart.tsx` colour tokens or `globals.css`):

```css
/* globals.css — chart colour palette */
:root {
  --chart-1: 210 100% 50%;   /* blue   — Daily Activities */
  --chart-2: 142 76% 36%;    /* green  — Community */
  --chart-3: 38 92% 50%;     /* amber  — Capacity Building */
  --chart-4: 280 65% 60%;    /* purple — Plan Management */
  --chart-5: 350 89% 60%;    /* red    — Other / Alerts */
}
```

---

### 8.1 BudgetOverviewCards

Four KPI cards: total remaining, total spent (with pace badge), days remaining, and a burn-rate projection card.

```tsx
// components/dashboard/budget-overview-cards.tsx
'use client'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertTriangle, Calendar, TrendingDown, Wallet } from 'lucide-react'
import { formatCurrency, formatDate, projectedExhaustion } from '@/lib/format'
import type { CategoryBudget, PlanSummary } from '@/lib/budget'

interface Props {
  plan:       PlanSummary
  categories: CategoryBudget[]
}

export function BudgetOverviewCards({ plan, categories }: Props) {
  const totalBudget    = categories.reduce((s, c) => s + c.allocated_amount, 0)
  const totalSpent     = categories.reduce((s, c) => s + c.spent_amount, 0)
  const totalRemaining = totalBudget - totalSpent
  const pctRemaining   = Math.round((totalRemaining / totalBudget) * 100)

  const actualSpentPct   = Math.round((totalSpent / totalBudget) * 100)
  const burnDelta        = actualSpentPct - plan.pct_time_elapsed  // + = ahead of pace

  const dailyBurnRate    = totalSpent / plan.days_elapsed
  const { isAtRisk, daysUntilEmpty } = projectedExhaustion(
    totalRemaining, dailyBurnRate, plan.days_remaining
  )

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">

      {/* Total remaining */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Total Remaining</CardTitle>
          <Wallet className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{formatCurrency(totalRemaining)}</p>
          <p className="text-xs text-muted-foreground mt-1">
            {pctRemaining}% of {formatCurrency(totalBudget)}
          </p>
        </CardContent>
      </Card>

      {/* Total spent with pace indicator */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Total Spent</CardTitle>
          <TrendingDown className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{formatCurrency(totalSpent)}</p>
          <Badge
            variant={Math.abs(burnDelta) <= 5 ? 'secondary' : burnDelta > 5 ? 'destructive' : 'outline'}
            className="mt-1 text-xs"
          >
            {burnDelta > 0 ? `+${burnDelta}%` : `${burnDelta}%`} vs expected pace
          </Badge>
        </CardContent>
      </Card>

      {/* Days remaining */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Days Remaining</CardTitle>
          <Calendar className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{plan.days_remaining}</p>
          <p className="text-xs text-muted-foreground mt-1">
            Plan ends {formatDate(plan.end_date)}
          </p>
        </CardContent>
      </Card>

      {/* Burn-rate projection */}
      <Card className={isAtRisk ? 'border-amber-400 bg-amber-50/30' : ''}>
        <CardHeader className="flex flex-row items-center justify-between pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">Projected Balance</CardTitle>
          {isAtRisk && <AlertTriangle className="h-4 w-4 text-amber-500" />}
        </CardHeader>
        <CardContent>
          <p className="text-2xl font-bold">{isAtRisk ? 'At risk' : 'On track'}</p>
          <p className="text-xs text-muted-foreground mt-1">
            {isAtRisk
              ? `Funds may run out ~${daysUntilEmpty} days before plan end`
              : 'Budget should last the full plan period'}
          </p>
        </CardContent>
      </Card>

    </div>
  )
}
```

---

### 8.2 SpendingTrendChart

Stacked area chart — monthly spend by support category for the full plan year.

```tsx
// components/dashboard/spending-trend-chart.tsx
'use client'
import {
  Area, AreaChart, CartesianGrid, XAxis, YAxis, ResponsiveContainer,
} from 'recharts'
import {
  ChartContainer, ChartLegend, ChartLegendContent,
  ChartTooltip, ChartTooltipContent,
} from '@/components/ui/chart'
import {
  Card, CardContent, CardDescription, CardHeader, CardTitle,
} from '@/components/ui/card'
import { formatCurrency } from '@/lib/format'
import type { MonthlySpend } from '@/lib/budget'

const chartConfig = {
  daily_act:    { label: 'Daily Activities',        color: 'hsl(var(--chart-1))' },
  community:    { label: 'Community Participation', color: 'hsl(var(--chart-2))' },
  cap_daily:    { label: 'Capacity Building',       color: 'hsl(var(--chart-3))' },
  plan_mgmt:    { label: 'Plan Management',         color: 'hsl(var(--chart-4))' },
  other:        { label: 'Other',                   color: 'hsl(var(--chart-5))' },
}

interface Props {
  monthly:    MonthlySpend[]
  className?: string
}

export function SpendingTrendChart({ monthly, className }: Props) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Monthly Spending</CardTitle>
        <CardDescription>By support category — current plan year</CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig} className="h-[300px] w-full">
          <AreaChart data={monthly} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
            <defs>
              {Object.entries(chartConfig).map(([key, cfg]) => (
                <linearGradient key={key} id={`grad-${key}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor={cfg.color} stopOpacity={0.35} />
                  <stop offset="95%" stopColor={cfg.color} stopOpacity={0}    />
                </linearGradient>
              ))}
            </defs>

            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--border))" />
            <XAxis
              dataKey="label"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              tick={{ fontSize: 12 }}
            />
            <YAxis
              tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
              tickLine={false}
              axisLine={false}
              width={42}
              tick={{ fontSize: 12 }}
            />
            <ChartTooltip
              content={
                <ChartTooltipContent
                  formatter={(value, name) => [
                    formatCurrency(value as number),
                    chartConfig[name as keyof typeof chartConfig]?.label ?? name,
                  ]}
                />
              }
            />
            <ChartLegend content={<ChartLegendContent />} />

            {Object.keys(chartConfig).map((key) => (
              <Area
                key={key}
                type="monotone"
                dataKey={key}
                stackId="stack"
                stroke={chartConfig[key as keyof typeof chartConfig].color}
                fill={`url(#grad-${key})`}
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 4 }}
              />
            ))}
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
```

---

### 8.3 CategoryBreakdown

Donut chart + per-category utilisation progress bars. Bars turn amber at ≥80%, red at 100%.

```tsx
// components/dashboard/category-breakdown.tsx
'use client'
import { Cell, Pie, PieChart } from 'recharts'
import {
  ChartContainer, ChartTooltip, ChartTooltipContent,
} from '@/components/ui/chart'
import {
  Card, CardContent, CardHeader, CardTitle,
} from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'
import { formatCurrency } from '@/lib/format'
import type { CategoryBudget } from '@/lib/budget'

const PALETTE = [
  'hsl(var(--chart-1))',
  'hsl(var(--chart-2))',
  'hsl(var(--chart-3))',
  'hsl(var(--chart-4))',
  'hsl(var(--chart-5))',
]

interface Props {
  categories: CategoryBudget[]
}

export function CategoryBreakdown({ categories }: Props) {
  // Only show categories with allocated budget > 0
  const active = categories.filter((c) => c.allocated_amount > 0)

  const donutData = active.map((c) => ({
    name:  c.category_name,
    value: c.spent_amount,
  }))

  return (
    <Card>
      <CardHeader>
        <CardTitle>Budget by Category</CardTitle>
      </CardHeader>
      <CardContent className="space-y-5">

        {/* Donut */}
        <ChartContainer config={{}} className="mx-auto h-[160px] w-[160px]">
          <PieChart>
            <Pie
              data={donutData}
              cx="50%"
              cy="50%"
              innerRadius={48}
              outerRadius={72}
              paddingAngle={3}
              dataKey="value"
              strokeWidth={0}
            >
              {donutData.map((_, i) => (
                <Cell key={i} fill={PALETTE[i % PALETTE.length]} />
              ))}
            </Pie>
            <ChartTooltip
              content={
                <ChartTooltipContent
                  formatter={(v) => formatCurrency(v as number)}
                />
              }
            />
          </PieChart>
        </ChartContainer>

        {/* Progress bars */}
        <div className="space-y-4">
          {active.map((cat, i) => {
            const pct       = Math.min(cat.utilisation_pct, 100)
            const isWarning = cat.utilisation_pct >= 80 && cat.utilisation_pct < 100
            const isDanger  = cat.utilisation_pct >= 100

            return (
              <div key={cat.id}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-medium truncate max-w-[150px]">
                    {cat.category_name}
                  </span>
                  <span className={cn(
                    'text-xs font-mono',
                    isWarning && 'text-amber-600 font-semibold',
                    isDanger  && 'text-red-600 font-semibold',
                  )}>
                    {cat.utilisation_pct}%
                  </span>
                </div>

                <Progress
                  value={pct}
                  className={cn(
                    'h-2',
                    isWarning && '[&>div]:bg-amber-500',
                    isDanger  && '[&>div]:bg-red-500',
                    !isWarning && !isDanger && '[&>div]:bg-[--cat-color]',
                  )}
                  style={{ '--cat-color': PALETTE[i % PALETTE.length] } as React.CSSProperties}
                />

                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>{formatCurrency(cat.spent_amount)} spent</span>
                  <span>{formatCurrency(cat.remaining_amount)} left</span>
                </div>
              </div>
            )
          })}
        </div>
      </CardContent>
    </Card>
  )
}
```

---

### 8.4 RecentTransactions

Filterable transaction history table — last 20 paid, claimed, or on-hold transactions.

```tsx
// components/dashboard/recent-transactions.tsx
'use client'
import { useState } from 'react'
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import {
  Card, CardContent, CardHeader, CardTitle, CardDescription,
} from '@/components/ui/card'
import { formatCurrency, formatDate } from '@/lib/format'
import type { RecentTransaction } from '@/lib/budget'

const STATUS_BADGE: Record<string, 'default' | 'secondary' | 'outline' | 'destructive'> = {
  paid:     'default',
  claimed:  'secondary',
  verified: 'outline',
  received: 'outline',
  on_hold:  'destructive',
  rejected: 'destructive',
}

interface Props {
  transactions: RecentTransaction[]
}

export function RecentTransactions({ transactions }: Props) {
  const [search, setSearch] = useState('')

  const filtered = transactions.filter((t) =>
    t.provider_name.toLowerCase().includes(search.toLowerCase()) ||
    t.category_name.toLowerCase().includes(search.toLowerCase()) ||
    (t.pace_claim_ref ?? '').toLowerCase().includes(search.toLowerCase())
  )

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <CardTitle>Recent Transactions</CardTitle>
            <CardDescription>Last 20 invoices processed on your plan</CardDescription>
          </div>
          <Input
            placeholder="Search provider, category, claim ref…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-64"
          />
        </div>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Date</TableHead>
              <TableHead>Provider</TableHead>
              <TableHead>Category</TableHead>
              <TableHead className="text-right">Amount</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Claim Ref</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.length === 0 && (
              <TableRow>
                <TableCell colSpan={6} className="text-center text-muted-foreground py-8">
                  No transactions found
                </TableCell>
              </TableRow>
            )}
            {filtered.map((t) => (
              <TableRow key={t.id}>
                <TableCell className="tabular-nums text-sm">
                  {formatDate(t.service_date)}
                </TableCell>
                <TableCell className="font-medium max-w-[160px] truncate">
                  {t.provider_name}
                </TableCell>
                <TableCell className="text-sm text-muted-foreground">
                  {t.category_name}
                </TableCell>
                <TableCell className="text-right tabular-nums font-mono text-sm">
                  {formatCurrency(t.amount)}
                </TableCell>
                <TableCell>
                  <Badge variant={STATUS_BADGE[t.status] ?? 'outline'} className="capitalize text-xs">
                    {t.status.replace('_', ' ')}
                  </Badge>
                </TableCell>
                <TableCell className="text-xs text-muted-foreground font-mono">
                  {t.pace_claim_ref ?? '—'}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
```

---

### 8.5 RealtimeBudgetWatcher

Invisible client component — subscribes to the `transactions` table and calls `router.refresh()` on any new INSERT for this participant. Drop into the dashboard layout once; all server components re-run automatically.

```tsx
// components/dashboard/realtime-budget-watcher.tsx
'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'

interface Props {
  participantId: string
}

export function RealtimeBudgetWatcher({ participantId }: Props) {
  const supabase = createClient()
  const router   = useRouter()

  useEffect(() => {
    const channel = supabase
      .channel(`budget-watch:${participantId}`)
      .on(
        'postgres_changes',
        {
          event:  'INSERT',
          schema: 'public',
          table:  'transactions',
          filter: `participant_id=eq.${participantId}`,
        },
        () => router.refresh()     // re-runs server component; no full reload
      )
      .on(
        'postgres_changes',
        {
          event:  'UPDATE',        // status changes (received → paid) also refresh
          schema: 'public',
          table:  'transactions',
          filter: `participant_id=eq.${participantId}`,
        },
        () => router.refresh()
      )
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [participantId, router, supabase])

  return null
}
```

---

## 9. Dashboard Page Composition

```tsx
// app/(portal)/dashboard/page.tsx
import { redirect }               from 'next/navigation'
import { createClient }           from '@/lib/supabase/server'
import { getParticipantBudget }   from '@/lib/budget'
import { BudgetOverviewCards }    from '@/components/dashboard/budget-overview-cards'
import { SpendingTrendChart }     from '@/components/dashboard/spending-trend-chart'
import { CategoryBreakdown }      from '@/components/dashboard/category-breakdown'
import { RecentTransactions }     from '@/components/dashboard/recent-transactions'
import { RealtimeBudgetWatcher }  from '@/components/dashboard/realtime-budget-watcher'
import { formatDate }             from '@/lib/format'

export default async function DashboardPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) redirect('/login')

  const { data: participant } = await supabase
    .from('participants')
    .select('id, full_name')
    .eq('user_id', user.id)
    .single()

  if (!participant) redirect('/onboarding')

  const budget = await getParticipantBudget(participant.id)
  if (!budget) {
    return (
      <div className="p-6 text-muted-foreground">
        No active plan found. Please contact your plan manager.
      </div>
    )
  }

  const { plan, categories, monthly, recent } = budget

  return (
    <>
      {/* Invisible realtime watcher — refreshes page when new transaction arrives */}
      <RealtimeBudgetWatcher participantId={participant.id} />

      <div className="space-y-6 p-4 md:p-6 max-w-7xl mx-auto">

        <header>
          <h1 className="text-2xl font-semibold tracking-tight">
            {participant.full_name} — NDIS Budget Dashboard
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Plan period: {formatDate(plan.start_date)} → {formatDate(plan.end_date)}
            &nbsp;·&nbsp;{plan.days_remaining} days remaining
          </p>
        </header>

        {/* Row 1 — 4 KPI cards */}
        <BudgetOverviewCards plan={plan} categories={categories} />

        {/* Row 2 — Trend chart (2/3) + Donut breakdown (1/3) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <SpendingTrendChart monthly={monthly} className="lg:col-span-2" />
          <CategoryBreakdown categories={categories} />
        </div>

        {/* Row 3 — Transaction table */}
        <RecentTransactions transactions={recent} />

      </div>
    </>
  )
}
```

---

## 10. Admin Analytics — Metabase

### Setup

**Option A — Railway (recommended for prod, ~$10/month):**

1. Go to railway.app → New Project → Deploy from Docker Image
2. Image: `metabase/metabase:latest`
3. Add a Railway PostgreSQL database for Metabase's own metadata
4. Set env vars:
   ```
   MB_DB_TYPE=postgres
   MB_DB_HOST=<railway postgres host>
   MB_DB_PORT=5432
   MB_DB_DBNAME=metabase
   MB_DB_USER=postgres
   MB_DB_PASS=<railway postgres pass>
   MB_SITE_URL=https://<your-metabase-subdomain>.railway.app
   ```

**Option B — Local dev:**
```yaml
# docker-compose.yml
services:
  metabase:
    image: metabase/metabase:latest
    ports:
      - "3001:3000"
    volumes:
      - metabase-data:/metabase-data
volumes:
  metabase-data:
```
```bash
docker-compose up -d
# Open http://localhost:3001
```

### Connect to Supabase

In Metabase → Admin → Databases → Add database → PostgreSQL:

| Field | Value |
|-------|-------|
| Host | `db.<project-ref>.supabase.co` |
| Port | `5432` |
| Database | `postgres` |
| Username | `postgres` |
| Password | Supabase database password |
| SSL mode | `require` |

> Use the **Direct** connection (not Session Pooler) — Metabase requires persistent connections.

### Signed embedding setup

In Metabase → Admin → Embedding → Enable "Embedding in other applications" → Copy the Embedding Secret Key → add to your `.env.local`:

```bash
METABASE_SITE_URL=https://your-metabase.railway.app
METABASE_SECRET_KEY=<copied secret key>
METABASE_PARTICIPANT_DASHBOARD_ID=1   # set once you've built the dashboard
```

### Admin embed component

```tsx
// components/admin/metabase-participant-view.tsx
'use client'
import { useEffect, useState } from 'react'
import { Skeleton } from '@/components/ui/skeleton'

interface Props {
  participantId: string
  height?: number
}

export function MetabaseParticipantView({ participantId, height = 640 }: Props) {
  const [src, setSrc] = useState<string | null>(null)

  useEffect(() => {
    setSrc(null)   // reset on participant change
    fetch(`/api/metabase-embed-token?participantId=${participantId}`)
      .then((r) => r.json())
      .then(({ iframeUrl }) => setSrc(iframeUrl))
  }, [participantId])

  if (!src) return <Skeleton className="w-full rounded-lg" style={{ height }} />

  return (
    <iframe
      src={src}
      className="w-full rounded-lg border bg-background"
      style={{ height }}
      allowTransparency
      title="Participant analytics"
    />
  )
}
```

### Recommended Metabase dashboards to build

Once connected, build these in the Metabase GUI (no code):

| Dashboard | Key questions to add |
|-----------|---------------------|
| **Participant detail** | Budget by category (bar), monthly spend trend (line), transaction log (table filtered by `participant_id`) |
| **Portfolio overview** | Total funds under management, participants by risk level (< 20% remaining), average monthly invoice volume |
| **Invoice pipeline** | Count and value by status (received / verified / claimed / paid / on-hold), average days from received to paid |
| **Provider analytics** | Top 10 providers by total spend, providers with rejected invoices, first-time vs returning providers |
| **Quality indicators** (PM-POL-017) | Average invoice processing time, statement delivery rate, budget alert response rate |

---

## 11. File Structure

```
app/
  (portal)/
    dashboard/
      page.tsx                          ← Dashboard page (Server Component)
  admin/
    participants/
      [id]/
        analytics/
          page.tsx                      ← Embeds MetabaseParticipantView
  api/
    metabase-embed-token/
      route.ts                          ← Signs JWT for Metabase embed

components/
  dashboard/
    budget-overview-cards.tsx
    spending-trend-chart.tsx
    category-breakdown.tsx
    recent-transactions.tsx
    realtime-budget-watcher.tsx
  admin/
    metabase-participant-view.tsx

lib/
  budget.ts                             ← getParticipantBudget()
  format.ts                             ← formatCurrency, formatDate, projectedExhaustion
  supabase/
    server.ts                           ← createClient() for server components
    client.ts                           ← createClient() for client components

supabase/
  migrations/
    YYYYMMDD_add_monthly_spending_fn.sql
    YYYYMMDD_budget_rls_policies.sql
```

---

## 12. Environment Variables

```bash
# .env.local

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://<project-ref>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon key>
SUPABASE_SERVICE_ROLE_KEY=<service role key>    # server-only, never expose to client

# Metabase (admin analytics)
METABASE_SITE_URL=https://your-metabase.railway.app
METABASE_SECRET_KEY=<metabase embedding secret>
METABASE_PARTICIPANT_DASHBOARD_ID=1
```

---

## 13. Dependencies

```json
{
  "dependencies": {
    "recharts":    "^2.x",
    "date-fns":    "^4.x",
    "jsonwebtoken":"^9.x"
  },
  "devDependencies": {
    "@types/jsonwebtoken": "^9.x"
  }
}
```

shadcn components required:
```bash
npx shadcn@latest add card badge progress table input skeleton chart
```

---

## 14. Build Checklist

### Phase 3 — Admin invoice review (Weeks 10–12)
- [ ] Create `plans`, `budget_categories`, `transactions` tables with migrations
- [ ] Apply RLS policies
- [ ] Deploy `get_monthly_spending` SQL function
- [ ] Build `lib/budget.ts` data layer
- [ ] Build `RecentTransactions` component (admin view — no RLS restriction)
- [ ] Deploy Metabase on Railway; connect to Supabase
- [ ] Build Metabase "Invoice pipeline" and "Portfolio overview" dashboards
- [ ] Wire `MetabaseParticipantView` into admin participant detail page
- [ ] Build `/api/metabase-embed-token` route with admin auth guard

### Phase 5 — Participant portal (Weeks 16–17)
- [ ] Install `recharts`, `date-fns`, shadcn chart components
- [ ] Build `BudgetOverviewCards`
- [ ] Build `SpendingTrendChart`
- [ ] Build `CategoryBreakdown`
- [ ] Build `RecentTransactions` (participant-facing, filtered by RLS)
- [ ] Build `RealtimeBudgetWatcher`
- [ ] Compose `/dashboard` page
- [ ] Test RLS: confirm participant A cannot see participant B's data
- [ ] Test real-time: process a test invoice in admin → confirm dashboard updates without reload
- [ ] Test burn-rate projection logic with edge cases (new plan with no spend, almost-exhausted plan)
- [ ] Mobile responsive check (2-col KPI cards on small screens)

### Phase 6 — Automation and polish (Weeks 18–20)
- [ ] Add Metabase "Quality Indicators" dashboard (PM-POL-017 metrics)
- [ ] Add Metabase "Provider analytics" dashboard
- [ ] Add PDF export of participant monthly statement (trigger from dashboard)
- [ ] Add date-range filter to `RecentTransactions` (shadcn DateRangePicker)
- [ ] Add "download CSV" to transaction table
- [ ] Stress test with 50 mock participants and 12 months of transactions
