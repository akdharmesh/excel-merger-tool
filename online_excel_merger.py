import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Excel Merger Tool", layout="centered")

st.title("📊 Online Excel Merger Tool")
st.write("Upload multiple Excel files, select columns, and merge them into one file.")

uploaded_files = st.file_uploader(
    "Upload your XLSX files",
    type="xlsx",
    accept_multiple_files=True
)

if uploaded_files:
    try:
        first_df = pd.read_excel(uploaded_files[0])
        all_columns = first_df.columns.tolist()

        selected_columns = st.multiselect(
            "✅ Select columns to merge:",
            options=all_columns,
            default=all_columns
        )

        if selected_columns:
            if st.button("🚀 Merge Files"):
                progress = st.progress(0)
                all_data = []

                total_files = len(uploaded_files)

                for i, file in enumerate(uploaded_files):
                    df = pd.read_excel(file)
                    df = df[selected_columns]
                    df["Source_File"] = file.name
                    all_data.append(df)

                    time.sleep(0.3)
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

        else:
            st.warning("⚠ Please select at least one column.")

    except Exception as e:
        st.error(str(e))
