import streamlit as st
import pandas as pd
import pyodbc
from pandasai import SmartDataframe as PandasAI
from pandasai.llm import OpenAI

def main():
    st.title("PandasAI Chat App")
    #st.image("D:\hello.png", use_column_width=True)
    st.write("Connect to your SQL Server database to get started.")


    # Sidebar for input fields
    st.sidebar.subheader("Database Connection")
    server_name = st.sidebar.text_input("Server Name or IP")
    database_name = st.sidebar.text_input("Database Name")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    # Connect to SQL Server
    if st.sidebar.button("Connect"):
        try:
            conn = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
            )
            st.session_state.connection = conn
            st.success("Connected to the database.")
        except Exception as e:
            st.error(f"Error connecting to the database: {e}")

    # Main content area
    if 'connection' in st.session_state:
        conn = st.session_state.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM [dbo].[Sample - Superstore]')
        rows = cursor.fetchall()
        data = [tuple(row) for row in rows]
        df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
        cursor.close()

        st.subheader("ALL Records")
        st.write(df)

        llm = OpenAI(api_token="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")
        pandasai = PandasAI(df, config={"llm": llm})

        # Chat interface
        st.subheader("Chat Interface")
        prompt = st.text_input("Enter your prompt", "")
        if st.button("Generate Answer"):
            if prompt:
                response = pandasai.chat(prompt)
                st.write("Response:")
                st.write(response)
            else:
                st.warning("Please enter a prompt before generating an answer.")

if __name__ == "__main__":
    main()
