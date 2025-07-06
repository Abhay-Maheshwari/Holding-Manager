
# 📊 Holdings Manager – Shareholding Data Uploader & Pivot Viewer

A powerful Streamlit-based web app to **upload, process, and analyze** multiple demat/shareholding statement files (Excel or CSV) into a clean pivot table format. Ideal for individuals and financial professionals managing multi-account portfolios.

---

## 🚀 Key Features

- ✅ Upload **multiple Excel/CSV** shareholding statements at once  
- 🧠 Auto-extracts:
  - **Company Name** and **Free/Total** holdings
  - **Owner name** from file name (between `CLIENT` and `CLIENT-ID`)
- 📊 Generates a pivot table:
  - **Rows:** Company Name  
  - **Columns:** Owner Name  
  - **Values:** Share count (from ‘Total’ column)
- 💾 Download the pivot table in:
  - CSV  
  - Excel (with timestamped filename)
- 🔐 Password-protected features:
  - Save pivot tables (user-isolated by password hash)
  - View previously saved pivots
  - Delete old pivots
- 🔁 View previously downloaded pivot tables by uploading them again

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

1. Prepare your demat statements in `.xlsx` or `.csv` format.
2. Click **Upload** and select multiple files.
3. App automatically extracts:
   - Owner name from file name
   - Relevant columns for company and total shares
4. View the live pivot table (filterable and scrollable).
5. Download the pivot table as **CSV** or **Excel**.
6. Use password login to:
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
