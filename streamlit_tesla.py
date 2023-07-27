import streamlit as st
import sqlite3
import pandas as pd





def load_data(table_name):
    # Establish a connection to the database
    conn = sqlite3.connect('/Users/aryasachar/Desktop/final_cleaned_project.db')

    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():

    st.title("Tesla Accident Data")

    # Sidebar: Table selection
   # st.sidebar.subheader("Table Selection")
   # table_names = ['accidents']
   # selected_table = st.sidebar.selectbox("Select a table", table_names)

    # Load data from the selected table
    df = load_data('accidents')

    tesla_logo_path = '/Users/aryasachar/Desktop/logotesla.png'  
    st.image(tesla_logo_path, caption="Tesla Logo", use_column_width=True, output_format="auto")

    # Show the entire DataFrame
    st.subheader("Table: accidents")
    st.dataframe(df)

    # Allow users to enter row indices and column names to delete
    st.subheader("Delete Rows and Columns")
    rows_to_delete = st.text_input("Enter row indices to delete (comma-separated):")
    columns_to_delete = st.text_input("Enter column names to delete (comma-separated):")

    if st.button("Delete"):
        try:
            
            rows_list = [int(idx.strip()) for idx in rows_to_delete.split(",") if idx.strip().isdigit()]
            columns_list = [col.strip() for col in columns_to_delete.split(",")]

            # Delete specified rows and columns
            if rows_list:
                df = df.drop(rows_list, axis=0)
            if columns_list:
                df = df.drop(columns=columns_list)

            # Save the updated DataFrame to the 'accidents' table
            conn = sqlite3.connect('/Users/aryasachar/Desktop/final_cleaned_project.db')
            df.to_sql('accidents', conn, if_exists='replace', index=False)
            conn.close()

            st.success("Selected rows and columns deleted successfully!")
        except ValueError:
            st.error("Invalid row indices provided. Please enter valid integers.")
        except Exception as e:
            st.error(f"Error: {e}")




    # Allow users to enter SQL queries
    st.subheader("Extract Tesla Accident Data")
    user_query = st.text_area("Tesla Accidents:")
    if st.button("Run Query"):
        try:
            conn = sqlite3.connect('/Users/aryasachar/Desktop/final_cleaned_project.db')
            custom_df = pd.read_sql_query(user_query, conn)
            conn.close()

            if custom_df.empty:
                st.warning("Query returned an empty result.")
            else:
                st.dataframe(custom_df)
        except Exception as e:
            st.error(f"Error: {e}")


    # Add/Update Entry
    st.subheader("Add/Update Data: Please add 0 for any missing values in the input fields")
    new_entry = {}
    for column in df.columns:
        new_entry[column] = st.text_input(f"Enter {column}:", key=column)

    if st.button("Add/Update Entry"):
        try:
            conn = sqlite3.connect('/Users/aryasachar/Desktop/final_cleaned_project.db')
            df = load_data('accidents')  
            df = df.append(new_entry, ignore_index=True)
            df.to_sql('accidents', conn, if_exists='replace', index=False)
            conn.close()
            st.success("New entry added successfully!")

            # user will refresh the DataFrame with the updated data
            df = load_data('accidents')
            table.dataframe(df)  # Display the updated data in the table
        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
