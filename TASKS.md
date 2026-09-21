# Tasks

This file tracks all work for the e-commerce analytics dashboard, from initial setup through deployment.

## Definition of Done

A milestone can move to Done only when:

- All of its acceptance criteria are met
- The app runs locally with `streamlit run app.py` without errors
- Changes are committed with the milestone ID (e.g. `TASK-1`) in the commit message

## To Do

## In Progress

## Done

### TASK-7: Deployment to Streamlit Community Cloud
- [x] App deployed and reachable via a public Streamlit Community Cloud URL
- [x] Deployed app matches local behavior (KPIs, charts, no errors)

Live URL: https://ai-dev-workflow-tutorial-uqvjz7usqbdhprhyxorlnr.streamlit.app/

Commit: ce67c1e (deployed from `main`; manual step, no separate implementation commit)

Notes: Deployed manually via Streamlit Community Cloud, pointing at `app.py` on `main`, per the plan's handoff note.

### TASK-6: Testing and refinement
- [x] Dashboard runs end-to-end with no errors or warnings
- [x] All values verified against expected calculations from the CSV
- [x] Layout and labels reviewed for a professional, executive-ready appearance

Commit: c9bb85b

Notes: Full pytest suite (8 tests) passed with no warnings before and after the change. Verified computed values directly against the PRD's expected output: Total Sales $116,500.21, Total Orders 482, top category Electronics, all four regions present. The plan's caption snippet showed it going directly under `st.title(...)`, but `df` isn't loaded until after the try/except block, so it was placed right after that instead — placing it earlier would raise a NameError.

### TASK-5: Category and region breakdowns
- [x] Bar chart shows sales by category, sorted highest to lowest, all categories shown
- [x] Bar chart shows sales by region, sorted highest to lowest, all regions shown
- [x] Both charts include interactive tooltips with exact values

Commit: 5f4e88a

Notes: Clean — implementation matched the plan exactly, no corrections needed.

### TASK-4: Sales trend chart
- [x] Line chart shows sales over time (daily or monthly granularity)
- [x] Chart includes interactive tooltips showing exact values

Commit: b13d4f4

Notes: Clean — implementation matched the plan exactly, no corrections needed.

### TASK-3: KPI cards implementation
- [x] Total Sales displayed, formatted as currency ($X,XXX,XXX)
- [x] Total Orders displayed, formatted with number separators
- [x] Values match expected output (~$116,500 total sales, 482 orders)

Commit: 50562be

Notes: Clean — implementation matched the plan exactly, no corrections needed.

### TASK-2: Data loading and basic structure
- [x] sales-data.csv loads into a Pandas DataFrame with correct dtypes (date, numeric, categorical)
- [x] Basic page layout/title in place

Commit: 1ec95db

Notes: The plan's `pytest tests/test_data.py -v` command failed with `ModuleNotFoundError: No module named 'data'` even after `data.py` existed, because the bare `pytest` entry point doesn't add the project root to `sys.path` when `tests/` has no `__init__.py`. Used `python -m pytest` instead, which does add the cwd to `sys.path`. This will apply to TASK-3 through TASK-6 as well.

### TASK-1: Environment setup and project initialization
- [x] Project structure created (app.py, requirements.txt, data/ folder)
- [x] Dependencies (streamlit, pandas, plotly) installed and pinned in requirements.txt
- [x] `streamlit run app.py` launches a blank/placeholder app with no errors

Commit: 959edd7

Notes: Claude briefly overwrote the repo's existing, more thorough `.gitignore` with a minimal 3-line version while scaffolding this task; caught via `git diff` and reverted before anything was committed, so no bad state landed. Also needed `streamlit run app.py --server.headless true` to avoid the first-run "onboarding email" prompt blocking non-interactive/background runs.
