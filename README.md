# Clean the Netflix Dataset

A small, reproducible data-cleaning project for the Kaggle [Netflix Movies and TV Shows dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows). The notebook inspects the data, documents column-level cleaning choices, handles missing values, fixes mixed types, parses dates, and exports a cleaned CSV.

## 1. Get the data

Download `netflix_titles.csv` from the [Kaggle dataset page](https://www.kaggle.com/datasets/shivamb/netflix-shows), then place it here:

```text
data/netflix_titles.csv
```

The source dataset is not included in this repository. Keep its original CSV unchanged so you can compare it with the cleaned output.

## 2. Install and run

Python 3.9 or newer is recommended.

```bash
python -m venv .venv
```

Activate the environment, then install the dependencies:

```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
jupyter notebook clean_netflix_dataset.ipynb
```

Run the notebook cells from top to bottom. It reads `data/netflix_titles.csv` and writes `data/cleaned_netflix_titles.csv`.

## Cleaning decisions

- Trim text and treat blank strings as missing values.
- Keep the first row for each `show_id`; remove records missing `show_id`, `title`, or `type` because those records cannot be identified reliably.
- Fill missing `director`, `cast`, `country`, and `rating` with `Unknown`. Keep missing dates and unparseable numbers empty instead of guessing them.
- Parse `date_added` as a date and `release_year` as a nullable integer.
- Split the mixed `duration` column into `duration_value` and `duration_unit` (`min` or `season`). Unexpected non-empty formats are marked `Unknown` for review.

## Project page

[roadmap.sh — Clean the Netflix Dataset](https://roadmap.sh/projects/cleaning-netflix-dataset)

