from pathlib import Path
import duckdb

DB = Path('data/processed/olist.duckdb')
con = duckdb.connect(str(DB))

print('DB exists:', DB.exists())
print('Tables:', con.execute('SHOW TABLES').fetchall())

print('\nSample from orders:')
print(con.execute('SELECT order_id, order_status, order_purchase_timestamp, order_estimated_delivery_date, order_delivered_customer_date FROM orders LIMIT 5').fetchdf())

print('\nCount orders:')
print(con.execute('SELECT COUNT(*) FROM orders').fetchone())

con.close()
