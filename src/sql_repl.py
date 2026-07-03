import duckdb
from pathlib import Path
import pandas as pd

DB = Path('data/processed/olist.duckdb')

con = None

def _get_con():
    global con
    if con is None:
        con = duckdb.connect(str(DB))
    return con


def execute(sql: str):
    """Execute a SQL statement and return a pandas.DataFrame for SELECTs or the raw result otherwise."""
    c = _get_con()
    q = sql.strip()
    if q.lower().startswith('select') or 'return' in q.lower():
        return c.execute(q).fetchdf()
    else:
        return c.execute(q).fetchall()


def repl():
    print(f"Connected to: {DB} (exists={DB.exists()})")
    print("Enter SQL statements terminated with a semicolon ';'. Type 'exit' to quit.")
    buffer = []
    try:
        while True:
            line = input('sql> ')
            if not line:
                continue
            if line.strip().lower() in ('exit','quit'):
                break
            buffer.append(line)
            if line.strip().endswith(';'):
                stmt = '\n'.join(buffer).rstrip(';')
                buffer = []
                try:
                    res = execute(stmt)
                    if isinstance(res, pd.DataFrame):
                        print(res)
                    else:
                        print(res)
                except Exception as e:
                    print('Error:', e)
    except (KeyboardInterrupt, EOFError):
        print('\nExiting.')


if __name__ == '__main__':
    repl()
