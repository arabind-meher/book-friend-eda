import pandas as pd
from .connection import get_engine
from .utils import uuid_to_str


class Database:
    def __init__(self):
        self.engine = get_engine()

    def get_table(self, table_name: str, schema: str = "library") -> pd.DataFrame:
        query = f'SELECT * FROM "{schema}"."{table_name}";'
        df = pd.read_sql(query, self.engine)
        return uuid_to_str(df)

    def get_books(self) -> pd.DataFrame:
        # Fetch raw tables
        books = self.get_table("books")
        genres = self.get_table("genres")
        book_genres = self.get_table("book_genres")
        media_types = self.get_table("media_types")
        book_media_types = self.get_table("book_media_types")

        # Join book_genres -> genres
        bg = (
            book_genres.merge(genres, left_on="genre_id", right_on="id", how="left")
            .groupby("book_id")["name"]
            .apply(list)
            .reset_index(name="genres")
        )

        # Join book_media_types -> media_types
        bm = (
            book_media_types.merge(
                media_types, left_on="media_type_id", right_on="id", how="left"
            )
            .groupby("book_id")["name"]
            .apply(list)
            .reset_index(name="media_types")
        )

        # Merge into books
        df = books.merge(bg, left_on="id", right_on="book_id", how="left").merge(
            bm, left_on="id", right_on="book_id", how="left"
        )

        # Clean up extra join columns
        df = df.drop(columns=["book_id_x", "book_id_y"], errors="ignore")

        return df

    def get_recommendations(self) -> pd.DataFrame:
        return self.get_table("book_recs")
