import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

from db import Database
from dash_layout import (
    navbar,
    review_count_row,
    author_genre_row,
    distribution_row,
    controls,
    compare_row,
    top_metrics_row,
    series_row,
)
from figures import make_reviews_counts_fig, make_top_authors_fig, make_top_genres_fig

# --------------------------------------------------
# Data
# --------------------------------------------------

db = Database()
books_df = db.get_books()
recs_df = db.get_recommendations()

series = {
    "Harry Potter": [
        "Harry Potter and the Sorcerer's Stone",
        "Harry Potter and the Sorcerer's Stone",
        "Harry Potter and the Chamber of Secrets",
        "Harry Potter and the Prisoner of Azkaban",
        "Harry Potter and the Goblet of Fire",
        "Harry Potter and the Order of the Phoenix",
        "Harry Potter and the Half-Blood Prince",
        "Harry Potter and the Deathly Hallows",
    ],
    "The Chronicles of Narnia": [
        "The Lion, the Witch and the Wardrobe",
        "Prince Caspian",
        "The Voyage of the Dawn Treader",
        "The Silver Chair",
        "The Horse and His Boy",
        "The Magician's Nephew",
        "The Last Battle",
    ],
}

# --------------------------------------------------

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# --------------------------------------------------
# Layout
# --------------------------------------------------

app.layout = dbc.Container(
    fluid=True,
    children=[
        navbar,
        *review_count_row,
        *author_genre_row,
        top_metrics_row,
        *distribution_row,
        *controls,
        *compare_row,
        series_row,
    ],
)


@app.callback(
    Output("reviews-count-graph", "figure"), Input("init-once", "n_intervals")
)
def build_reviews_counts(_):
    return make_reviews_counts_fig(books_df)


@app.callback(
    Output("top-authors-graph", "figure"), Input("top-authors-slider", "value")
)
def build_top_authors(n):
    return make_top_authors_fig(books_df, n)


@app.callback(Output("top-genres-graph", "figure"), Input("top-genres-slider", "value"))
def build_top_genres(n):
    return make_top_genres_fig(books_df, n)


def _safe_series(df: pd.DataFrame, col: str) -> pd.Series:
    s = pd.to_numeric(df[col], errors="coerce").dropna()
    return s.clip(lower=0, upper=5)  # keep common [0,5] scale


def _pretty(col: str) -> str:
    return col.replace("_", " ").title()


@app.callback(
    Output("top50-title", "children"),
    Output("top10-title", "children"),
    Output("top50-generic-list", "children"),
    Output("top10-generic-graph", "figure"),
    Input("metric-select", "value"),
    prevent_initial_call=False,
)
def update_top_metrics(metric_col):
    if metric_col not in {"rating", "featured_rating", "sentiment_score"}:
        metric_col = "rating"

    df = books_df.copy()
    if "title" not in df.columns:
        df["title"] = df.index.astype(str)

    s = _safe_series(df, metric_col)
    df = df.loc[s.index].copy()
    df[metric_col] = s

    pretty = _pretty(metric_col)

    top50 = df.sort_values(by=metric_col, ascending=False).head(50)
    list_items = []
    for i, row in enumerate(top50.itertuples(index=False), start=1):
        list_items.append(
            dbc.ListGroupItem(
                dbc.Row(
                    [
                        dbc.Col(html.Span(f"{i:02d}"), width=2),
                        dbc.Col(html.Span(getattr(row, "title")), width=8),
                        dbc.Col(
                            html.Span(f"{getattr(row, metric_col):.2f}"),
                            width=2,
                            className="text-end",
                        ),
                    ],
                    align="center",
                    className="g-0",
                )
            )
        )

    top10 = top50.head(10).iloc[::-1]  # highest at top
    fig = px.bar(
        top10,
        x=metric_col,
        y="title",
        orientation="h",
        text=top10[metric_col].round(2),
        title="",
    )

    fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(color="white"),
        cliponaxis=False,
        hovertemplate=f"{pretty}: %{{x:.2f}}<extra></extra>",
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        height=600,
        xaxis_title=pretty,
        yaxis_title=None,
        showlegend=False,
        uniformtext_minsize=10,
        uniformtext_mode="hide",
    )
    fig.update_xaxes(range=[0, 5])
    return (
        f"Top 50 Books by {pretty}",
        f"Top 10 Books by {pretty}",
        list_items,
        fig,
    )


