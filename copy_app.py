import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from db import Database

# -------------------------
# Load data once at startup
# -------------------------
db = Database()
books_df = db.get_books()
recs_df = db.get_recommendations()

num_authors = books_df["author"].nunique()
num_genres = books_df['genres'].explode().nunique()

# -------------------------
# Dash app (with Bootstrap theme)
# -------------------------
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)

# -------------------------
# Layout
# -------------------------
app.layout = html.Div(
    [
        # Full-width navbar
        dbc.NavbarSimple(
            brand=html.H3("Book Friend Dashboard", className="mb-0"),
            color="primary",
            dark=True,
            className="mb-4",
        ),

        # Main content
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5("Authors", className="text-center"),
                                dcc.Slider(
                                    id="author-count",
                                    min=1,
                                    max=max(1, int(num_authors)),
                                    value=min(10, int(num_authors)) if num_authors else 1,
                                    marks={i: str(i) for i in range(1, num_authors + 1, 10)},
                                    step=1,
                                ),
                                html.H5("Authors", className="text-center mt-1"),
                                dcc.Graph(
                                    id="author-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "420px"},
                                ),
                            ],
                            md=6,
                        ),
                        dbc.Col(
                            [
                                html.H5("Genres", className="text-center"),
                                dcc.Slider(
                                    id="genre-count",
                                    min=1,
                                    max=max(1, int(num_genres)),
                                    value=min(10, int(num_genres)) if num_genres else 1,
                                    marks={i: str(i) for i in range(1, num_genres + 1, 10)},
                                    step=1,
                                ),
                                dcc.Graph(
                                    id="genre-graph",
                                    config={"displayModeBar": False},
                                    style={"height": "420px"},
                                ),
                            ],
                            md=6,
                        ),
                    ],
                    className="g-3",
                ),
            ],
            fluid=True,
        ),
    ]
)


# -------------------------
# Callback
# -------------------------

# --- authors ---
@app.callback(
    Output("author-graph", "figure"),
    Input("author-count", "value"),
)
def update_author_graph(top_n):
    top = books_df['author'].value_counts().head(int(top_n or 10)).reset_index()
    top.columns = ["author", "count"]

    if top.empty:
        return px.bar()

    fig = px.bar(top, x="author", y="count", text="count")
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        height=420,
        yaxis=dict(range=[0, 10]),  # fixed ylim
    )
    return fig


# --- genres ---
@app.callback(
    Output("genre-graph", "figure"),
    Input("genre-count", "value"),
)
def update_genre_graph(top_n):
    top = books_df['genres'].explode().value_counts().head(int(top_n or 10)).reset_index()
    top.columns = ["genre", "count"]

    if top.empty:
        return px.bar()

    fig = px.bar(top, x="genre", y="count", text="count")
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(
        height=420,
        yaxis=dict(range=[0, 220]),  # fixed ylim
    )
    return fig


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)
