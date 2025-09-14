# pylint: disable = missing-module-docstring
"""
SQL SRS (Spaced Repetition System) Application

A Streamlit application for practicing SQL queries with spaced repetition learning.
Users can select themes, practice SQL queries, and compare their results with solutions.
"""

import logging
import os
import subprocess
from typing import Optional, Tuple

import duckdb
import pandas as pd
import streamlit as st


def ensure_data_directory() -> None:
    """Ensure the data directory exists for storing the database."""
    if "data" not in os.listdir():
        print("creating folder data")
        logging.error(os.listdir())
        logging.error("creating folder data")
        os.mkdir("data")


def ensure_database_exists() -> None:
    """Ensure the SQL exercises database exists, create it if not."""
    if "exercises_sql_tables.duckdb" not in os.listdir("data"):
        subprocess.run(["python", "init_db.py"], check=True)


def get_database_connection() -> duckdb.DuckDBPyConnection:
    """
    Create and return a database connection.
    
    Returns:
        duckdb.DuckDBPyConnection: Database connection object
    """
    return duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


def get_available_themes(connection: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """
    Get all available themes from the memory_state table.
    
    Args:
        connection: Database connection object
        
    Returns:
        pd.DataFrame: DataFrame containing distinct themes
    """
    return connection.execute("SELECT DISTINCT theme FROM memory_state").df()


def get_exercise_query(theme: Optional[str]) -> str:
    """
    Generate the appropriate SQL query based on theme selection.
    
    Args:
        theme: Selected theme name or None for all themes
        
    Returns:
        str: SQL query string
    """
    if theme:
        return f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    return "SELECT * FROM memory_state"


def get_exercises(connection: duckdb.DuckDBPyConnection, theme: Optional[str]) -> pd.DataFrame:
    """
    Get exercises sorted by last reviewed date.
    
    Args:
        connection: Database connection object
        theme: Selected theme name or None for all themes
        
    Returns:
        pd.DataFrame: Sorted exercises DataFrame
    """
    query = get_exercise_query(theme)
    return (
        connection.execute(query)
        .df()
        .sort_values("last_reviewed", ascending=True)
        .reset_index()
    )

def load_exercise_question(exercise_name: str) -> str:
    """
    Load the SQL question for a given exercise.
    
    Args:
        exercise_name: Name of the exercise file
    """
    with open(f"questions/{exercise_name}.sql", "r", encoding="utf-8") as f:
        return f.read()

def load_exercise_solution(exercise_name: str) -> str:
    """
    Load the SQL solution for a given exercise.
    
    Args:
        exercise_name: Name of the exercise file
        
    Returns:
        str: SQL solution content
    """
    with open(f"answers/{exercise_name}.sql", "r", encoding="utf-8") as f:
        return f.read()


def execute_user_query(connection: duckdb.DuckDBPyConnection, query: str) -> pd.DataFrame:
    """
    Execute user's SQL query and return results.
    
    Args:
        connection: Database connection object
        query: SQL query string
        
    Returns:
        pd.DataFrame: Query results
    """
    return connection.execute(query).df()


def validate_query_results(user_results: pd.DataFrame, solution_df: pd.DataFrame) -> Tuple[bool, str, int]:
    """
    Validate user query results against solution.
    
    Args:
        user_results: User's query results
        solution_df: Expected solution results
        
    Returns:
        Tuple[bool, str, int]: (is_valid, error_message, line_difference)
    """
    # Check columns
    try:
        user_results = user_results[solution_df.columns]
        column_error = ""
    except KeyError:
        column_error = "Some columns are missing"
    
    # Check row count
    line_difference = user_results.shape[0] - solution_df.shape[0]
    
    is_valid = not column_error and line_difference == 0
    return is_valid, column_error, line_difference


def render_sidebar(connection: duckdb.DuckDBPyConnection) -> Tuple[Optional[str], pd.DataFrame, str, pd.DataFrame]:
    """
    Render the sidebar with theme selection and exercise data.
    
    Args:
        connection: Database connection object
        
    Returns:
        Tuple containing theme, exercises, exercise_name, and solution_df
    """
    available_theme_df = get_available_themes(connection)
    theme = st.selectbox(
        "what would you like to work on",
        available_theme_df["theme"],
        index=None,
        placeholder="Select a theme...",
    )
    
    if theme:
        st.write("You chose:", theme)
    
    exercises = get_exercises(connection, theme)
    st.write(exercises)
    
    # Getting the exercise solution
    exercise_name = exercises.loc[0, "exercise_name"]
    answer = load_exercise_solution(exercise_name)
    solution_df = connection.execute(answer).df()
    
    return theme, exercises, exercise_name, solution_df


def render_query_input(exercise_name: str) -> str:
    """
    Render the query input area with question.
    
    Args:
        exercise_name: Name of the exercise file
        
    Returns:
        str: User's SQL query
    """
    
    
    # Display the question
    question_sql = load_exercise_question(exercise_name)
    st.header(f" {question_sql}")
    
    return st.text_area(label="votre_code_sql", key="query", height=200)


def render_query_results(connection: duckdb.DuckDBPyConnection, query: str, solution_df: pd.DataFrame) -> None:
    """
    Render query results and validation.
    
    Args:
        connection: Database connection object
        query: User's SQL query
        solution_df: Expected solution results
    """
    if not query:
        return
        
    results = execute_user_query(connection, query)
    st.dataframe(results)
    
    # Validate results
    is_valid, column_error, line_difference = validate_query_results(results, solution_df)
    
    if column_error:
        st.write(column_error)
    
    if line_difference != 0:
        st.write(f"results has a {line_difference} lines difference with the solution")
    
    if is_valid:
        st.success("Query results match the solution!")


def render_tables_tab(exercises: pd.DataFrame, connection: duckdb.DuckDBPyConnection) -> None:
    """
    Render the tables tab showing exercise data.
    
    Args:
        exercises: Exercises DataFrame
        connection: Database connection object
    """
    exercise_tables = exercises.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = connection.execute(f"SELECT * FROM {table}").df()
        st.dataframe(df_table)

def render_solution_tab(solution_sql: str) -> None:
    """
    Render the solution tab showing the SQL solution.
    
    Args:
        solution_sql: SQL solution string
    """
    st.write(solution_sql)


# Main application logic
def main() -> None:
    """Main application entry point."""
    # Initialize data and database
    ensure_data_directory()
    ensure_database_exists()
    
    # Get database connection
    connection = get_database_connection()
    
    # Render sidebar and get exercise data
    with st.sidebar:
        theme, exercises, exercise_name, solution_df = render_sidebar(connection)
    
    # Render query input with question
    query = render_query_input(exercise_name)
    
    # Render query results and validation
    render_query_results(connection, query, solution_df)
    
    # Render tabs
    tab2, tab3 = st.tabs(["Tables", "Solution"])
    
    with tab2:
        render_tables_tab(exercises, connection)
    
    with tab3:
        solution_sql = load_exercise_solution(exercise_name)
        render_solution_tab(solution_sql)


if __name__ == "__main__":
    main()