def build_hist_figure(df, col, bin_edges, title, y_max=150):
    s = df[col].dropna()
    counts, edges = np.histogram(s, bins=bin_edges)
    centers = (edges[:-1] + edges[1:]) / 2.0
    widths = np.diff(edges)

    min_val = float(s.min()) if len(s) else None
    median_val = float(s.median()) if len(s) else None
    mean_val = float(s.mean()) if len(s) else None
    max_val = float(s.max()) if len(s) else None

    fig = go.Figure()

    fig.add_bar(
        x=centers,
        y=counts,
        width=widths,
        text=[str(int(c)) if c > 0 else "" for c in counts],
        textposition="outside",
        hovertemplate="Bin: %{x}<br>Count: %{y}<extra></extra>",
        name="Count",
        showlegend=False,
    )

    # Vertical summary lines (use scatter lines so they appear in legend)
    def add_vline_line(xval, name, dash, color):
        if xval is None:
            return
        fig.add_trace(
            go.Scatter(
                x=[xval, xval],
                y=[0, max(max(counts), y_max if y_max else 0)],
                mode="lines",
                line=dict(dash=dash, width=2, color=color),
                name=f"{name}: {xval:.2f}",
                hoverinfo="skip",
            )
        )

    add_vline_line(min_val, "Min", "dash", "gray")
    add_vline_line(median_val, "Median", "dash", "blue")
    add_vline_line(mean_val, "Mean", "dash", "green")
    add_vline_line(max_val, "Max", "dash", "red")

    fig.update_layout(
        title=title,
        xaxis_title="Rating",
        yaxis_title="Number of Books",
        margin=dict(l=10, r=10, t=30, b=10),
        height=300,
        bargap=0.05,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(tickvals=bin_edges, range=[bin_edges[0], bin_edges[-1]])
    if y_max:
        fig.update_yaxes(range=[0, y_max])

    return fig


@app.callback(
    Output("rating-dist-hist", "figure"),
    Input("rating-dist-hist", "id"),
    prevent_initial_call=False,
)
def update_rating_hist(_):
    bins = np.arange(0, 5.5, 0.5)
    return build_hist_figure(books_df, "rating", bins, "", y_max=150)


@app.callback(
    Output("featured-rating-dist-hist", "figure"),
    Input("featured-rating-dist-hist", "id"),
    prevent_initial_call=False,
)
def update_featured_rating_hist(_):
    bins = np.arange(0, 5.5, 0.5)
    return build_hist_figure(books_df, "featured_rating", bins, "", y_max=150)


@app.callback(
    Output("sentiment-dist-hist", "figure"),
    Input("sentiment-dist-hist", "id"),
    prevent_initial_call=False,
)
def update_sentiment_hist(_):
    bins = np.arange(0, 5.5, 0.5)  # sentiment_score in [0, 5]
    fig = build_hist_figure(books_df, "sentiment_score", bins, "", y_max=150)
    fig.update_layout(xaxis_title="Sentiment Score")
    return fig


def _coerce_and_clip01(df, cols):
    # ensure numeric and clip to [0,5] to keep scales consistent
    out = df[list(cols)].apply(pd.to_numeric, errors="coerce").clip(lower=0, upper=5)
    return out.dropna()


@app.callback(
    Output("diff-bar", "figure"),
    Output("xy-scatter", "figure"),
    Input("metric-x", "value"),
    Input("metric-y", "value"),
    prevent_initial_call=False,
)
def update_compare_plots(col_x, col_y):
    if col_x is None or col_y is None:
        col_x, col_y = "rating", "featured_rating"

    df = _coerce_and_clip01(books_df, [col_x, col_y])
    if df.empty:
        return go.Figure(), go.Figure()

    x_vals = df[col_x].values
    y_vals = df[col_y].values
    diff = y_vals - x_vals

    order = np.argsort(diff)
    diff_sorted = diff[order]

    # Colors: red (<0), green (>0), blue (=0)
    colors = np.where(
        diff_sorted < 0, "red", np.where(diff_sorted > 0, "green", "blue")
    )

    fig_bar = go.Figure()
    fig_bar.add_bar(
        x=np.arange(len(diff_sorted)),
        y=diff_sorted,
        marker_color=colors,
        hovertemplate="Index: %{x}<br>Y−X: %{y:.3f}<extra></extra>",
        name="Y − X",
        showlegend=False,
    )
    fig_bar.update_layout(
        title=f"{col_y} − {col_x} for All Books (sorted)",
        xaxis_title="Books (Index Sorted by Difference)",
        yaxis_title="Rating Difference",
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
    )

    rmse = float(np.sqrt(np.mean((y_vals - x_vals) ** 2)))
    # guard against std=0 for constant arrays
    if np.std(x_vals) > 0 and np.std(y_vals) > 0:
        corr = float(np.corrcoef(x_vals, y_vals)[0, 1])
    else:
        corr = float("nan")

    fig_scatter = go.Figure()
    fig_scatter.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="markers",
            name=f"{col_y} vs {col_x}",
            hovertemplate=f"{col_x}: %{{x:.3f}}<br>{col_y}: %{{y:.3f}}<extra></extra>",
        )
    )
    fig_scatter.add_trace(
        go.Scatter(
            x=[0, 5],
            y=[0, 5],
            mode="lines",
            line=dict(dash="dash", width=2, color="gray"),
            name="y = x",
            hoverinfo="skip",
        )
    )
    fig_scatter.add_annotation(
        x=0.5,
        y=4.2,
        xref="x",
        yref="y",
        showarrow=False,
        text=f"RMSE = {rmse:.3f}",
        font=dict(size=12),
    )
    fig_scatter.add_annotation(
        x=0.5,
        y=3.8,
        xref="x",
        yref="y",
        showarrow=False,
        text=f"Pearson r = {corr:.3f}" if np.isfinite(corr) else "Pearson r = N/A",
        font=dict(size=12),
    )

    fig_scatter.update_layout(
        title=f"{col_x} (X) vs {col_y} (Y)",
        xaxis_title=col_x.replace("_", " ").title(),
        yaxis_title=col_y.replace("_", " ").title(),
        margin=dict(l=10, r=10, t=40, b=10),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=0.9, xanchor="left", x=0),
    )
    fig_scatter.update_xaxes(range=[0, 5])
    fig_scatter.update_yaxes(range=[0, 5])

    return fig_bar, fig_scatter


