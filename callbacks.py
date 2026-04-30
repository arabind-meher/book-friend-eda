import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Input, Output, html
from app import app, books_df  # 👈 reuse app + data


# --------------------------------
# Reviews Counts
# --------------------------------
@app.callback(
    Output("reviews-count-graph", "figure"),
    Input("init-once", "n_intervals"),
)
def build_reviews_counts(_):
    review_stats = (
        books_df["reviews_count"].agg(["min", "mean", "median", "max"]).round(2)
    )
    sorted_books_full = books_df.sort_values(
        by="reviews_count", ascending=True
    ).reset_index(drop=True)
    sorted_books_full["index"] = sorted_books_full.index

    fig = go.Figure()
    fig.add_bar(
        x=sorted_books_full["index"],
        y=sorted_books_full["reviews_count"],
        marker_color="steelblue",
        name="Reviews",
    )

    x_range = np.array(
        [sorted_books_full["index"].min(), sorted_books_full["index"].max()]
    )
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=[review_stats["min"]] * 2,
            mode="lines",
            line=dict(color="orange", dash="dash"),
            name="Min",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=[review_stats["mean"]] * 2,
            mode="lines",
            line=dict(color="green", dash="dash"),
            name="Mean",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=[review_stats["median"]] * 2,
            mode="lines",
            line=dict(color="purple", dash="dash"),
            name="Median",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=[review_stats["max"]] * 2,
            mode="lines",
            line=dict(color="black", dash="dash"),
            name="Max",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=[100] * 2,
            mode="lines",
            line=dict(color="red", dash="solid"),
            name="Y=100",
        )
    )

    fig.update_layout(
        title="Books Sorted by Review Count",
        template="plotly_white",
        xaxis=dict(title=None, showticklabels=False),
        yaxis_title="Review Count",
        margin=dict(l=20, r=20, t=40, b=60),
    )
    return fig


# --------------------------------
# Top Authors
# --------------------------------
@app.callback(
    Output("top-authors-graph", "figure"),
    Input("top-authors-slider", "value"),
)
def build_top_authors(n):
    author_stats = (
        books_df.groupby("author", dropna=True)["featured_rating"]
        .count()
        .reset_index(name="book_count")
    )
    top_authors = author_stats.sort_values("book_count", ascending=False).head(int(n))

    fig = go.Figure()
    fig.add_bar(
        x=top_authors["author"],
        y=top_authors["book_count"],
        marker_color="steelblue",
        showlegend=False,
    )

    for _, row in top_authors.iterrows():
        fig.add_annotation(
            x=row["author"],
            y=row["book_count"] + 0.5,
            text=str(int(row["book_count"])),
            showarrow=False,
            font=dict(size=10, color="steelblue"),
            yanchor="bottom",
        )

    fig.update_layout(
        title=f"Top {int(n)} Authors by Book Count",
        template="plotly_white",
        xaxis=dict(title=None, tickangle=-45),
        yaxis_title="Number of Books",
        margin=dict(l=20, r=20, t=50, b=100),
    )
    return fig


# --------------------------------
# Top Genres
# --------------------------------
@app.callback(
    Output("top-genres-graph", "figure"),
    Input("top-genres-slider", "value"),
)
def build_top_genres(n):
    genre_df = books_df.explode("genres", ignore_index=True).rename(
        columns={"genres": "genre"}
    )
    genre_stats = (
        genre_df.groupby("genre")["featured_rating"]
        .count()
        .reset_index(name="book_count")
        .sort_values("book_count", ascending=False)
        .head(int(n))
    )

    fig = go.Figure()
    fig.add_bar(
        x=genre_stats["genre"],
        y=genre_stats["book_count"],
        marker_color="steelblue",
        showlegend=False,
    )

    for _, row in genre_stats.iterrows():
        fig.add_annotation(
            x=row["genre"],
            y=row["book_count"] + 0.5,
            text=str(int(row["book_count"])),
            showarrow=False,
            font=dict(size=10, color="steelblue"),
            yanchor="bottom",
        )

    fig.update_layout(
        title=f"Top {int(n)} Genres by Book Count",
        template="plotly_white",
        xaxis=dict(title=None, tickangle=-45),
        yaxis_title="Number of Books",
        margin=dict(l=20, r=20, t=50, b=100),
    )
    return fig


