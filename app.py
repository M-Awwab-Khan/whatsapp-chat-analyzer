import streamlit as st
from preprocessor import preprocess
from helper import fetch_stats, most_active_users
import matplotlib.pyplot as plt

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

        num_messages, num_words, num_media, num_links = fetch_stats(selected_user, df)
        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Media Shared")
            st.title(num_media)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # finding the active users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Active Users')
            x = most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)