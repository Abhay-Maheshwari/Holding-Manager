import streamlit as st
import pandas as pd
from io import BytesIO
import os
import re
from datetime import datetime
import hashlib
import pytz

# Configure the page
st.set_page_config(
    page_title="Holdings Manager",
    page_icon="assets/favicon-light.ico",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Set the title of the Streamlit app
st.title('Holdings Manager')

# --- Allowed Passwords from Streamlit secrets.toml ---
ALLOWED_PASSWORDS = [
    st.secrets.get("password1", ""),
    st.secrets.get("password2", ""),
    st.secrets.get("password3", ""),
    st.secrets.get("password4", ""),
]
ALLOWED_PASSWORDS = [p for p in ALLOWED_PASSWORDS if p]  # Remove empty entries

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "current_password" not in st.session_state:
    st.session_state["current_password"] = None

# Function to hash the password for folder separation
def get_password_hash(password):
    if password is None:
        return "default"
    return hashlib.sha256(password.encode()).hexdigest()

# Password authentication
if not st.session_state["authenticated"]:
    pwd = st.text_input("Enter password to access save/delete features", type="password")
    if st.button("Login"):
        if pwd in ALLOWED_PASSWORDS:
            st.session_state["authenticated"] = True
            st.session_state["password_hash"] = get_password_hash(pwd)
            st.session_state["current_password"] = pwd
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

pivot_df = None  # Will hold the current pivot table if available

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
            if df.shape[1] > 9:
                df = df.iloc[:, [1, 9]]  # [1] is Company Name, [8] is Total
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
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)
        excel_filename = f"pivot - {now.strftime('%d-%m-%Y')} - {now.strftime('%H-%M-%S')}.xlsx"
        st.download_button(
            label="Download as Excel",
            data=to_excel(pivot_df),
            file_name=excel_filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# --- Save/Delete/Load Pivot Table (Password Protected) ---
if st.session_state["authenticated"]:
    st.markdown("---")
    st.header("Save/Delete/Load Pivot Table")
    # Use a per-password folder for saved pivots
    user_folder = os.path.join("saved_pivots", get_password_hash(st.session_state["current_password"]))
    os.makedirs(user_folder, exist_ok=True)
    # Save pivot table (only if available)
    if pivot_df is not None:
        if st.button("Save Pivot Table"):
            ist = pytz.timezone('Asia/Kolkata')
            now = datetime.now(ist)
            save_name = f"Pivot_Date-{now.strftime('%d-%m-%Y')}_Time-{now.strftime('%H-%M-%S')}"
            pivot_df.to_csv(f"{user_folder}/{save_name}.csv")
            st.success(f"Saved as {save_name}.csv")
    # List, load, and delete saved pivots
    saved_files = os.listdir(user_folder) if os.path.exists(user_folder) else []
    if saved_files:
        file_to_manage = st.selectbox("Select a saved pivot:", saved_files)
        if st.button("Delete Selected Pivot"):
            os.remove(f"{user_folder}/{file_to_manage}")
            st.success(f"Deleted {file_to_manage}")
        if st.button("Load/View Selected Pivot"):
            loaded_df = pd.read_csv(f"{user_folder}/{file_to_manage}", index_col=0)
            st.subheader(f"Loaded Pivot Table: {file_to_manage}")
            st.dataframe(loaded_df)
    else:
        st.info("No saved pivots found.")

# --- View Downloaded Pivot Table ---
st.markdown("---")
st.header("View Downloaded Pivot Table")
view_file = st.file_uploader(
    "Upload a previously downloaded pivot table (CSV or Excel) to view it here.",
    type=["csv", "xlsx"],
    key="view_pivot"
)
if view_file is not None:
    try:
        if view_file.name.endswith(".csv"):
            view_df = pd.read_csv(view_file, index_col=0)
        else:
            view_df = pd.read_excel(view_file, index_col=0)
        st.subheader(f"Preview: {view_file.name}")
        st.dataframe(view_df)
    except Exception as e:
        st.error(f"Could not load file: {e}")

else:
    # Show info message if no files are uploaded
    st.info('Please upload as many Excel or CSV files as you want to begin.') 