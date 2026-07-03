from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "olist" / "brazilian-ecommerce"
DB_PATH = ROOT / "data" / "processed" / "olist.duckdb"


def load_csv_table(con: duckdb.DuckDBPyConnection, table_name: str, file_name: str) -> None:
    csv_path = RAW_DIR / file_name
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {csv_path}")

    con.execute(
        f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_path}', all_varchar=TRUE);"
    )
    print(f"Tabela carregada: {table_name}")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(DB_PATH))

    tables = [
        ("customers", "olist_customers_dataset.csv"),
        ("orders", "olist_orders_dataset.csv"),
        ("order_items", "olist_order_items_dataset.csv"),
        ("payments", "olist_order_payments_dataset.csv"),
        ("reviews", "olist_order_reviews_dataset.csv"),
        ("products", "olist_products_dataset.csv"),
        ("sellers", "olist_sellers_dataset.csv"),
    ]

    for table_name, file_name in tables:
        load_csv_table(con, table_name, file_name)

    print(f"Banco DuckDB criado em: {DB_PATH}")


if __name__ == "__main__":
    main()
