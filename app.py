import streamlit as st
from preprocessor import preprocess

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocess(data)

    st.dataframe(df)

    user_list = df.user.unique().tolist()

    st.sidebar.selectbox('Analysis with respect to', user_list)