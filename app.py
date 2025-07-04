import streamlit as st
import pandas as pd
import duckdb
import io
csv ='''
beverage, price
coffee, 1.50
tea, 1.00
water, 0.75
'''

beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item, price
cookie, 1.00
chocolatine, 1.50
muffin, 2.00
'''
food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""


solution = duckdb.sql(answer).df()

st.header("enter your query")
query = st.text_area(label="votre_code_sql", key="query", height=200)
if query:
    try:
        result = duckdb.sql(query).df()
        st.write(result)
    except Exception as e:
        st.error(f"Erreur: {e}")

tab2, tab3 = st.tabs(["tables", "solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected result")
    st.dataframe(solution)


with tab3:
    st.write(answer)
