from pathlib import Path
import sqlite3

import pandas as pd


NUMERIC_COLUMNS = ["age", "price", "quantity"]


def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [c.strip().lower() for c in cleaned.columns]

    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned["purchase_date"] = pd.to_datetime(cleaned["purchase_date"], errors="coerce")
    cleaned = cleaned.dropna(subset=["customer_id", "category", "price", "quantity", "purchase_date"])
    cleaned = cleaned.drop_duplicates()

    cleaned["quantity"] = cleaned["quantity"].clip(lower=1)
    cleaned["price"] = cleaned["price"].clip(lower=0)
    cleaned["total_amount"] = cleaned["price"] * cleaned["quantity"]

    return cleaned


def build_eda_summary(df: pd.DataFrame) -> dict:
    category_revenue = (
        df.groupby("category", as_index=False)["total_amount"].sum().sort_values("total_amount", ascending=False)
    )
    return {
        "rows": int(len(df)),
        "unique_customers": int(df["customer_id"].nunique()),
        "total_revenue": float(df["total_amount"].sum()),
        "avg_order_value": float(df["total_amount"].mean()) if len(df) else 0.0,
        "top_category_by_revenue": category_revenue.iloc[0]["category"] if len(category_revenue) else None,
    }


def write_sqlite(df: pd.DataFrame, db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        df.to_sql("transactions", connection, if_exists="replace", index=False)


def run_business_queries(db_path: Path) -> dict[str, pd.DataFrame]:
    queries = {
        "monthly_sales": """
            SELECT strftime('%Y-%m', purchase_date) AS month,
                   ROUND(SUM(total_amount), 2) AS revenue,
                   COUNT(*) AS orders
            FROM transactions
            GROUP BY month
            ORDER BY month
        """,
        "category_performance": """
            SELECT category,
                   ROUND(SUM(total_amount), 2) AS revenue,
                   ROUND(AVG(total_amount), 2) AS avg_order_value,
                   COUNT(*) AS orders
            FROM transactions
            GROUP BY category
            ORDER BY revenue DESC
        """,
        "top_customers": """
            SELECT customer_id,
                   city,
                   ROUND(SUM(total_amount), 2) AS lifetime_value,
                   COUNT(*) AS order_count
            FROM transactions
            GROUP BY customer_id, city
            ORDER BY lifetime_value DESC
            LIMIT 5
        """,
    }

    with sqlite3.connect(db_path) as connection:
        return {name: pd.read_sql_query(query, connection) for name, query in queries.items()}


def run_pipeline(raw_path: Path, processed_path: Path, db_path: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    raw = load_data(raw_path)
    cleaned = clean_data(raw)
    cleaned.to_csv(processed_path, index=False)

    write_sqlite(cleaned, db_path)
    query_results = run_business_queries(db_path)
    for name, frame in query_results.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)

    return build_eda_summary(cleaned)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    summary = run_pipeline(
        raw_path=root / "data" / "raw" / "retail_customer_behavior.csv",
        processed_path=root / "data" / "processed" / "retail_customer_behavior_cleaned.csv",
        db_path=root / "outputs" / "retail_analytics.db",
        output_dir=root / "outputs",
    )
    print(summary)
