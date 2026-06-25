# BUNKEE

**A desktop attendance dashboard for GEHU students.**

Logs into the college ERP, pulls your live attendance, and does the math
you'd otherwise do in your head every morning — exactly how many classes
you can skip (or need to attend) before you drop below 70% or 75%.

Smash the ⭐ if bunkee fw you heavy.

Want to contribute? 
  redirect to the contribution tab.

## What it actually does
- Auto-handles ERP login via a persistent browser session — no re-login every run
- Per-subject breakdown: attended / conducted / live %
- **Bunk Score** — max classes safely skippable while staying ≥ 70%
- **Recovery Count** — classes needed to hit 70% or 75% if you're below it
- Color-coded zones: 🟢 Free Zone (≥80%) · 🟩 Safe (≥75%) · 🟡 Warning (≥70%) · 🔴 Danger (<70%)

**Stack:** Python · Flet · Playwright
