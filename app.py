# pylint: disable = missing-module-docstring

import io

import duckdb
import pandas as pd
import streamlit as st
import duckdb
import pandas as pd
import streamlit as st

CSV = """
beverage, price
coffee, 1.50
tea, 1.00
water, 0.75
"""


beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item, price
cookie, 1.00
chocolatine, 1.50
muffin, 2.00
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER = """
SELECT * FROM beverages
CROSS JOIN food_items
"""


def my_func():
    print("hello")


solution = duckdb.sql(ANSWER).df()

with st.sidebar:
    st.title("what do you want to work on?")
    table = st.selectbox(
        label="tables", key="tables", options=["beverages", "food_items"]
    )
    table = st.selectbox(
        label="tables", key="tables", options=["beverages", "food_items"]
    )
    if table == "beverages":
        st.write(beverages)
    elif table == "food_items":
        st.write(food_items)
    else:
        st.write("no table selected")

st.header("enter your query")
query = st.text_area(label="votre_code_sql", key="query", height=200)


if query:
    results = duckdb.sql(query).df()
    st.dataframe(results)

    results = duckdb.sql(query).df()
    st.dataframe(results)

    try:
        results = results[solution.columns]
        st.dataframe(results.compare(solution))
    except KeyError as e:
        st.write("columns not in the same ORDER or are not the same as solution")
        # st.write("somethihng is odd")

    # if len(results.columns) != len(solution.columns):
    #     st.write("nombre de colomnes différentes")

    # n_lines_diff = results.shape[0] - solution.shape[0]
    # if n_lines_diff != 0:
    #     st.write(" not the same lenght nigga")


# if query:
#     try:
#         result = duckdb.sql(query).df()
#         st.write(result)
#     except Exception as e:
#         st.error(f"Erreur: {e}")
        results = results[solution.columns]
        st.dataframe(results.compare(solution))
    except KeyError as e:
        st.write("columns not in the same ORDER or are not the same as solution")
        # st.write("somethihng is odd")

    # if len(results.columns) != len(solution.columns):
    #     st.write("nombre de colomnes différentes")

    # n_lines_diff = results.shape[0] - solution.shape[0]
    # if n_lines_diff != 0:
    #     st.write(" not the same lenght nigga")


# if query:
#     try:
#         result = duckdb.sql(query).df()
#         st.write(result)
#     except Exception as e:
#         st.error(f"Erreur: {e}")

tab2, tab3 = st.tabs(["tables", "solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected result")
    st.dataframe(solution)


with tab3:
    st.write(ANSWER)
