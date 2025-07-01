import streamlit as st
import pandas as pd
from io import BytesIO
import os
import re

st.title('Shareholding Data Uploader & Pivot')

uploaded_files = st.file_uploader(
    'Upload as many Excel or CSV shareholding statements as you want',
    type=['csv', 'xlsx'],
    accept_multiple_files=True
)

REQUIRED_COLUMNS = ['Company Name', 'Free']
all_data = []

def extract_owner_from_filename(filename):
    # Extract words between 'CLIENT' and 'CLIENT-ID' (case-insensitive)
    match = re.search(r'CLIENT\s*([^-|_]+?)\s*CLIENT-ID', filename, re.IGNORECASE)
    if match:
        return match.group(1).strip().replace('_', ' ').replace('-', ' ')
    return os.path.splitext(filename)[0]

if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded.")
    for i, file in enumerate(uploaded_files, 1):
        # Use words between 'CLIENT' and 'CLIENT-ID' as owner name
        owner = extract_owner_from_filename(file.name)
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file, header=5)  # Skip the first 5 lines
            # Exclude the last row (totals or summary)
            if len(df) > 1:
                df = df.iloc[:-1]
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_cols:
                st.warning(f"Missing columns in {file.name}: {missing_cols}")
            else:
                df = df[REQUIRED_COLUMNS].copy()
                df['Owner Name'] = owner
                all_data.append(df)
        except Exception as e:
            st.error(f"Error processing {file.name}: {e}")

    if all_data:
        merged_df = pd.concat(all_data, ignore_index=True)
        # Convert Free to numeric for pivoting (ensure fillna is called on Series)
        merged_df['Free'] = pd.to_numeric(merged_df['Free'], errors='coerce')
        merged_df['Free'] = merged_df['Free'].fillna(0)
        pivot_df = pd.pivot_table(
            merged_df,
            index='Company Name',
            columns='Owner Name',
            values='Free',
            aggfunc='sum',
            fill_value=0
        )
        st.subheader('Pivot Table: Company vs Owner (Shares)')
        st.dataframe(pivot_df)

        # Export buttons
        def to_csv(df):
            return df.to_csv().encode('utf-8')
        def to_excel(df):
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:  # type: ignore
                df.to_excel(writer)
            buffer.seek(0)
            return buffer.getvalue()

        st.download_button(
            label="Download as CSV",
            data=to_csv(pivot_df),
            file_name="pivoted_shareholding.csv",
            mime="text/csv"
        )
        st.download_button(
            label="Download as Excel",
            data=to_excel(pivot_df),
            file_name="pivoted_shareholding.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.info('Please upload as many Excel or CSV files as you want to begin.') 