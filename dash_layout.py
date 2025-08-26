from dash import html, dcc
import dash_bootstrap_components as dbc

# Your mapping
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
    ]
}

navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand(
            [
                html.H2("Book Friend EDA", className="mb-0 fw-bold"),
            ],
            className="me-auto text-light"
        ),
        html.Span("Exploratory Dashboard", className="text-secondary fs-5"),
    ]),
    color="dark",
    dark=True,
    className="mb-4"
)

review_count_row = [
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Reviews Counts", className="card-title text-center"),
                    dcc.Graph(
                        id="reviews-count-graph",
                        config={"displayModeBar": False}
                    )
                ])
            ),
            width=12
        )
    ], className="mb-3"),

    dcc.Interval(id="init-once", interval=0, n_intervals=0, max_intervals=1),
]

author_genre_row = [
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top Authors by Count", className="card-title"),
                    dcc.Slider(
                        id="top-authors-slider",
                        min=1,
                        max=50,
                        step=1,
                        value=10,
                        marks={i: str(i) for i in range(0, 51, 5)},
                    ),
                    dcc.Graph(id="top-authors-graph", config={"displayModeBar": False}),
                ])
            ),
            width=6
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top Genres by Count", className="card-title"),
                    dcc.Slider(
                        id="top-genres-slider",
                        min=1,
                        max=20,
                        step=1,
                        value=10,
                        marks={i: str(i) for i in range(0, 21, 2)},
                    ),
                    dcc.Graph(id="top-genres-graph", config={"displayModeBar": False}),
                ])
            ),
            width=6
        ),
    ], className="mb-3"),
]

rating_sentiment_row = [
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top Books by Rating", className="card-title"),
                    dcc.Slider(
                        id="top-books-rating-slider",
                        min=0, max=50, step=1, value=10,
                        marks={i: str(i) for i in [0, 10, 20, 30, 40, 50]},
                        tooltip={"always_visible": True}
                    ),
                    dcc.Graph(id="top-books-rating-graph", config={"displayModeBar": False}),
                ])
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top Books by Featured Rating", className="card-title"),
                    dcc.Slider(
                        id="top-books-featured-slider",
                        min=0, max=50, step=1, value=10,
                        marks={i: str(i) for i in [0, 10, 20, 30, 40, 50]},
                        tooltip={"always_visible": True}
                    ),
                    dcc.Graph(id="top-books-featured-graph", config={"displayModeBar": False}),
                ])
            ),
            width=4
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top Books by Sentiment Score", className="card-title"),
                    dcc.Slider(
                        id="top-books-sentiment-slider",
                        min=0, max=50, step=1, value=10,
                        marks={i: str(i) for i in [0, 10, 20, 30, 40, 50]},
                        tooltip={"always_visible": True}
                    ),
                    dcc.Graph(id="top-books-sentiment-graph", config={"displayModeBar": False}),
                ])
            ),
            width=4
        ),
    ], className="mb-3"),
]

rating_row = [
    dbc.Row([
        # Left: Top 50 list (scrollable)
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top 50 Books by Rating", className="card-title"),
                    html.Div(
                        dbc.ListGroup(id="top50-rating-list", flush=True),
                        style={"maxHeight": "58vh", "overflowY": "auto"}  # scroll inside
                    ),
                ]),
                style={"height": "70vh"}  # fixed height
            ),
            width=5
        ),

        # Right: Top 10 graph
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top 10 Books by Rating", className="card-title"),
                    dcc.Graph(id="top10-rating-graph", config={"displayModeBar": False},
                              style={"height": "60vh"})  # fill available height inside card
                ]),
                style={"height": "70vh"}  # fixed height
            ),
            width=7
        ),
    ], className="mb-3"),
]

featured_rating_row = [
    dbc.Row([
        # Left: Top 50 list
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top 50 Books by Featured Rating", className="card-title"),
                    html.Div(
                        dbc.ListGroup(id="top50-featured-list", flush=True),
                        style={"maxHeight": "58vh", "overflowY": "auto"}
                    ),
                ]),
                style={"height": "70vh"}
            ),
            width=5
        ),

        # Right: Top 10 graph
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top 10 Books by Featured Rating", className="card-title"),
                    dcc.Graph(id="top10-featured-graph", config={"displayModeBar": False},
                              style={"height": "60vh"})
                ]),
                style={"height": "70vh"}
            ),
            width=7
        ),
    ], className="mb-3"),
]

sentiment_score_row = [
    dbc.Row([
        # Left: Top 50 list
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top 50 Books by Sentiment Score", className="card-title"),
                    html.Div(
                        dbc.ListGroup(id="top50-sentiment-list", flush=True),
                        style={"maxHeight": "58vh", "overflowY": "auto"}
                    ),
                ]),
                style={"height": "70vh"}
            ),
            width=5
        ),

        # Right: Top 10 graph
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Top 10 Books by Sentiment Score", className="card-title"),
                    dcc.Graph(id="top10-sentiment-graph", config={"displayModeBar": False},
                              style={"height": "60vh"})
                ]),
                style={"height": "70vh"}
            ),
            width=7
        ),
    ], className="mb-3"),
]