# --- Top Books by Rating ---
@app.callback(
    Output("top-books-rating-graph", "figure"),
    Input("top-books-rating-slider", "value"),
)
def top_books_by_rating(n):
    n = int(n or 0)
    df = (
        books_df[["title", "rating"]]
        .dropna(subset=["title", "rating"])
        .sort_values("rating", ascending=False)
        .head(n)
    )
    fig = px.bar(
        df,
        x="rating",
        y="title",
        orientation="h",
        text="title",  # <- put title text directly on bars
        title=f"Top {n} Books by Rating",
        template="plotly_white",
    )
    fig.update_traces(
        textposition="inside",
        insidetextanchor="start",
        textfont=dict(size=10, color="white"),
    )
    # highest at top
    fig.update_layout(
        yaxis=dict(showticklabels=False),  # hide redundant labels
        xaxis=dict(title="Rating", range=[0, 5]),
    )
    fig.update_yaxes(autorange="reversed")
    return fig


# --- Top Books by Featured Rating ---
@app.callback(
    Output("top-books-featured-graph", "figure"),
    Input("top-books-featured-slider", "value"),
)
def top_books_by_featured(n):
    n = int(n or 0)
    df = (
        books_df[["title", "featured_rating"]]
        .dropna(subset=["title", "featured_rating"])
        .sort_values("featured_rating", ascending=False)
        .head(n)
    )
    fig = px.bar(
        df,
        x="featured_rating",
        y="title",
        orientation="h",
        title=f"Top {n} Books by Featured Rating",
        template="plotly_white",
    )
    fig.update_layout(
        xaxis=dict(title="Rating", range=[0, 5]),
        yaxis=dict(title="Book Title"),
        margin=dict(l=20, r=20, t=50, b=40),
        showlegend=False,
    )
    fig.update_yaxes(autorange="reversed")
    return fig


# --- Top Books by Sentiment Score ---
@app.callback(
    Output("top-books-sentiment-graph", "figure"),
    Input("top-books-sentiment-slider", "value"),
)
def top_books_by_sentiment(n):
    n = int(n or 0)
    col = "sentiment_score"  # adjust if your column is named differently
    if col not in books_df.columns:
        # empty placeholder if sentiment not available
        return px.bar(title="Top Books by Sentiment Score", template="plotly_white")

    df = (
        books_df[["title", col]]
        .dropna(subset=["title", col])
        .sort_values(col, ascending=False)
        .head(n)
    )
    fig = px.bar(
        df,
        x=col,
        y="title",
        orientation="h",
        title=f"Top {n} Books by Sentiment Score",
        template="plotly_white",
        labels={col: "Sentiment Score", "title": "Book Title"},
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=40),
        showlegend=False,
    )
    fig.update_yaxes(autorange="reversed")
    return fig


# List (Top 50)
@app.callback(
    Output("top50-rating-list", "children"),
    Input("init-once", "n_intervals"),
)
def build_top50_list(_):
    df = (
        books_df[["title", "rating"]]
        .dropna(subset=["title", "rating"])
        .sort_values("rating", ascending=False)
        .head(50)
    )

    items = []
    for _, row in df.iterrows():
        items.append(
            dbc.ListGroupItem(
                [
                    html.Span(row["title"], className="me-2"),
                    dbc.Badge(
                        f"{row['rating']:.2f}", color="primary", className="ms-auto"
                    ),
                ],
                className="d-flex justify-content-between align-items-center",
            )
        )
    return items


# Graph (Top 10)
@app.callback(
    Output("top10-rating-graph", "figure"),
    Input("init-once", "n_intervals"),
)
def build_top10_graph(_):
    df = (
        books_df[["title", "rating"]]
        .dropna(subset=["title", "rating"])
        .sort_values("rating", ascending=False)
        .head(10)
    )

    fig = px.bar(
        df,
        x="rating",
        y="title",
        orientation="h",
        title="Top 10 Books by Rating",
        template="plotly_white",
        text="rating",
    )
    fig.update_traces(
        texttemplate="%{text:.2f}", textposition="outside", marker_color="steelblue"
    )
    fig.update_layout(
        xaxis=dict(title="Rating", range=[0, 5]),
        yaxis=dict(title=None),
        margin=dict(l=20, r=20, t=50, b=40),
        showlegend=False,
    )
    # Highest at top
    fig.update_yaxes(autorange="reversed")
    return fig


