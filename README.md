# 📊 Holdings Manager

**Holdings Manager** is a secure and user-friendly web app that lets you upload multiple shareholding statement files (Excel or CSV), extract & merge ownership data, and generate an insightful pivot table—company-wise and owner-wise. Each user gets a private workspace to manage and export pivot tables securely.

---

## 🚀 Live Demo

👉 [Try it now](https://hold-letter.streamlit.app)


---

## ✅ Key Features

- 🔐 **Password-Protected Access**
  - Login required to access save, load, and delete features
  - Passwords stored securely via `secrets.toml`
  - Each password unlocks a private data workspace

- 📂 **Multi-File Upload**
  - Upload 9–10 Excel or CSV shareholding statements at once
  - Intelligent handling of each file:
    - Skips first **5 rows** (Excel headers)
    - Skips **last row** (summary/total)
    - Selects:
      - Column 2 as **Company Name**
      - Column 9 as **Total Shares**

- 🧠 **Smart Owner Extraction**
  - Owner name auto-extracted from filename:
    - Finds text between `'CLIENT'` and `'CLIENT-ID'`
    - If not found, defaults to filename (no extension)

- 📊 **Pivot Table Generator**
  - Merges all data into a single pivot table:
    - **Rows:** Company Name
    - **Columns:** Owner Name
    - **Values:** Total shares
    - **Total Holdings** column: Auto-calculated and always last

- 📥 **Export Options**
  - Download pivot table as **CSV** or **Excel**

- 💾 **Save & Load Pivot Tables**
  - Save pivot tables with auto timestamp
  - Load/view previous saves
  - Delete old pivot tables
  - Each user sees only their own saved pivots

- 🖥️ **Streamlit UI Perks**
  - Fullscreen responsive layout (desktop + mobile)
  - Sort, filter, scroll, and resize pivot tables
  - Drag & drop file uploads
  - Masked password input
  - Instant feedback via success/warning/error messages

- 🔐 **Security & Data Privacy**
  - No passwords stored in code
  - `.gitignore` excludes sensitive data
  - Saved data is isolated by user via SHA256-hashed folders


---

## 🛠️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd <repo-directory>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   - Navigate to `http://localhost:8501` or the link shown in your terminal

---

## 🧪 Usage Guide

1. Prepare Excel or CSV files with shareholding data.
2. Make sure filenames contain owner info:
   - Format: `Client ABC Client-ID 123.xlsx`
   - Owner will be extracted as `ABC`
3. Upload the files in the app.
4. The pivot table will be generated automatically.
5. Use search/sort tools or scroll to view full data.
6. Download the table as CSV or Excel.
7. Log in to save your pivot tables and manage them later.

---

## 📝 File Naming Examples

| File Name Example                                   | Extracted Owner |
|-----------------------------------------------------|------------------|
| `Client Abc CLIENT-ID 291 Demat 8xxxxx.xlsx`       | `ABC`           |
| `CLIENT 123 CLIENT-ID 999 Sample Statement.xlsx`   | `123`           |

---

## 📦 Requirements

- Python 3.8+
- streamlit
- pandas
- openpyxl
