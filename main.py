from pathlib import Path

from data_analytics import generate_analytics
from data_cleaning import clean_data
from data_visualization import create_charts
from database_connection import create_database_engine
from import_data import import_data, load_data


PROJECT_DIR = Path(__file__).resolve().parent
CSV_PATH = PROJECT_DIR / "TN_Electronics_Sales_Analytics.csv"
OUTPUT_DIR = PROJECT_DIR / "reports"


def main() -> None:
    raw_data = load_data(CSV_PATH)
    cleaned_data = clean_data(raw_data)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_csv = OUTPUT_DIR / "tn_electronics_sales_analytics_cleaned.csv"
    cleaned_excel = OUTPUT_DIR / "tn_electronics_sales_analytics_cleaned.xlsx"
    cleaned_data.to_csv(cleaned_csv, index=False, encoding="utf-8-sig")
    cleaned_data.to_excel(cleaned_excel, index=False)

    generate_analytics(cleaned_data, OUTPUT_DIR)
    charts = create_charts(cleaned_data, OUTPUT_DIR)

    engine = create_database_engine()
    try:
        with engine.connect():
            imported_rows = import_data(cleaned_data, engine)
    finally:
        engine.dispose()

    print(f"\nImported {imported_rows} rows into MySQL.")
    print(f"Cleaned CSV: {cleaned_csv}")
    print(f"Cleaned Excel: {cleaned_excel}")
    print(f"Reports and charts: {OUTPUT_DIR}")
    print(f"Charts: {', '.join(path.name for path in charts)}")


if __name__ == "__main__":
    main()