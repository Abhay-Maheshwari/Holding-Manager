import streamlit as st
import pandas as pd
from io import BytesIO
import os
import re
from datetime import datetime

# Set the title of the Streamlit app
st.title('Holdings Manager')

# --- Password Protection ---
PASSWORD = "your_secret_password"  # Change this to your desired password
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    pwd = st.text_input("Enter password to access save/delete features", type="password")
    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Access granted!")
        else:
            st.error("Incorrect password")

# File uploader widget for multiple Excel/CSV files
uploaded_files = st.file_uploader(
    'Upload as many Excel or CSV shareholding statements as you want',
    type=['csv', 'xlsx'],
    accept_multiple_files=True
)

# List to store all processed DataFrames
all_data = []

def extract_owner_from_filename(filename):
    """
    Extract the owner name from the file name.
    Looks for words between 'CLIENT' and 'CLIENT-ID'.
    If not found, uses the file name (without extension).
    """
    match = re.search(r'CLIENT\s*([^-|_]+?)\s*CLIENT-ID', filename, re.IGNORECASE)
    if match:
        return match.group(1).strip().replace('_', ' ').replace('-', ' ')
    return os.path.splitext(filename)[0]

# Main logic: only runs if files are uploaded
if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")
    for i, file in enumerate(uploaded_files, 1):
        # Extract owner name from file name
        owner = extract_owner_from_filename(file.name)
        try:
            # Read the file as a DataFrame
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                # For Excel, skip the first 5 lines (header=5)
                df = pd.read_excel(file, header=5)
            # Exclude the last row (often a totals/summary row)
            if len(df) > 1:
                df = df.iloc[:-1]
            # Select the second column as 'Company Name' and the ninth column as 'Total'
            if df.shape[1] > 8:
                df = df.iloc[:, [1, 8]]  # [1] is Company Name, [8] is Total
                df.columns = ['Company Name', 'Total']  # Rename columns for clarity
                df['Owner Name'] = owner  # Add owner name column
                all_data.append(df)  # Add to list for merging
            else:
                st.warning(f"File {file.name} does not have enough columns.")
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    # If any data was successfully processed
    if all_data:
        # Merge all DataFrames into one
        merged_df = pd.concat(all_data, ignore_index=True)
        # Convert the 'Total' column to numeric (in case of text/NaN)
        merged_df['Total'] = pd.to_numeric(merged_df['Total'], errors='coerce')
        merged_df['Total'] = merged_df['Total'].fillna(0)
        # Create a pivot table: rows=Company Name, columns=Owner Name, values=Total
        pivot_df = pd.pivot_table(
            merged_df,
            index='Company Name',
            columns='Owner Name',
            values='Total',
            aggfunc='sum',
            fill_value=0
        )
        # Add a 'Total Holdings' column summing across all owners for each company
        pivot_df['Total Holdings'] = pivot_df.sum(axis=1)
        # Ensure 'Total Holdings' is the last column
        cols = list(pivot_df.columns)
        if 'Total Holdings' in cols:
            cols = [c for c in cols if c != 'Total Holdings'] + ['Total Holdings']
            pivot_df = pivot_df[cols]
        # Show the pivot table in the app
        st.subheader('Holdings')
        st.dataframe(pivot_df)

        # Helper function to export DataFrame as CSV
        def to_csv(df):
            return df.to_csv().encode('utf-8')
        # Helper function to export DataFrame as Excel
        def to_excel(df):
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:  # type: ignore
                df.to_excel(writer)
            buffer.seek(0)
            return buffer.getvalue()

        # Download button for CSV
        st.download_button(
            label="Download as CSV",
            data=to_csv(pivot_df),
            file_name="pivoted_shareholding.csv",
            mime="text/csv"
        )
        # Download button for Excel
        st.download_button(
            label="Download as Excel",
            data=to_excel(pivot_df),
            file_name="pivoted_shareholding.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # --- Save/Delete/Load Pivot Table (Password Protected) ---
        if st.session_state["authenticated"]:
            st.markdown("---")
            st.header("Save/Delete/Load Pivot Table")
            os.makedirs("saved_pivots", exist_ok=True)
            # Save pivot table
            save_name = st.text_input("Save as (filename):", value=f"pivot_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            if st.button("Save Pivot Table"):
                pivot_df.to_csv(f"saved_pivots/{save_name}.csv")
                st.success(f"Saved as {save_name}.csv")
            # List, load, and delete saved pivots
            saved_files = os.listdir("saved_pivots") if os.path.exists("saved_pivots") else []
            if saved_files:
                file_to_manage = st.selectbox("Select a saved pivot:", saved_files)
                if st.button("Delete Selected Pivot"):
                    os.remove(f"saved_pivots/{file_to_manage}")
                    st.success(f"Deleted {file_to_manage}")
                if st.button("Load/View Selected Pivot"):
                    loaded_df = pd.read_csv(f"saved_pivots/{file_to_manage}", index_col=0)
                    st.subheader(f"Loaded Pivot Table: {file_to_manage}")
                    st.dataframe(loaded_df)
            else:
                st.info("No saved pivots found.")
else:
    # Show info message if no files are uploaded
    st.info('Please upload as many Excel or CSV files as you want to begin.') 