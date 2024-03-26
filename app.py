import streamlit as st
from preprocessor import preprocess
from helper import fetch_stats, most_active_users, create_wordcloud, most_common_words, emoji_helper, monthly_timeline, daily_timeline, week_activity_map, month_activity_map, activity_heatmap
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocess(data)

    #st.dataframe(df)

    user_list = df.user.unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Analysis with respect to', user_list)

    if st.sidebar.button('Show Analysis'):
        col1, col2, col3, col4 = st.columns(4)

        num_messages, num_words, num_media, num_links = fetch_stats(selected_user, df)
        st.title("Top Statistics")
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

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = monthly_timeline(selected_user,df)
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=timeline['time'], y=timeline['message'], mode='lines', marker=dict(color='red')))
        
        fig.update_layout(
            xaxis=dict(title='Time', tickfont=dict(size=14)),
            yaxis=dict(title='Message',tickfont=dict(size=14)),
            xaxis_tickangle=-90,
            autosize=True
        )
        st.plotly_chart(fig)

        # daily timeline
        st.title("Daily Timeline")
        d_timeline = daily_timeline(selected_user, df)
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=d_timeline['only_date'], y=d_timeline['message'], mode='lines', marker=dict(color='red')))
        
        fig.update_layout(
            xaxis=dict(title='Time', tickfont=dict(size=14)),
            yaxis=dict(title='Message',tickfont=dict(size=14)),
            xaxis_tickangle=-90,
            autosize=True
        )
        st.plotly_chart(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            busy_day = week_activity_map(selected_user,df)
            # Create a Plotly figure
            fig = go.Figure()    
            fig.add_trace(go.Bar(x=busy_day.index, y=busy_day.values, marker_color='red'))
            fig.update_layout(
                title="Most active day",
                xaxis=dict(title='Weekday'),
                yaxis=dict(title='Messages'),
                autosize=True
            )
            st.plotly_chart(fig)

        with col2:
            busy_month = month_activity_map(selected_user, df)
            fig = go.Figure()    
            fig.add_trace(go.Bar(x=busy_month.index, y=busy_month.values, marker_color='red'))
            fig.update_layout(
                title="Most active month",
                xaxis=dict(title='Month'),
                yaxis=dict(title='Messages'),
                autosize=True
            )
            st.plotly_chart(fig)

        st.title("Weekly Activity Map")
        user_heatmap = activity_heatmap(selected_user,df)
        fig,ax = plt.subplots(figsize=(20, 6))
        ax = sns.heatmap(user_heatmap, cmap='Reds')
        st.pyplot(fig)

        # finding the active users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Active Users')
            col1,col2 = st.columns(2)
            active_users, proportion_active_users = most_active_users(df)
            # Create a Plotly bar chart for most active users
            with col1:
                bar_fig = go.Figure(go.Bar(
                    x=active_users.index,
                    y=active_users.values,
                    marker_color='red'
                ))
            
                # Update layout for bar chart
                bar_fig.update_layout(
                    title='Most Active Users',
                    xaxis=dict(title='Name'),
                    yaxis=dict(title='Messages'),
                )
                st.plotly_chart(bar_fig)
                
                
            with col2:
                # Create a Plotly pie chart for proportion of active users
                pie_fig = go.Figure(go.Pie(
                    labels=proportion_active_users['name'].head(10),
                    values=proportion_active_users['percent'].head(10),
                    textinfo='percent',
                    marker=dict(colors=sns.color_palette('hls')),
                ))
                
                # Update layout for pie chart
                pie_fig.update_layout(
                    title='Proportion of Active Users',
                )
            
                st.plotly_chart(pie_fig)

        # wordcloud
        st.title("Wordcloud")
        df_wc = create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_20_df = most_common_words(selected_user, df)

        fig,ax = plt.subplots()
        most_common_20_df.sort_values(1, inplace=True)
        ax.barh(most_common_20_df[0], most_common_20_df[1], color='red')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)