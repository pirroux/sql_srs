# pylint: disable = missing-module-docstring

import ast
import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# solution = duckdb.sql(ANSWER).df()

with st.sidebar:
    theme = st.selectbox(
        "what would you like to work on",
        ("cross_joins", "group_by", "window_functions"),
        placeholder="Select a theme..."
    )
    st.write("You chose:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ").df()
    st.write(exercise)
    
st.header("enter your query")
query = st.text_area(label="votre_code_sql", key="query", height=200)

if query:
    results = con.execute(query).df()
    st.dataframe(results)
#     results = duckdb.sql(query).df()
#     st.dataframe(results)

#     results = duckdb.sql(query).df()
#     st.dataframe(results)

#     try:
#         results = results[solution.columns]
#         st.dataframe(results.compare(solution))
#     except KeyError as e:
#         st.write("columns not in the same ORDER or are not the same as solution")
#         # st.write("somethihng is odd")

#         # if len(results.columns) != len(solution.columns):
#         #     st.write("nombre de colomnes différentes")

#         # n_lines_diff = results.shape[0] - solution.shape[0]
#         # if n_lines_diff != 0:
#         #     st.write(" not the same lenght nigga")

#         # if query:
#         #     try:
#         #         result = duckdb.sql(query).df()
#         #         st.write(result)
#         #     except Exception as e:
#         #         st.error(f"Erreur: {e}")
#         results = results[solution.columns]
#         st.dataframe(results.compare(solution))
#     except KeyError as e:
#         st.write("columns not in the same ORDER or are not the same as solution")
#         # st.write("somethihng is odd")

#     # if len(results.columns) != len(solution.columns):
#     #     st.write("nombre de colomnes différentes")

#     # n_lines_diff = results.shape[0] - solution.shape[0]
#     # if n_lines_diff != 0:
#     #     st.write(" not the same lenght nigga")


# # if query:
# #     try:
# #         result = duckdb.sql(query).df()
# #         st.write(result)
# #     except Exception as e:
# #         st.error(f"Erreur: {e}")

tab2, tab3 = st.tabs(["tables", "solution"])

with tab2:  
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:    
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}")
        st.dataframe(df_table)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected result")
#     st.dataframe(solution)


# with tab3:
#     st.write(ANSWER)