distribution_row = [
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Distribution of Rating"),
                        dbc.CardBody(
                            dcc.Graph(
                                id="rating-dist-hist",
                                config={"displayModeBar": False},
                                style={"height": 300}
                            )
                        ),
                    ],
                    className="h-100",
                ),
                width=4,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Distribution of Featured Rating"),
                        dbc.CardBody(
                            dcc.Graph(
                                id="featured-rating-dist-hist",
                                config={"displayModeBar": False},
                                style={"height": 300}
                            )
                        ),
                    ],
                    className="h-100",
                ),
                width=4,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Distribution of Sentiment Score"),
                        dbc.CardBody(
                            dcc.Graph(
                                id="sentiment-dist-hist",
                                config={"displayModeBar": False},
                                style={"height": 300}
                            )
                        ),
                    ],
                    className="h-100",
                ),
                width=4,
            ),
        ],
        className="mb-3",
    )
]

# -------------------------
# Controls (row-level)
# -------------------------
controls = [
    dbc.Card(
        [
            dbc.CardHeader("Compare Any Two Metrics"),
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("X-axis metric", className="form-label"),
                                dcc.Dropdown(
                                    id="metric-x",
                                    options=[
                                        {"label": "rating", "value": "rating"},
                                        {"label": "featured_rating", "value": "featured_rating"},
                                        {"label": "sentiment_score", "value": "sentiment_score"},
                                    ],
                                    value="rating",
                                    clearable=False,
                                ),
                            ],
                            md=6,
                        ),
                        dbc.Col(
                            [
                                html.Label("Y-axis metric", className="form-label"),
                                dcc.Dropdown(
                                    id="metric-y",
                                    options=[
                                        {"label": "rating", "value": "rating"},
                                        {"label": "featured_rating", "value": "featured_rating"},
                                        {"label": "sentiment_score", "value": "sentiment_score"},
                                    ],
                                    value="featured_rating",
                                    clearable=False,
                                ),
                            ],
                            md=6,
                        ),
                    ],
                    className="g-3",
                )
            ),
        ],
        className="mb-3",
    )
]

# -------------------------
# Row of two analysis cards
# -------------------------
compare_row = [
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Y − X Across All Books"),
                        dbc.CardBody(
                            dcc.Graph(
                                id="diff-bar",
                                config={"displayModeBar": False},
                                style={"height": 350},
                            )
                        ),
                    ],
                    className="h-100",
                ),
                width=6,
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Y vs X Scatter"),
                        dbc.CardBody(
                            dcc.Graph(
                                id="xy-scatter",
                                config={"displayModeBar": False},
                                style={"height": 350},
                            )
                        ),
                    ],
                    className="h-100",
                ),
                width=6,
            ),
        ],
        className="mb-3",
    )
]

##### top

top_metrics_row = dbc.Row(
    [
        # Left: Top 50 list
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Row(
                            [
                                dbc.Col(html.H5(id="top50-title", className="mb-0")),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="metric-select",
                                        options=[
                                            {"label": "rating", "value": "rating"},
                                            {"label": "featured_rating", "value": "featured_rating"},
                                            {"label": "sentiment_score", "value": "sentiment_score"},
                                        ],
                                        value="rating",
                                        clearable=False,
                                        style={"fontSize": "14px"},
                                    ),
                                    width=6,
                                ),
                            ],
                            align="center",
                        )
                    ),
                    dbc.CardBody(
                        html.Div(
                            dbc.ListGroup(id="top50-generic-list", flush=True),
                            style={"maxHeight": "58vh", "overflowY": "auto"},
                        )
                    ),
                ],
                style={"height": "70vh"},
            ),
            width=5,
        ),

        # Right: Top 10 graph
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(html.H5(id="top10-title", className="mb-0")),
                    dbc.CardBody(
                        dcc.Graph(
                            id="top10-generic-graph",
                            config={"displayModeBar": False},
                            style={"height": "60vh"},
                        )
                    ),
                ],
                style={"height": "70vh"},
            ),
            width=7,
        ),
    ],
    className="mb-4",  # margin before next row
)

# -------------------------
# Layout: Series Analysis row
# -------------------------
series_row = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader(
                        dbc.Row(
                            [
                                dbc.Col(html.H5("Series Analysis", className="mb-0"), md=8),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id="series-select",
                                        options=[{"label": k, "value": k} for k in series.keys()],
                                        value="Harry Potter",
                                        clearable=False,
                                    ),
                                    md=4,
                                ),
                            ],
                            align="center",
                        )
                    ),
                    dbc.CardBody(
                        dcc.Graph(
                            id="series-trend-graph",
                            config={"displayModeBar": False},
                            style={"height": "60vh"},
                        )
                    ),
                ]
            ),
            width=12,
        )
    ],
    className="mb-4",  # margin before next row
)
