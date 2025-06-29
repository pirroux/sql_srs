import streamlit as st
import pandas as pd
import duckdb

st.write("Hello World how are you ?")
data = { "a": [1,2,3], "b": [4,5,6]}
df = pd.DataFrame(data)

tab1, tab2 , tab3 = st.tabs(["tab1", "tab2", "tab3"])

with st.sidebar:

    if option == "Joins":
        st.write("You selected Joins")

with tab1:
    duckdb.register("df", df)
    option = st.selectbox(
        "What would you like to work on",
        ("Joins", "GROUPBY", "Window Functions"), index=None,
        placeholder="select a topic..."
    )
    if option == "Joins":
        st.write("You selected Joins")
    sql_query = st.text_area(label="entrez votre input")
    result = duckdb.sql(sql_query).df()
    st.write(f"vous avez entré la query suivante: {sql_query}")
    st.dataframe(result)
