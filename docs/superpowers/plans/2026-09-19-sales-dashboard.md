# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 Streamlit sales dashboard described in `prd/ecommerce-analytics.md` — KPI cards, a monthly sales trend chart, and category/region breakdown charts, reading from `data/sales-data.csv`.

**Architecture:** Three files, one responsibility each: `data.py` holds pure, pytest-tested calculation functions; `charts.py` holds Plotly figure-builder functions verified by running the app; `app.py` composes the two into the Streamlit page layout.

**Tech Stack:** Python 3, Streamlit, Pandas, Plotly, pytest, run inside a `venv/` virtual environment.

**Spec:** `docs/superpowers/specs/2026-09-19-sales-dashboard-design.md`

## Global Constraints

- Work on the current branch, `feature/sales-dashboard` — do not create a git worktree.
- Use a plain Python virtual environment in `venv/`, dependencies listed in `requirements.txt` — no `uv`, no `conda`.
- Data calculations live only in `data.py`, tested with pytest in `tests/test_data.py`. `charts.py` is verified by running the app, not unit-tested.
- Keep code simple and readable: plain functions taking a DataFrame, no class wrappers, no speculative abstraction.
- Each task below maps to exactly one milestone from `TASKS.md` (TASK-1 through TASK-7); every commit message includes that milestone ID.
- TASK-7 (deployment) is executed by the user, manually, from `main`, after this branch is merged — it is not automated by this plan.

---

### Plan Task 1 — TASK-1: Environment Setup and Project Skeleton

**Files:**
- Create: `requirements.txt`
- Create: `app.py`
- Create: `.gitignore`

**Interfaces:**
- Produces: a runnable `app.py` entry point that later tasks extend.

- [ ] **Step 1: Create the virtual environment**

Run: `python -m venv venv`

- [ ] **Step 2: Create `requirements.txt`**

```
streamlit>=1.30
pandas>=2.0
plotly>=5.20
pytest>=8.0
```

- [ ] **Step 3: Activate the venv and install dependencies**

Run (Git Bash): `source venv/Scripts/activate && pip install -r requirements.txt`
Run (PowerShell): `venv\Scripts\Activate.ps1; pip install -r requirements.txt`
Expected: all four packages install with no errors.

- [ ] **Step 4: Create `.gitignore`**

```
venv/
__pycache__/
*.pyc
```

- [ ] **Step 5: Create the minimal `app.py`**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 6: Run the app and verify it launches**

Run: `streamlit run app.py`
Expected: browser opens showing the title "ShopSmart Sales Dashboard", no errors in the terminal.

- [ ] **Step 7: Commit**

```bash
git add requirements.txt app.py .gitignore
git commit -m "TASK-1: initialize project skeleton and virtual environment"
```

---

### Plan Task 2 — TASK-2: Data Loading and Basic Structure

