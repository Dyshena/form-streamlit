import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# ===============================
# 1. KONFIGURASI GOOGLE SHEETS
# ===============================
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Link Google Sheet kamu
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1pOra9rJq4vuIqvpvOEWw-NEX1Oyvwy1QBjWn2SqUxIY/edit"

# ===============================
# 2. AMBIL DATA REGIONAL & CABANG
# ===============================
spreadsheet = client.open_by_url(SPREADSHEET_URL)
sheet_ref = spreadsheet.worksheet("Sheet1")
df_ref = pd.DataFrame(sheet_ref.get_all_records())

# ===============================
# 3. STREAMLIT FORM UI
# ===============================
st.title("📋 Form Input Cabang Berdasarkan Regional")

# Dropdown Regional
regional_list = sorted(df_ref["REGIONAL"].unique())
regional = st.selectbox("Pilih Regional", regional_list)

# Dropdown Cabang berdasarkan Regional
filtered = df_ref[df_ref["REGIONAL"] == regional]
cabang_list = sorted(filtered["CABANG"].unique())
cabang = st.selectbox("Pilih Cabang", cabang_list)

# Tombol Kirim
if st.button("Kirim"):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_baru = [waktu, regional, cabang]

    # ===============================
    # 4. SIMPAN HASIL KE SHEET "Hasil"
    # ===============================
    try:
        sheet_hasil = spreadsheet.worksheet("Hasil")
    except gspread.exceptions.WorksheetNotFound:
        sheet_hasil = spreadsheet.add_worksheet(title="Hasil", rows="1000", cols="10")
        sheet_hasil.append_row(["WAKTU", "REGIONAL", "CABANG"])  # header pertama

    sheet_hasil.append_row(data_baru)

    # Konfirmasi sukses
    st.success("✅ Data berhasil dikirim!")
    st.write(f"📌 {regional} - {cabang} ({waktu})")
