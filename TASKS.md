# Tasks

This file tracks all work for the e-commerce analytics dashboard, from initial setup through deployment.

## Definition of Done

A milestone can move to Done only when:

- All of its acceptance criteria are met
- The app runs locally with `streamlit run app.py` without errors
- Changes are committed with the milestone ID (e.g. `TASK-1`) in the commit message

## To Do

### TASK-4: Sales trend chart
- [ ] Line chart shows sales over time (daily or monthly granularity)
- [ ] Chart includes interactive tooltips showing exact values

Commit:

### TASK-5: Category and region breakdowns
- [ ] Bar chart shows sales by category, sorted highest to lowest, all categories shown
- [ ] Bar chart shows sales by region, sorted highest to lowest, all regions shown
- [ ] Both charts include interactive tooltips with exact values

Commit:

### TASK-6: Testing and refinement
- [ ] Dashboard runs end-to-end with no errors or warnings
- [ ] All values verified against expected calculations from the CSV
- [ ] Layout and labels reviewed for a professional, executive-ready appearance

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
- [ ] App deployed and reachable via a public Streamlit Community Cloud URL
- [ ] Deployed app matches local behavior (KPIs, charts, no errors)

Commit:

## In Progress

## Done

### TASK-3: KPI cards implementation
- [x] Total Sales displayed, formatted as currency ($X,XXX,XXX)
- [x] Total Orders displayed, formatted with number separators
- [x] Values match expected output (~$116,500 total sales, 482 orders)

Commit: 50562be

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