**Files:**
- Create: `data.py`
- Create: `tests/test_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: nothing from earlier tasks (first module in `data.py`).
- Produces: `load_sales_data(path: str) -> pandas.DataFrame`, raising `FileNotFoundError` if the file doesn't exist or `ValueError` if a required column is missing. Later tasks import this from `data.py`.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_data.py
import pandas as pd
import pytest

from data import load_sales_data


def test_load_sales_data_returns_dataframe_with_parsed_dates(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-05,ORD-001,Wireless Earbuds,Audio,North,2,79.99,159.98\n"
    )

    df = load_sales_data(str(csv_path))

    assert len(df) == 1
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df.loc[0, "total_amount"] == 159.98


def test_load_sales_data_raises_for_missing_file(tmp_path):
    missing_path = tmp_path / "does-not-exist.csv"

    with pytest.raises(FileNotFoundError):
        load_sales_data(str(missing_path))


def test_load_sales_data_raises_for_missing_required_column(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price\n"
        "2024-01-05,ORD-001,Wireless Earbuds,Audio,North,2,79.99\n"
    )

    with pytest.raises(ValueError):
        load_sales_data(str(csv_path))
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_data.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'data'` (the module doesn't exist yet).

- [ ] **Step 3: Write the implementation**

```python
# data.py
import os

import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category", "region",
    "quantity", "unit_price", "total_amount",
]


def load_sales_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Sales data file not found: {path}")

    df = pd.read_csv(path)

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Sales data is missing required columns: {missing_columns}")

    df["date"] = pd.to_datetime(df["date"])
    return df
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: all 3 tests PASS.

- [ ] **Step 5: Wire loading into `app.py`**

```python
# app.py
import streamlit as st

from data import load_sales_data

DATA_PATH = "data/sales-data.csv"

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

try:
    df = load_sales_data(DATA_PATH)
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()
```

- [ ] **Step 6: Run the app and verify no errors**

Run: `streamlit run app.py`
Expected: page loads with the title, no errors or tracebacks in the terminal.

- [ ] **Step 7: Commit**

```bash
git add data.py tests/test_data.py app.py
git commit -m "TASK-2: load and validate sales data from CSV"
```

---

### Plan Task 3 — TASK-3: KPI Cards Implementation

**Files:**
- Create: `tests/conftest.py`
- Modify: `data.py`
- Modify: `tests/test_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data` from Plan Task 2, and the shared `sample_sales_df` pytest fixture defined in this task (reused by Plan Tasks 4 and 5).
- Produces: `total_sales(df: pandas.DataFrame) -> float` and `total_orders(df: pandas.DataFrame) -> int`.

- [ ] **Step 1: Create the shared test fixture**

```python
# tests/conftest.py
import pandas as pd
import pytest


@pytest.fixture
def sample_sales_df():
    return pd.DataFrame({
        "date": pd.to_datetime([
            "2024-01-05", "2024-01-20", "2024-02-10", "2024-02-15", "2024-03-01",
        ]),
        "order_id": ["ORD-001", "ORD-002", "ORD-003", "ORD-004", "ORD-005"],
        "product": [
            "Wireless Earbuds", "Phone Case", "Smart Watch",
            "USB-C Cable", "Bluetooth Speaker",
        ],
        "category": ["Audio", "Accessories", "Wearables", "Accessories", "Audio"],
        "region": ["North", "South", "East", "West", "North"],
        "quantity": [2, 3, 1, 5, 1],
        "unit_price": [79.99, 24.99, 299.99, 12.99, 149.99],
        "total_amount": [159.98, 74.97, 299.99, 64.95, 149.99],
    })
```

- [ ] **Step 2: Write the failing tests**

```python
# add to tests/test_data.py
from data import total_orders, total_sales


def test_total_sales(sample_sales_df):
    assert total_sales(sample_sales_df) == pytest.approx(749.88)


def test_total_orders(sample_sales_df):
    assert total_orders(sample_sales_df) == 5
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `pytest tests/test_data.py -v`
Expected: FAIL with `ImportError: cannot import name 'total_sales' from 'data'`.

- [ ] **Step 4: Write the implementation**

```python
# add to data.py
def total_sales(df):
    return df["total_amount"].sum()


def total_orders(df):
    return len(df)
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: all tests PASS.

- [ ] **Step 6: Add KPI cards to `app.py`**

```python
# app.py — add to imports and to the bottom of the file
from data import load_sales_data, total_orders, total_sales

# ... after the try/except load block ...
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(df):,.0f}")
col2.metric("Total Orders", f"{total_orders(df):,}")
```

- [ ] **Step 7: Run the app and verify the KPI values**

Run: `streamlit run app.py`
Expected: Total Sales shows approximately $116,500 and Total Orders shows 482, matching the PRD's expected output.

- [ ] **Step 8: Commit**

```bash
git add tests/conftest.py tests/test_data.py data.py app.py
git commit -m "TASK-3: add KPI cards for total sales and orders"
```

---

### Plan Task 4 — TASK-4: Sales Trend Chart

**Files:**
- Create: `charts.py`
- Modify: `data.py`
- Modify: `tests/test_data.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `sample_sales_df` fixture from Plan Task 3.
- Produces: `monthly_sales_trend(df: pandas.DataFrame) -> pandas.Series` (indexed by month start, chronological order) from `data.py`, and `trend_line_chart(monthly_series: pandas.Series) -> plotly.graph_objects.Figure` from `charts.py`.

