from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "processed" / "game_analytics.db"
SQL_DIR = ROOT / "sql"
OUTPUT_DIR = ROOT / "data" / "processed" / "sql_results"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

with sqlite3.connect(DB) as conn:
    for sql_file in sorted(SQL_DIR.glob("*.sql")):
        query = sql_file.read_text(encoding="utf-8")
        result = pd.read_sql_query(query, conn)

        output_file = OUTPUT_DIR / f"{sql_file.stem}.csv"
        result.to_csv(output_file, index=False)

        print(f"\n{sql_file.name}")
        print(result.head(10).to_string(index=False))
        print(f"Saved: {output_file}")