import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Excel Merger Tool", layout="centered")

st.title("📊 Online Excel Merger Tool")
st.write("Upload Excel files, select columns, then click **Start Merging**.")

# ---------------- FILE UPLOAD ---------------- #

uploaded_files = st.file_uploader(
    "✅ Upload your XLSX files",
    type="xlsx",
    accept_multiple_files=True
)

# ---------------- COLUMN SELECTION ---------------- #

selected_columns = []

if uploaded_files:
    try:
        first_df = pd.read_excel(uploaded_files[0])
        all_columns = first_df.columns.tolist()

        st.subheader("✅ Select columns to merge")

        selected_columns = st.multiselect(
            "Tick the columns you want:",
            options=all_columns,
            default=all_columns
        )

    except Exception as e:
        st.error("Error reading Excel file")
        st.error(str(e))

# ---------------- START MERGE BUTTON ---------------- #

st.subheader("🚀 Start Merging")

start_merge = st.button("▶ Start Merging Now")

# ---------------- MERGING PROCESS ---------------- #

if start_merge:

    if not uploaded_files:
        st.warning("⚠ Please upload Excel files first.")
        st.stop()

    if not selected_columns:
        st.warning("⚠ Please select at least one column.")
        st.stop()

    progress = st.progress(0)
    status_text = st.empty()

    all_data = []
    total_files = len(uploaded_files)

    for i, file in enumerate(uploaded_files):
        status_text.text(f"Merging file {i+1} of {total_files}...")

        df = pd.read_excel(file)
        df = df[selected_columns]
        df["Source_File"] = file.name

        all_data.append(df)

        time.sleep(0.5)   # ✅ REQUIRED for visible progress
        progress.progress((i + 1) / total_files)

    merged_df = pd.concat(all_data, ignore_index=True)

    st.success("✅ Files merged successfully!")

    output_file = "merged_output.xlsx"
    merged_df.to_excel(output_file, index=False)

    with open(output_file, "rb") as f:
        st.download_button(
            label="⬇ Download Merged Excel",
            data=f,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
