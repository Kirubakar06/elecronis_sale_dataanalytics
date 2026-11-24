
from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Engine


TABLE_NAME = "tn_electronics_sales_analytics"


def load_data(csv_path: Path) -> pd.DataFrame:
    if not csv_path.is_file():
        raise FileNotFoundError(f"Sales CSV was not found: {csv_path}")

    data = pd.read_csv(
        csv_path,
        encoding="utf-8-sig",
        skip_blank_lines=True,
    )
    if data.empty:
        raise ValueError(f"Sales CSV contains no data rows: {csv_path}")
    return data


def import_data(data: pd.DataFrame, engine: Engine) -> int:
    data.to_sql(
        TABLE_NAME,
        engine,
        if_exists="replace",
        index=False,
        chunksize=500,
    )
    return len(data)
