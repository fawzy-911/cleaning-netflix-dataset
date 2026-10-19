"""Cleaning helpers for the Netflix titles dataset."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = {"show_id", "type", "title", "date_added", "release_year", "duration"}


def clean_netflix_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the Netflix titles DataFrame.

    Missing descriptive/category values remain represented as "Unknown". Rows
    without an identifier, title, or content type are removed because they
    cannot be reliably identified. Dates and numeric values that cannot be
    parsed are kept as missing instead of being guessed.
    """
    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        names = ", ".join(sorted(missing_columns))
        raise ValueError(f"Dataset is missing required columns: {names}")

    cleaned = data.copy()

    # Trim surrounding whitespace and treat empty/whitespace-only cells as null.
    for column in cleaned.select_dtypes(include=["object", "string"]).columns:
        cleaned[column] = cleaned[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
        cleaned[column] = cleaned[column].replace(r"^\s*$", pd.NA, regex=True)

    # A show_id identifies a record; keep the first occurrence of each ID.
    cleaned = cleaned.drop_duplicates(subset=["show_id"], keep="first")

    # These fields are needed to identify what the record describes.
    cleaned = cleaned.dropna(subset=["show_id", "type", "title"])

    # Preserve records while making unknown descriptive values explicit.
    for column in ("director", "cast", "country", "rating"):
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].fillna("Unknown")

    # Parse the source's month-name date format; invalid or absent values stay null.
    cleaned["date_added"] = pd.to_datetime(
        cleaned["date_added"], format="%B %d, %Y", errors="coerce"
    )
    cleaned["release_year"] = pd.to_numeric(
        cleaned["release_year"], errors="coerce"
    ).astype("Int64")

    # Movie runtimes and TV seasons share one source column; split value and unit.
    duration_text = cleaned.pop("duration").astype("string")
    duration_parts = duration_text.str.extract(
        r"(?i)^\s*(?P<duration_value>\d+)\s*(?P<duration_unit>min|season)s?\s*$"
    )
    cleaned["duration_value"] = pd.to_numeric(
        duration_parts["duration_value"], errors="coerce"
    ).astype("Int64")
    cleaned["duration_unit"] = duration_parts["duration_unit"].str.lower().astype("string")

    # Keep unexpected non-empty duration formats visible for later review.
    unmatched_duration = duration_text.notna() & duration_parts["duration_value"].isna()
    cleaned.loc[unmatched_duration, "duration_unit"] = "Unknown"

    return cleaned.reset_index(drop=True)

