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
