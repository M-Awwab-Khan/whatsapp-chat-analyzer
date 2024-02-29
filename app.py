import streamlit as st
from preprocessor import preprocess
from helper import fetch_stats

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocess(data)

    st.dataframe(df)

    user_list = df.user.unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Analysis with respect to', user_list)

    if st.sidebar.button('Show Analysis'):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(fetch_stats(selected_user, df))