def _norm(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower()


def _ensure_year(df: pd.DataFrame) -> str:
    # falls back to parsing start_date if a year column isn't already present
    if "year" in df.columns:
        return "year"
    if "start_date" in df.columns:
        return "year"
    raise KeyError("No 'year' (or 'start_date') column found in books_df")


@app.callback(
    Output("series-trend-graph", "figure"),
    Input("series-select", "value"),
    prevent_initial_call=False,
)
def update_series_trend(selected_series):
    if selected_series not in series:
        selected_series = list(series.keys())[0]

    titles = series[selected_series]
    titles_norm = {t.strip().lower() for t in titles}

    df = books_df.copy()

    year_col = _ensure_year(df)
    if year_col != "year" and "year" not in df.columns:
        df["year"] = pd.to_datetime(df["start_date"], errors="coerce").dt.year
        year_col = "year"

    df["title_norm"] = _norm(df["title"])
    sub = df[df["title_norm"].isin(titles_norm)].copy()

    for c in ["rating", "featured_rating", "sentiment_score"]:
        sub[c] = pd.to_numeric(sub[c], errors="coerce").clip(lower=0, upper=5)

    # Aggregate by year (mean in case multiple books per year)
    agg = (
        sub.groupby(year_col, as_index=False)[
            ["rating", "featured_rating", "sentiment_score"]
        ]
        .mean()
        .sort_values(year_col)
    )

    fig = go.Figure()
    traces = [
        ("rating", "Rating"),
        ("featured_rating", "Featured Rating"),
        ("sentiment_score", "Sentiment Score"),
    ]
    for col, name in traces:
        if col in agg.columns and not agg[col].isna().all():
            fig.add_trace(
                go.Scatter(
                    x=agg[year_col],
                    y=agg[col],
                    mode="lines+markers",
                    name=name,
                    hovertemplate=f"Year: %{{x}}<br>{name}: %{{y:.2f}}<extra></extra>",
                )
            )

    fig.update_layout(
        title="",
        xaxis_title="Year of Release",
        yaxis_title="Score",
        margin=dict(l=10, r=10, t=50, b=10),
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_yaxes(range=[0, 5])

    # If there are few points, widen the x range slightly for padding
    if len(agg[year_col]) >= 1:
        xmin, xmax = agg[year_col].min(), agg[year_col].max()
        if pd.notna(xmin) and pd.notna(xmax) and xmin != xmax:
            pad = max(1, int((xmax - xmin) * 0.05))
            fig.update_xaxes(range=[xmin - pad, xmax + pad])

    return fig


if __name__ == "__main__":
    app.run(debug=True)