- [ ] **Step 1: Write the failing test**

```python
# add to tests/test_data.py
from data import monthly_sales_trend


def test_monthly_sales_trend(sample_sales_df):
    trend = monthly_sales_trend(sample_sales_df)

    assert list(trend.index.strftime("%Y-%m")) == ["2024-01", "2024-02", "2024-03"]
    assert trend.iloc[0] == pytest.approx(234.95)
    assert trend.iloc[1] == pytest.approx(364.94)
    assert trend.iloc[2] == pytest.approx(149.99)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_data.py -v`
Expected: FAIL with `ImportError: cannot import name 'monthly_sales_trend' from 'data'`.

- [ ] **Step 3: Write the implementation**

```python
# add to data.py
def monthly_sales_trend(df):
    monthly = df.groupby(df["date"].dt.to_period("M"))["total_amount"].sum()
    monthly.index = monthly.index.to_timestamp()
    return monthly.sort_index()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_data.py -v`
Expected: all tests PASS.

- [ ] **Step 5: Create `charts.py` with the trend chart builder**

```python
# charts.py
import plotly.express as px


def trend_line_chart(monthly_series):
    fig = px.line(
        x=monthly_series.index,
        y=monthly_series.values,
        labels={"x": "Month", "y": "Total Sales ($)"},
        title="Sales Trend Over Time",
    )
    fig.update_traces(mode="lines+markers", hovertemplate="%{x|%B %Y}: $%{y:,.2f}")
    return fig
```

- [ ] **Step 6: Add the trend chart to `app.py`**

```python
# app.py — add to imports and to the bottom of the file
from data import load_sales_data, monthly_sales_trend, total_orders, total_sales
from charts import trend_line_chart

# ... after the KPI columns ...
st.plotly_chart(trend_line_chart(monthly_sales_trend(df)), use_container_width=True)
```

- [ ] **Step 7: Run the app and verify the trend chart**

Run: `streamlit run app.py`
Expected: a line chart with 12 monthly points appears below the KPI cards; hovering a point shows the month and exact dollar value.

- [ ] **Step 8: Commit**

```bash
git add charts.py data.py tests/test_data.py app.py
git commit -m "TASK-4: add monthly sales trend chart"
```

---

### Plan Task 5 — TASK-5: Category and Region Breakdowns

**Files:**
- Modify: `data.py`
- Modify: `tests/test_data.py`
- Modify: `charts.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `sample_sales_df` fixture from Plan Task 3.
- Produces: `sales_by_category(df) -> pandas.Series` and `sales_by_region(df) -> pandas.Series` (both indexed by name, sorted descending) from `data.py`; `category_bar_chart(category_series) -> plotly.graph_objects.Figure` and `region_bar_chart(region_series) -> plotly.graph_objects.Figure` from `charts.py`.

- [ ] **Step 1: Write the failing tests**

```python
# add to tests/test_data.py
from data import sales_by_category, sales_by_region


def test_sales_by_category_sorted_descending(sample_sales_df):
    result = sales_by_category(sample_sales_df)

    assert list(result.index) == ["Audio", "Wearables", "Accessories"]
    assert result.iloc[0] == pytest.approx(309.97)


def test_sales_by_region_sorted_descending(sample_sales_df):
    result = sales_by_region(sample_sales_df)

    assert list(result.index) == ["North", "East", "South", "West"]
    assert result.iloc[0] == pytest.approx(309.97)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_data.py -v`
Expected: FAIL with `ImportError: cannot import name 'sales_by_category' from 'data'`.

- [ ] **Step 3: Write the implementation**

```python
# add to data.py
def sales_by_category(df):
    return df.groupby("category")["total_amount"].sum().sort_values(ascending=False)