# ---------- Featured Rating: Top 50 list ----------
@app.callback(
    Output("top50-featured-list", "children"),
    Input("init-once", "n_intervals"),
)
def build_top50_featured_list(_):
    if "featured_rating" not in books_df.columns:
        return [dbc.ListGroupItem("featured_rating column not found")]
    df = (
        books_df[["title", "featured_rating"]]
        .dropna(subset=["title", "featured_rating"])
        .sort_values("featured_rating", ascending=False)
        .head(50)
    )
    return [
        dbc.ListGroupItem(
            [
                html.Span(row.title, className="me-2"),
                dbc.Badge(
                    f"{row.featured_rating:.2f}", color="primary", className="ms-auto"
                ),
            ],
            className="d-flex justify-content-between align-items-center",
        )
        for _, row in df.iterrows()
    ]


# ---------- Featured Rating: Top 10 graph ----------
@app.callback(
    Output("top10-featured-graph", "figure"),
    Input("init-once", "n_intervals"),
)
def build_top10_featured_graph(_):
    if "featured_rating" not in books_df.columns:
        return px.bar(title="Top 10 Books by Featured Rating", template="plotly_white")
    df = (
        books_df[["title", "featured_rating"]]
        .dropna(subset=["title", "featured_rating"])
        .sort_values("featured_rating", ascending=False)
        .head(10)
    )
    fig = px.bar(
        df,
        x="featured_rating",
        y="title",
        orientation="h",
        title="Top 10 Books by Featured Rating",
        template="plotly_white",
        text="featured_rating",
    )
    fig.update_traces(
        texttemplate="%{text:.2f}", textposition="outside", marker_color="steelblue"
    )
    fig.update_layout(
        xaxis=dict(title="Featured Rating", range=[0, 5]),
        yaxis=dict(title=None),
        margin=dict(l=20, r=20, t=50, b=40),
        showlegend=False,
    )
    fig.update_yaxes(autorange="reversed")
    return fig


# ---------- Sentiment Score: Top 50 list ----------
@app.callback(
    Output("top50-sentiment-list", "children"),
    Input("init-once", "n_intervals"),
)
def build_top50_sentiment_list(_):
    col = "sentiment_score"
    if col not in books_df.columns:
        return [dbc.ListGroupItem("sentiment_score column not found")]
    df = (
        books_df[["title", col]]
        .dropna(subset=["title", col])
        .sort_values(col, ascending=False)
        .head(50)
    )
    return [
        dbc.ListGroupItem(
            [
                html.Span(row.title, className="me-2"),
                dbc.Badge(
                    f"{getattr(row, col):.2f}", color="primary", className="ms-auto"
                ),
            ],
            className="d-flex justify-content-between align-items-center",
        )
        for _, row in df.iterrows()
    ]


# ---------- Sentiment Score: Top 10 graph ----------
@app.callback(
    Output("top10-sentiment-graph", "figure"),
    Input("init-once", "n_intervals"),
)
def build_top10_sentiment_graph(_):
    col = "sentiment_score"
    if col not in books_df.columns:
        return px.bar(title="Top 10 Books by Sentiment Score", template="plotly_white")
    df = (
        books_df[["title", col]]
        .dropna(subset=["title", col])
        .sort_values(col, ascending=False)
        .head(10)
    )
    fig = px.bar(
        df,
        x=col,
        y="title",
        orientation="h",
        title="Top 10 Books by Sentiment Score",
        template="plotly_white",
        text=col,
        labels={col: "Sentiment Score", "title": "Book Title"},
    )
    fig.update_traces(
        texttemplate="%{text:.2f}", textposition="outside", marker_color="steelblue"
    )
    # Choose an axis range that fits your scoring scale
    smin, smax = float(df[col].min()), float(df[col].max())
    if 0.0 <= smin and smax <= 1.0:
        x_range = [0, 1]
    elif -1.0 <= smin and smax <= 1.0:
        x_range = [-1, 1]
    else:
        x_range = None
    fig.update_layout(
        xaxis=dict(title="Sentiment Score", range=x_range),
        yaxis=dict(title=None),
        margin=dict(l=20, r=20, t=50, b=40),
        showlegend=False,
    )
    fig.update_yaxes(autorange="reversed")
    return fig
