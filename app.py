# pylint: disable = missing-module-docstring

import ast
import io
import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# solution = duckdb.sql(ANSWER).df()

with st.sidebar:
    theme = st.selectbox(
        "what would you like to work on",
        ("cross_joins", "group_by", "window_functions"),
        placeholder="Select a theme...",
    )
    st.write("You chose:", theme)
    
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ").df()
    st.write(exercise)
    
st.header("enter your query")
query = st.text_area(label="votre_code_sql", key="query", height=200)

if query:
    results = con.execute(query).df()
    st.dataframe(results)