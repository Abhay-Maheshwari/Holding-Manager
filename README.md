# Holdings Manager

This web app allows you to upload multiple shareholding statement files (Excel or CSV), automatically extract and merge the relevant data, and generate a pivot table showing company-wise shareholdings for each owner. You can also export the pivot table as CSV or Excel.

## Features
- Upload 9-10 Excel or CSV shareholding statement files at once
- Automatically extracts 'Company Name' and 'Free' columns
- Owner name is auto-extracted from the file name (between 'CLIENT' and 'CLIENT-ID')
- Skips the first row (for Excel files) and the last row (totals/summary) in each file
- Merges all data and creates a pivot table:
  - Rows: Company Name
  - Columns: Owner Name
  - Values: Shares (Free)
- Download the pivot table as CSV or Excel

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd <repo-directory>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the app:**
   ```bash
   streamlit run app.py
   ```
4. **Open your browser:**
   Go to the URL shown in the terminal (usually http://localhost:8501 or similar).

## Usage
1. Prepare your shareholding statement files in Excel or CSV format. The files should have columns like 'Company Name' and 'Free'.
2. The app will skip the first row (for Excel) and the last row (totals/summary) automatically.
3. Upload your files using the uploader.
4. The app will display a pivot table with company names as rows and owner names (from file names) as columns.
5. Download the pivot table as CSV or Excel for further analysis or sharing.

## Example File Naming
- `Client 123 Client-ID 2xx Demat 8xxxxx.xlsx`
- `Client ABC Client-ID 9xx Demat 9xxxxxxx.xlsx`

The owner name will be extracted as 'REETA MAHESHWARI' and 'DINESH MAHESHWARI HUF' respectively.

## Requirements
- Python 3.8+
- streamlit
- pandas
- openpyxl
