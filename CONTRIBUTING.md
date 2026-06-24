# Contributing to Nek-Portal

Thanks for considering a contribution. 
This is a small student-built tool, so
the bar is simple: keep it working, keep it readable.

## Rules
- Be respectful and collaborative.
- Do not commit directly to the `main` branch. All changes must go through a Pull Request (PR).
- Ensure your code follows the existing style format before submitting.

## Setup

```bash
git clone https://github.com/<your-username>/nek-portal.git
cd nek-portal
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python main.py
```

## Before you open a PR

1. Check open issues — someone might already be working on it.
2. For anything non-trivial, open an issue first to discuss the approach.
3. Keep PRs focused — one fix/feature per PR, not a grab-bag.
4. Test that `python main.py` still runs and a live sync still works
   end-to-end before submitting.

## Code style

- Keep functions short and single-purpose.
- No secrets, session data, or `nek_profile*/` folders in commits.
- Match existing naming/formatting in the file you're editing.

## Reporting bugs / requesting features

Use the issue templates — they ask for exactly what's needed to act on it
(repro steps, environment, expected vs actual behavior).

## Questions

Open a Discussion or an issue tagged `question`. No formal process beyond that.
