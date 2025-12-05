import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fast Excel Merger Tool", layout="centered")

st.title("⚡ Fast Online Excel Merger Tool")
st.write("Upload Excel files, select columns, and merge them instantly.")

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

start_merge = st.button("🚀 Start Fast Merge")

# ---------------- FAST MERGING ---------------- #

@st.cache_data(show_spinner="⚡ Merging files at high speed...")
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

    st.success("✅ Files merged at high speed!")

    # ✅ In-memory download (FASTEST)
    output_bytes = merged_df.to_excel(index=False, engine="openpyxl")

    st.download_button(
        label="⬇ Download Merged Excel",
        data=merged_df.to_excel(index=False).encode(),
        file_name="merged_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
