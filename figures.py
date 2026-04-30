import numpy as np
import plotly.graph_objects as go


def make_reviews_counts_fig(books_df):
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

    # scatter traces so reference lines appear in the legend
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
            name="Y = 100",
        )
    )

    fig.update_layout(
        title="Books Sorted by Review Count",
        template="plotly_white",
        xaxis=dict(title=None, showticklabels=False),
        yaxis_title="Review Count",
        margin=dict(l=20, r=20, t=40, b=60),
        legend=dict(orientation="v", yanchor="middle", y=0.7, xanchor="left", x=0.01),
    )
    return fig


def make_top_authors_fig(books_df, n):
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
        showlegend=False,
    )
    return fig


def make_top_genres_fig(books_df, n):
    genre_df = books_df.explode("genres", ignore_index=True).rename(
        columns={"genres": "genre"}
    )
    genre_df = genre_df.dropna(subset=["genre"])
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
        showlegend=False,
    )
    return fig
