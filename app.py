import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Smart Data Merger", layout="wide")

st.title("🔬 Smart Scientific Data Merger")
st.markdown("**Designed by Muzzamil Malick**")

# 1. Choose file type
file_type = st.radio("📁 Select File Type:", options=["CSV", "Excel"])

# 2. Upload Files
st.header("📤 Upload Datasets")

col1, col2 = st.columns(2)

with col1:
    uploaded_file1 = st.file_uploader("Upload Reference File", type=["csv", "xlsx", "xls"], key="file1")
with col2:
    uploaded_file2 = st.file_uploader("Upload Second File", type=["csv", "xlsx", "xls"], key="file2")

# Function to read file
def read_file(uploaded_file, file_type):
    if uploaded_file is not None:
        if file_type == "CSV":
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
    return None

df1 = read_file(uploaded_file1, file_type)
df2 = read_file(uploaded_file2, file_type)

# 3. Column selectors
if df1 is not None and df2 is not None:
    st.header("⚙️ Merge Settings")

    cols_to_merge = st.multiselect("🧬 Select columns to bring from Reference File", df1.columns.tolist())
    key1 = st.selectbox("🔑 Merge Key in Reference File", df1.columns.tolist())
    key2 = st.selectbox("🔑 Merge Key in Second File", df2.columns.tolist())

    # 4. Merge and show preview
    if st.button("🔁 Merge Now"):
        df1[key1] = df1[key1].astype(str)
        df2[key2] = df2[key2].astype(str)

        cols_final = list(set([key1] + cols_to_merge))
        merged_df = pd.merge(df2, df1[cols_final], left_on=key2, right_on=key1, how='left')

        st.success(f"✅ Merge successful! Rows: {merged_df.shape[0]}, Columns: {merged_df.shape[1]}")
        st.dataframe(merged_df.head(10))

        # 5. Download merged data
        def convert_df(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='MergedData')
            processed_data = output.getvalue()
            return processed_data

        excel_data = convert_df(merged_df)
        st.download_button("📥 Download Merged Excel File", data=excel_data, file_name="merged_data.xlsx", mime="application/vnd.ms-excel")
