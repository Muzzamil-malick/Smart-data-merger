import streamlit as st
import pandas as pd
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Smart Data Merger", layout="wide")
st.title("🔬 Smart Scientific Data Merger")
st.markdown("**Designed by Muzzamil Malick**")

# File type selector
file_type = st.radio("📁 Select File Type:", options=["CSV", "Excel"])

# Upload files
st.header("📤 Upload Datasets")
col1, col2 = st.columns(2)

with col1:
    uploaded_file1 = st.file_uploader("Upload Reference File", type=["csv", "xlsx", "xls"], key="file1")

with col2:
    uploaded_file2 = st.file_uploader("Upload Second File", type=["csv", "xlsx", "xls"], key="file2")

# Function to handle file reading with encoding fallback
def read_file(uploaded_file, file_type):
    if uploaded_file is not None:
        try:
            if file_type == "CSV":
                try:
                    return pd.read_csv(uploaded_file, encoding="utf-8")
                except UnicodeDecodeError:
                    return pd.read_csv(uploaded_file, encoding="latin1")
            else:
                return pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"❌ Failed to read file: {e}")
    return None

# Read files
df1 = read_file(uploaded_file1, file_type)
df2 = read_file(uploaded_file2, file_type)

# Proceed if both files are uploaded
if df1 is not None and df2 is not None:
    st.header("⚙️ Merge Settings")

    cols_to_merge = st.multiselect("🧬 Select columns to bring from Reference File", df1.columns.tolist())
    key1 = st.selectbox("🔑 Merge Key in Reference File", df1.columns.tolist())
    key2 = st.selectbox("🔑 Merge Key in Second File", df2.columns.tolist())

    # Merge action
    if st.button("🔁 Merge Now"):
        try:
            df1[key1] = df1[key1].astype(str)
            df2[key2] = df2[key2].astype(str)

            cols_final = list(set([key1] + cols_to_merge))

            merged_df = pd.merge(df2, df1[cols_final], left_on=key2, right_on=key1, how='left')

            st.success(f"✅ Merge successful! Rows: {merged_df.shape[0]}, Columns: {merged_df.shape[1]}")
            st.dataframe(merged_df.head(10))

            # Download button
            def convert_df(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='MergedData')
                return output.getvalue()

            excel_data = convert_df(merged_df)

            st.download_button("📥 Download Merged Excel File", data=excel_data,
                               file_name="merged_data.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        except Exception as e:
            st.error(f"❌ Merge failed: {e}")
