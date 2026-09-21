# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two things layered on top of each other:

1. **Tutorial curriculum** (`README.md`, `pre-work-setup.md`, `workshop-build-deploy.md`, `codex-companion.md`, `capstone-tools.md`) — a course that teaches a PRD → tasks → plan → code → deploy workflow using Claude Code and the Superpowers skill add-on.
2. **The capstone project itself**: a Streamlit e-commerce sales dashboard (`app.py`, `data.py`, `charts.py`, `tests/`), being built by following that exact workflow. `TASKS.md` is the live task board for this project — check it before starting work to see what's done, in progress, or next.

When making changes to the dashboard code, follow the process the curriculum teaches rather than jumping straight to code: PRD (`prd/ecommerce-analytics.md`) → milestone in `TASKS.md` → design spec / implementation plan under `docs/superpowers/` → implementation → mark the milestone done. The existing plan (`docs/superpowers/plans/2026-09-19-sales-dashboard.md`) and spec (`docs/superpowers/specs/2026-09-19-sales-dashboard-design.md`) already cover TASK-1 through TASK-7; only deviate from them with a stated reason (see the "Notes" field pattern in `TASKS.md`).

## Commands

Activate the existing virtual environment before running anything (Git Bash: `source venv/Scripts/activate`; PowerShell: `venv\Scripts\Activate.ps1`).

```bash
pip install -r requirements.txt        # install/sync dependencies

streamlit run app.py                   # run the dashboard
streamlit run app.py --server.headless true   # non-interactive/background runs — skips the first-run onboarding-email prompt that otherwise blocks

python -m pytest -v                    # run the full test suite
python -m pytest tests/test_data.py::test_total_sales -v   # run a single test
```

Always invoke pytest as `python -m pytest`, not bare `pytest` — `tests/` has no `__init__.py`, so the bare entry point doesn't add the project root to `sys.path` and imports of `data` fail with `ModuleNotFoundError`.

## Architecture

Three files, one responsibility each (per the design spec's modularity requirement, without over-engineering a small app):

- **`data.py`** — pure functions taking a DataFrame (or a CSV path for `load_sales_data`) and returning calculations: `total_sales`, `total_orders`, `monthly_sales_trend`, `sales_by_category`, `sales_by_region`. This is the only module unit-tested with pytest, because it's the only part worth asserting exact values against.
- **`charts.py`** — Plotly figure-builder functions (`trend_line_chart`, `category_bar_chart`, `region_bar_chart`) that take already-computed data from `data.py` and return a `Figure`. Not unit-tested; verified by running the app and checking the rendered chart.
- **`app.py`** — Streamlit page composition only: calls into `data.py` for numbers, passes them to `charts.py` for figures, renders via `st.metric`/`st.plotly_chart`. Loads `data/sales-data.csv` through `load_sales_data`, catching `FileNotFoundError`/`ValueError` to show `st.error()` + `st.stop()` rather than crashing.

`tests/conftest.py` defines a shared `sample_sales_df` fixture (5 hand-crafted rows spanning 2+ categories/regions/months with known aggregate values) used across `tests/test_data.py` — extend that fixture rather than creating a new one when adding tests for new `data.py` functions.

Expected real-data values (from `data/sales-data.csv`, per the PRD): Total Sales ≈ $116,500, Total Orders = 482, Electronics is the top category, all four regions (North/South/East/West) present. Use these to sanity-check changes to the aggregation functions.

## Lessons

Distilled from the "Notes" lines in `TASKS.md` — rules to avoid repeating past corrections:

- Run tests with `python -m pytest`, never bare `pytest`. `tests/` has no `__init__.py`, so the bare entry point doesn't add the project root to `sys.path` and fails with `ModuleNotFoundError: No module named 'data'` even when `data.py` exists. (TASK-2)
- Run `streamlit run app.py --server.headless true` for any non-interactive/background launch. Without `--server.headless true`, the first run blocks on an onboarding-email prompt. (TASK-1)
- Before scaffolding new project files, check whether one already exists and diff before committing. A `.gitignore` was briefly overwritten with a minimal 3-line version during initial scaffolding, discarding the repo's existing, more thorough one — caught via `git diff` before it was committed, but only because it was checked. (TASK-1)
- When a plan snippet shows *where* to insert a line (e.g. "add directly under `st.title(...)`"), verify the variables it references are actually in scope at that point before placing it there — follow the plan's intent, not the literal line position, if the two conflict. A caption depending on `df` couldn't go where the plan snippet showed it, since `df` isn't loaded until after the try/except block that follows. (TASK-6)

## Task board conventions (`TASKS.md`)

- A task moves To Do → In Progress → Done; Done entries carry the commit hash and a "Notes" line recording any deviation from the plan (or "Clean" if none).
- Each milestone is typically two commits: one implementing the change with the milestone ID in the message (e.g. `TASK-4: add monthly sales trend chart`), and a separate one moving it to Done on the board (e.g. `TASK-4: mark done on the board`).
- TASK-7 (Streamlit Community Cloud deployment) is explicitly a manual step the user runs from `main` after merging — no plan or skill automates it.