def sales_by_region(df):
    return df.groupby("region")["total_amount"].sum().sort_values(ascending=False)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_data.py -v`
Expected: all tests PASS.

- [ ] **Step 5: Add the bar chart builders to `charts.py`**

```python
# add to charts.py
def category_bar_chart(category_series):
    fig = px.bar(
        x=category_series.index,
        y=category_series.values,
        labels={"x": "Category", "y": "Total Sales ($)"},
        title="Sales by Category",
    )
    fig.update_traces(hovertemplate="%{x}: $%{y:,.2f}")
    return fig


def region_bar_chart(region_series):
    fig = px.bar(
        x=region_series.index,
        y=region_series.values,
        labels={"x": "Region", "y": "Total Sales ($)"},
        title="Sales by Region",
    )
    fig.update_traces(hovertemplate="%{x}: $%{y:,.2f}")
    return fig
```

- [ ] **Step 6: Add the breakdown charts to `app.py`**

```python
# app.py — add to imports and to the bottom of the file
from data import (
    load_sales_data,
    monthly_sales_trend,
    sales_by_category,
    sales_by_region,
    total_orders,
    total_sales,
)
from charts import category_bar_chart, region_bar_chart, trend_line_chart

# ... after the trend chart ...
col3, col4 = st.columns(2)
col3.plotly_chart(category_bar_chart(sales_by_category(df)), use_container_width=True)
col4.plotly_chart(region_bar_chart(sales_by_region(df)), use_container_width=True)
```

- [ ] **Step 7: Run the app and verify both charts**

Run: `streamlit run app.py`
Expected: category chart shows Electronics as the tallest bar; region chart shows North, South, East, West all present; both sorted highest to lowest with tooltips.

- [ ] **Step 8: Commit**

```bash
git add data.py tests/test_data.py charts.py app.py
git commit -m "TASK-5: add category and region breakdown charts"
```

---

### Plan Task 6 — TASK-6: Testing and Refinement

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: the complete `data.py` and `charts.py` modules from Plan Tasks 2–5.
- Produces: no new functions — this task verifies and polishes what exists.

- [ ] **Step 1: Run the full test suite**

Run: `pytest -v`
Expected: all tests across `tests/test_data.py` PASS, no warnings.

- [ ] **Step 2: Add a data-range caption for a more polished, executive-ready presentation**

```python
# app.py — add directly under st.title(...)
st.caption(f"Data from {df['date'].min():%B %Y} to {df['date'].max():%B %Y}")
```

- [ ] **Step 3: Run the app and verify against the PRD's expected output**

Run: `streamlit run app.py`
Expected, matching `prd/ecommerce-analytics.md`'s Expected Output table:
- Total Sales ≈ $116,500
- Total Orders = 482
- Top category bar = Electronics
- Region chart shows North, South, East, West
- No errors or warnings in the terminal or browser console

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "TASK-6: verify calculations and refine dashboard presentation"
```

---

### Plan Task 7 — TASK-7: Deployment (User Action — Not Automated)

**This task is executed by you, not by whoever implements Plan Tasks 1-6.** It happens after this branch is reviewed and merged into `main`. Nothing in this plan automates it; it's recorded here so the task board's milestones stay complete.

- [ ] Merge `feature/sales-dashboard` into `main`.
- [ ] From `main`, push the repository to GitHub if it isn't already there.
- [ ] Deploy via Streamlit Community Cloud (share.streamlit.io), pointing at `app.py` on `main`.
- [ ] Open the resulting public URL and verify it matches local behavior: KPIs, all three charts, no errors — satisfying TASK-7's acceptance criteria in `TASKS.md`.

**Implementation of this plan stops at the end of Plan Task 6.** Hand off to the user here.
