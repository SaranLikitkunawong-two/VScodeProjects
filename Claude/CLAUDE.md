# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A static single-page countdown timer website with no build system or dependencies. Open `home.html` directly in a browser to run it — no server required.

## Architecture

Two files make up the entire site:

- **`home.html`** — all markup and inline JavaScript. The countdown logic targets `2026-04-08T22:35:00+10:00` (Melbourne AEST). The SVG background contains three animated planes using SMIL `<animateMotion>` along `<path>` elements.
- **`style.css`** — all styling. Z-index layering: `z-index 0` = bg-scene (SVG planes), `z-index 1` = globe-scene (unused in current HTML but defined in CSS), `z-index 2` = page-wrapper (card).

## Key Implementation Notes

**Countdown timer:** Always hardcode the timezone offset in the ISO string (e.g. `+10:00` for AEST). April 8 is after the first Sunday of April, so AEST (UTC+10) applies — not AEDT (UTC+11).

**Heart shape:** CSS-only hearts using a rotated square (`rotate(-45deg)`) with `::before`/`::after` pseudo-elements as circles. Pulse animation must preserve the `-45deg` rotation: `transform: rotate(-45deg) scale(1.3)`.

**SVG plane animation:** Uses SMIL `<animateMotion>` with `<mpath href="#trail-id"/>` and `rotate="auto"`. The `begin="-Xs"` offset makes planes visible immediately on load rather than starting off-screen.

**Responsive breakpoints:** `≤768px` (tablet), `≤520px` (mobile — separators hidden, `flex-wrap: nowrap` with `flex: 1 1 0` + `min-width: 0` on `.unit`), `≤380px` (small phone). Uses `100dvh` (not `100vh`) for correct mobile viewport height.

**VS Code conflict:** If edits revert, VS Code may have an unsaved buffer open. When prompted "file modified outside editor", choose **Discard Changes** to keep the disk version.
