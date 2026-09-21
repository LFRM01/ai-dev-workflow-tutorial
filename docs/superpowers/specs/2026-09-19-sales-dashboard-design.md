# Design: E-Commerce Sales Dashboard

Source PRD: `prd/ecommerce-analytics.md`
Task board: `TASKS.md` (TASK-1 through TASK-7)

## Scope

This spec covers Phase 1 of the PRD: a single-page Streamlit sales dashboard reading from `data/sales-data.csv`. It does not cover Phase 2 items (auth, database integration, filtering, exports) — those are explicitly out of scope per the PRD.

Deployment to Streamlit Community Cloud (TASK-7) is included in the task board but is executed manually by the user after merging to `main`; this spec and the implementation plan built from it stop at handoff to that step.

## Architecture

Three files, one responsibility each:

- **`data.py`** — pure functions that take a DataFrame (or a CSV path for loading) and return calculations. Unit-tested with pytest.
- **`charts.py`** — Plotly figure-builder functions that take calculated data and return a `Figure`. Verified visually by running the app, not unit-tested.
- **`app.py`** — Streamlit layout and composition: calls `data.py` for numbers, passes them to `charts.py` for figures, renders the page.

This split keeps calculation logic (the part worth asserting exact values against) isolated from rendering (the part best checked by eye), matching the PRD's NFR-3 (modular structure) without over-engineering a small app.

## Data flow

1. `app.py` calls `data.load_sales_data(path)` to get the DataFrame, handling the load error path if it fails.
2. `app.py` calls the `data.py` aggregation functions to get KPI values and grouped DataFrames.
3. `app.py` passes those results to the corresponding `charts.py` builder functions to get Plotly `Figure` objects.
4. `app.py` renders KPIs via `st.metric`/formatted text and figures via `st.plotly_chart`.

## Components

### `data.py`

- `load_sales_data(path)` — reads the CSV; checks the file exists and required columns (`date`, `order_id`, `product`, `category`, `region`, `quantity`, `unit_price`, `total_amount`) are present. Raises a clear exception on failure for `app.py` to catch and surface via `st.error()` + `st.stop()`. Beyond this existence/columns guard, the data is trusted as-is — no type or range validation.
- `total_sales(df)` — sum of `total_amount`.
- `total_orders(df)` — row count.
- `sales_by_category(df)` — sum of `total_amount` grouped by `category`, sorted descending.
- `sales_by_region(df)` — sum of `total_amount` grouped by `region`, sorted descending.
- `monthly_sales_trend(df)` — sum of `total_amount` grouped by calendar month, in chronological order.

Each function takes a DataFrame as its only data parameter (no class/state wrapper), per the "keep it simple" preference.

### `charts.py`

- `trend_line_chart(monthly_df)` — Plotly line chart with interactive tooltips (FR-2).
- `category_bar_chart(category_df)` — Plotly bar chart, already-sorted input rendered as-is, with tooltips (FR-3).
- `region_bar_chart(region_df)` — Plotly bar chart, already-sorted input rendered as-is, with tooltips (FR-4).

### `app.py`

Layout follows the PRD's mockup, top to bottom:

1. Page title "ShopSmart Sales Dashboard" (using the company name from the PRD's Executive Summary; the mockup's "SHOPMART" is treated as a typo), `st.set_page_config` for wide layout.
2. KPI row: Total Sales (formatted as `$X,XXX,XXX`) and Total Orders (comma-separated integer), side by side via `st.columns`.
3. Sales trend line chart (monthly granularity — chosen over daily because 482 records across 12 months would make a daily chart noisy), full width.
4. Category and region bar charts side by side via `st.columns`.

## Error handling

Scoped to a basic guard, not full validation (per explicit decision): `load_sales_data` checks the file exists and the required columns are present. If either check fails, `app.py` shows a friendly `st.error()` message and calls `st.stop()`. No further validation (e.g. negative amounts, unparseable dates) is performed — the data is trusted once it passes this guard.

## Testing

`tests/test_data.py` tests `data.py` only. It uses a small, hand-crafted fixture DataFrame (4-5 rows spanning at least 2 categories, 2 regions, and 2 months) with known values, asserting exact expected results from each aggregation function (e.g. a specific total, a specific sort order). `charts.py` and `app.py` are not unit-tested; they're verified by running `streamlit run app.py` and checking the rendered output against the PRD's expected values (~$116,500 total sales, 482 orders, Electronics as top category).

## Dependencies and environment

- Plain Python virtual environment in `venv/` (no uv or conda).
- `requirements.txt` pins: `streamlit`, `pandas`, `plotly`, `pytest`.

## Out of scope

- Any Phase 2 item from the PRD (auth, real-time DB, exports, alerts, filtering, drill-down, mobile responsiveness).
- Automated deployment — TASK-7 is a manual step the user runs from `main` after merge; the implementation plan hands off there rather than scripting it.
