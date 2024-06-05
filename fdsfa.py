import pandas as pd
import sqlite3

conn = sqlite3.connect('property_krakow.db', isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
db_df = pd.read_sql_query("SELECT * FROM warszawa", conn)
db_df.to_csv('warszawa.csv', index=False, encoding='utf-8')

