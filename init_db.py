# pylint: disable = missing-module-docstring

import io

import duckdb
import pandas as pd

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# --------------------------
# EXERCISES LIST
# --------------------------

data = {
    "theme": ["cross_joins", "cross_joins"],
    "exercise_name": ["beverages_and_food", "sizes_and_trademarks"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
    "last_reviewed": ["1980-01-01", "1970-01-01"],
}

memory_state_df = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state as SELECT * FROM memory_state_df")

# --------------------------
# CROSS JOIN EXERCISES
# --------------------------

CSV = """
beverage, price
orange juice, 2.5
Expresso, 2
Tea, 3
"""
beverages = pd.read_csv(io.StringIO(CSV))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

CSV2 = """
food_item, price
cookie juice, 1.00
chocolatine, 2
muffin, 3 .00
"""
food_items = pd.read_csv(io.StringIO(CSV2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")

SIZES = """
size
XS
M
L
XL
"""

SIZES = pd.read_csv(io.StringIO(SIZES))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

TRADEMARKS = """
TRADEMARKS
Nike
Asphalte
Abercrombie
Lewis
"""

TRADEMARKS = pd.read_csv(io.StringIO(TRADEMARKS))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

con.close()
