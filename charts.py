import plotly.express as px


def trend_line_chart(monthly_series):
    fig = px.line(
        x=monthly_series.index,
        y=monthly_series.values,
        labels={"x": "Month", "y": "Total Sales ($)"},
        title="Sales Trend Over Time",
    )
    fig.update_traces(mode="lines+markers", hovertemplate="%{x|%B %Y}: $%{y:,.2f}<extra></extra>")
    return fig


def category_bar_chart(category_series):
    fig = px.bar(
        x=category_series.index,
        y=category_series.values,
        labels={"x": "Category", "y": "Total Sales ($)"},
        title="Sales by Category",
    )
    fig.update_traces(hovertemplate="%{x}: $%{y:,.2f}<extra></extra>")
    return fig


def region_bar_chart(region_series):
    fig = px.bar(
        x=region_series.index,
        y=region_series.values,
        labels={"x": "Region", "y": "Total Sales ($)"},
        title="Sales by Region",
    )
    fig.update_traces(hovertemplate="%{x}: $%{y:,.2f}<extra></extra>")
    return fig
