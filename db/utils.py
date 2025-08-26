import uuid
import pandas as pd


def uuid_to_str(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].map(lambda x: str(x) if isinstance(x, uuid.UUID) else x)
    return df
