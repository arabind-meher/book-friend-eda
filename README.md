# Book Friend EDA

An interactive exploratory data analysis dashboard for a book database. Built with Dash and Plotly, backed by a PostgreSQL database.

## Features

- **Reviews Analysis** — books ranked by review count with min/mean/median/max reference lines
- **Top Authors & Genres** — adjustable slider to explore the top N authors or genres by book count
- **Top Books by Metric** — ranked list (top 50) and bar chart (top 10) for rating, featured rating, or sentiment score
- **Distributions** — histograms of rating, featured rating, and sentiment score with statistical overlays
- **Metric Comparison** — select any two metrics to compare via a difference bar chart and scatter plot (RMSE, Pearson r)
- **Series Trend Analysis** — line chart tracking average scores across a book series over time

## Tech Stack

| Layer | Library |
|---|---|
| Dashboard | [Dash](https://dash.plotly.com/) + [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) |
| Charts | [Plotly](https://plotly.com/python/) |
| Data | [Pandas](https://pandas.pydata.org/) |
| Database | PostgreSQL via [SQLAlchemy](https://www.sqlalchemy.org/) + psycopg2 |
| Package manager | [uv](https://github.com/astral-sh/uv) |

## Prerequisites

- Python 3.12+
- PostgreSQL with a `library` schema containing the tables listed below
- [uv](https://github.com/astral-sh/uv) (or pip)

### Required database tables

```
library.books
library.genres
library.book_genres
library.media_types
library.book_media_types
library.book_recs
```

## Setup

1. Clone the repository and install dependencies:

```bash
uv sync
```

2. Create a `.env` file in the project root:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=library
```

3. Run the app:

```bash
uv run python app.py
```

The dashboard will be available at `http://127.0.0.1:8050`.

## Project Structure

```
book-friend-eda/
├── app.py            # Dash app, callbacks, and layout entry point
├── dash_layout.py    # UI component definitions
├── figures.py        # Reusable Plotly figure builders
├── db/
│   ├── connection.py # SQLAlchemy engine setup
│   ├── database.py   # Data fetching and join logic
│   └── utils.py      # UUID serialization helper
└── pyproject.toml
```
