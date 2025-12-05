import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Excel Merger Tool", layout="centered")

st.title("⚡ Online Excel Merger Tool By AD")
st.write("Upload Excel files, select columns, and merge them instantly.")

# ---------------- FILE UPLOAD ---------------- #

uploaded_files = st.file_uploader(
    "✅ Upload your XLSX files",
    type="xlsx",
    accept_multiple_files=True
)

selected_columns = []

# ---------------- COLUMN SELECTION ---------------- #

if uploaded_files:
    try:
        first_df = pd.read_excel(uploaded_files[0], engine="openpyxl")
        all_columns = first_df.columns.tolist()

        selected_columns = st.multiselect(
            "✅ Select columns to merge:",
            options=all_columns,
            default=all_columns
        )

    except Exception as e:
        st.error("Error reading Excel file")
        st.error(str(e))

# ---------------- START MERGE BUTTON ---------------- #

start_merge = st.button("🚀 Start Merge")

# ---------------- FAST MERGING ---------------- #

@st.cache_data(show_spinner="⚡ Merging files...")
def fast_merge(files, selected_columns):
    all_data = []

    for file in files:
        df = pd.read_excel(file, engine="openpyxl")
        df = df[selected_columns]
        df["Source_File"] = file.name
        all_data.append(df)

    merged_df = pd.concat(all_data, ignore_index=True)
    return merged_df

if start_merge:

    if not uploaded_files:
        st.warning("⚠ Please upload Excel files first.")
        st.stop()

    if not selected_columns:
        st.warning("⚠ Please select at least one column.")
        st.stop()

    merged_df = fast_merge(uploaded_files, selected_columns)

    st.success("✅ Files merged!")

    # ✅ ✅ CORRECT IN-MEMORY DOWNLOAD (NO ERROR)
    output = BytesIO()
    merged_df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    st.download_button(
        label="⬇ Download Merged Excel",
        data=output,
        file_name="merged_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
