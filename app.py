# pylint: disable = missing-module-docstring
import logging
import os
import subprocess

import duckdb
import streamlit as st

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    # exec(open("init_db.py").read())
    subprocess.run(["python", "init_db.py"], check=True)

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "what would you like to work on",
        ("cross_joins", "group_by", "window_functions"),
        placeholder="Select a theme...",
    )
    st.write("You chose:", theme)

    exercise = (
        con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}' ")
        .df()
        .sort_values("last_reviewed")
        .reset_index()
    )
    st.write(exercise)

    # Getting the exercise solution
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        answer = f.read()
    solution_df = con.execute(answer).df()

st.header("enter your query")
query = st.text_area(label="votre_code_sql", key="query", height=200)

if query:
    results = con.execute(query).df()
    st.dataframe(results)

    # verifying the columns
    try:
        results = results[solution_df.columns]
        st.dataframe(results.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    # verifying the amount of lines
    n_lines_difference = results.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"results has a {n_lines_difference} lines difference with the solution"
        )

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

with tab3:
    st.write(answer)
