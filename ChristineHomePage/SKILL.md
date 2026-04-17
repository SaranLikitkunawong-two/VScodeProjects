# SKILL.md — Key Learnings from ChristineHomePage

---

## 1. CSS Heart Shape

A heart is built from a rotated square with two circles attached via `::before` and `::after`.

```css
.heart {
  position: relative;
  width: 32px;
  height: 28px;
  background-color: #C8A882;
  transform: rotate(-45deg);
}

.heart::before,
.heart::after {
  content: "";
  position: absolute;
  width: 32px;
  height: 32px;
  background-color: #C8A882;
  border-radius: 50%;
}

.heart::before { top: -16px; left: 0; }      /* circle on top */
.heart::after  { top: 0;     left: 16px; }   /* circle on right */
```

**Key rules:**
- `::before` top offset = half the pseudo-element height (negative)
- `::after` left offset = half the pseudo-element width
- Pulse animation must preserve the `-45deg` rotation: `transform: rotate(-45deg) scale(1.3)`
- For multiple hearts, stagger `animation-delay` on `:nth-child(2)`, `:nth-child(3)`

---

## 2. SVG Plane Animation Along a Path

Use SMIL `<animateMotion>` with `<mpath>` to move an element along a defined SVG path.

```html
<path id="trail-1" d="M -40 160 C 280 40, 680 360 ..." fill="none" stroke="#C8A882" stroke-dasharray="7 15"/>

<text font-size="90" fill="#B87A45" text-anchor="middle" dominant-baseline="central">✈
  <animateMotion dur="30s" repeatCount="indefinite" rotate="auto">
    <mpath href="#trail-1"/>
  </animateMotion>
</text>
```

**Key rules:**
- `rotate="auto"` — rotates the element to follow the path tangent
- `dominant-baseline="central"` — vertically centers the glyph on the path (critical for large font sizes)
- `text-anchor="middle"` — horizontally centers the glyph on the path point
- `begin="-Xs"` — starts the animation X seconds in, so elements are visible immediately on load
- Dashed trails use `stroke-dasharray="gap length"` — larger gaps feel more like contrails

---

## 3. CSS 3D Globe (rotateY)

A spinning globe effect using CSS `rotateY` with `perspective` on the parent.

```css
.globe-scene {
  perspective: 1000px;   /* set on PARENT, not the spinning element */
}

.globe-spin {
  animation: globe-rotate 32s linear infinite;
}

@keyframes globe-rotate {
  from { transform: rotateY(0deg); }
  to   { transform: rotateY(360deg); }
}
```

**Lighting trick:** Place a static shading overlay div on top of the spinning element. It doesn't rotate, so the lighting appears consistent regardless of globe position.

```css
.globe-shading {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background:
    radial-gradient(circle at 36% 32%, rgba(255,255,255,0.22) 0%, transparent 52%),
    radial-gradient(circle at 70% 72%, rgba(0,15,50,0.25)    0%, transparent 48%);
}
```

**SVG continent tips:**
- Use `<clipPath>` to clip grid lines and continents to the circle boundary
- Simple `<ellipse>` shapes with `transform="rotate(...)"` read as continents without needing accurate geography
- Subtle grid lines at ~13% white opacity add depth without noise

---

## 4. Z-Index Layering Strategy

When stacking background elements behind a card, assign explicit z-index to every layer.

```
z-index: 0  →  bg-scene (SVG planes)
z-index: 1  →  globe-scene
z-index: 2  →  page-wrapper (card content)
```

All positioned elements (`position: fixed/absolute/relative`) must have `z-index` set explicitly, otherwise stacking order falls back to DOM order which is easy to break.

---

## 5. JavaScript Countdown Timer

```js
const target = new Date('2026-04-08T22:35:00+10:00'); // include timezone offset

function pad(n) { return String(n).padStart(2, '0'); }

function updateCountdown() {
  const diff = target - new Date();
  if (diff <= 0) { /* handle expiry */ return; }

  const days    = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours   = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);
}

updateCountdown();
setInterval(updateCountdown, 1000);
```

**Key rules:**
- Always hardcode the timezone offset in the ISO string (e.g. `+10:00` for AEST) — do not rely on the user's local timezone
- Check whether daylight saving is active on the target date (AEDT = UTC+11, AEST = UTC+10; clocks go back first Sunday of April)
- Call the function once immediately before `setInterval` to avoid a 1-second blank on load

---

## 6. Mobile Responsive Design

### Viewport height
```css
body { min-height: 100dvh; } /* dvh = dynamic viewport height */
```
`100vh` is clipped by mobile browser toolbars. `100dvh` adjusts for the toolbar dynamically.

### Three breakpoints used in this project
```
≤768px  — tablet:      modest padding reduction, globe/planes scale down
≤520px  — mobile:      further reduction, separators hidden, hearts gap reduced
≤380px  — small phone: minimum padding, tightest spacing
```

### Guaranteeing 4 units on one line
`flex-wrap: wrap` allows elements to drop to new lines. To prevent this:

```css
.countdown {
  flex-wrap: nowrap;
  gap: 0.35rem;
}
.unit {
  flex: 1 1 0;   /* grow and shrink equally */
  min-width: 0;  /* removes the implicit min-width constraint */
  padding: 0.75rem 0.25rem;
}
.number {
  font-size: clamp(1.5rem, 8vw, 2.5rem); /* scales with viewport */
}
```

`flex: 1 1 0` + `min-width: 0` is the key combination — units share available space equally and are allowed to shrink below their content size.

### Responsive sizing with min()
```css
.globe-scene {
  width: min(420px, 85vw);  /* never larger than 85% of viewport width */
}
```

### Scaling SVG elements via CSS
SVG presentation attributes (e.g. `font-size="90"`) can be overridden by CSS. Add a class to the element and target it in a media query:

```html
<text class="plane-1" font-size="90">✈</text>
```
```css
@media (max-width: 520px) {
  .plane-1 { font-size: 38px; }
}
```

---

## 7. Scalable Typography with clamp()

```css
font-size: clamp(MIN, PREFERRED, MAX);
```

- `MIN` — smallest size regardless of viewport
- `PREFERRED` — scales with viewport (use `vw` units)
- `MAX` — largest size on wide screens

Example: `clamp(1.5rem, 8vw, 3.75rem)` — at 375px wide = 30px, at 1200px = 96px capped at 60px.

---

## 8. VS Code File Conflict Warning

When Claude edits a file externally and VS Code has an unsaved version open, VS Code may overwrite the external change on save. If edits keep reverting:

1. Check for multiple open tabs of the same file — close duplicates
2. When VS Code shows "file modified outside editor" — choose **Discard Changes** to keep the version on disk
3. Enable auto-reload in VS Code settings: `"files.autoSave": "onFocusChange"`
