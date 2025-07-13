
# 📊 Holdings Manager – Shareholding Data Uploader & Pivot Viewer

A powerful Streamlit-based web app to **upload, process, and analyze** multiple demat/shareholding statement files (Excel or CSV) into a clean pivot table format. Ideal for individuals and financial professionals managing multi-account portfolios.

## 🎯 Live Demo: 

Experience the full functionality of Holdings Manager in action — upload files, generate pivots, and explore all features in the live demo:

[Launch the App](https://hold-letter.streamlit.app/)


## 🚀 Key Features

This application offers a robust set of features to streamline your shareholding data management:

### 1. 📁 File Upload

- Multi-file Upload Support: Upload multiple CSV and Excel files simultaneously.

### 2. 🧠 Smart Aggregation

- Intelligent Client Matching: Merges data from files with the same client name automatically.

- Duplicate Prevention: Prevents double entries by summing duplicate company holdings.

### 3. 📊 Pivot Table

- Dynamic Pivot Generation: Companies as rows, Owners as columns, and summed holdings as values.

- Total Holdings Column: Auto-calculated totals across all owners for each company.

- Interactive Table: Sort, search, scroll, and resize columns.

### 4. ⬇️ Export Options

- Download as CSV / Excel: Export pivot with auto-timestamped filenames.

### 5. 🔐 Privacy & Security

- 100% Local Execution: All processing happens on your system — no cloud involved.

- Password-Protected Access: Enables secure Save/Delete/Load only after authentication.

- Separate Save Folders: Each password creates its own secure save directory.

### 6. 💾 Save & Load

- Save Pivot Table Locally: One-click save with timestamped filenames.

- Load Existing Pivots: Instantly preview previously saved tables.

- Delete Pivots: Safely delete saved pivot files with one click.

### 7. 🧩 File Compatibility

- Mixed Format Uploads: Upload .csv and .xlsx in any order — works seamlessly.

- Column Validation: Validates file structure and alerts if format is incorrect.

- Error Messaging: Catches and displays detailed upload errors per file.

### 8. 📂 Data Viewing

- Upload Previous Downloads: View older exported pivot files by re-uploading them.

### 9. 🧠 Automation & UX

- Owner Name Detection from Filename: Auto-extracts names from filenames like CLIENT_NAME_CLIENT-ID_123.xlsx.

- Audit-Ready Reporting: All files are timestamped, organized, and formatted for record-keeping.

### 10. 🖥️ UI & Performance

- Clean, Responsive UI: Built with Streamlit — fully responsive and centered layout.

- Fast Performance: Handles large datasets smoothly with minimal memory use.

---

## 📁 Example File Naming

These examples demonstrate how the app extracts the **owner name** automatically:

```
Client PERSON A Client-ID 123 Demat 1234567890123456.xlsx
Client ENTITY B Client-ID 456 Demat 6543210987654321.xlsx
```

Extracted names will be:  
`PERSON A`, `ENTITY B`

---

## 🛠 Setup Instructions

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/holdings-manager.git
cd holdings-manager
```

### 2. Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Add passwords for saving/viewing pivots:

Create a file: `.streamlit/secrets.toml`

```toml
[general]
password1 = "demo123"
password2 = "client456"
password3 = "..."
```

### 4. Run the app:

```bash
streamlit run app.py
```

Open the browser at the address shown in the terminal (e.g., `http://localhost:8501`).

---

## 🧪 How to Use

### 1. Prepare your demat statements in `.xlsx` or `.csv` format.
### 2. Click **Upload** and select multiple files.
### 3. App automatically extracts:
   - Owner name from file name
   - Relevant columns for company and total shares
### 4. View the live pivot table (filterable and scrollable).
### 5. Download the pivot table as **CSV** or **Excel**.
### 6. Use password login to:
   - Save your pivot table
   - Reload old ones
   - Delete any previous data saved under your login
  

---

## 📦 Requirements

- `Python 3.8+`
- `streamlit`
- `pandas`
- `openpyxl`
- `pytz`
- `pdfplumber` *(optional, if PDFs are later added)*

Install via:

```bash
pip install -r requirements.txt
```

---

## 📄 License

MIT License – use freely, modify, and share with credit.

---

## 👤 Author

**Abhay Maheshwari**  
💼 [LinkedIn](https://linkedin.com/maheshwari-abhay) | 🛠️ [GitHub](https://github.com/abhay-maheshwari)
