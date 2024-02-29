def fetch_stats(selected_user, df):

    if selected_user == 'Overall':
        num_messages = df.shape[0]
        num_words = 0
        for msg in df['message'].tolist():
            num_words += len(msg.split())
        return num_messages, num_words
    
    else:
        user_df = df[df['user'] == selected_user]
        num_messages = user_df.shape[0]
        num_words = 0
        for msg in user_df['message'].tolist():
            num_words += len(msg.split())
        return num_messages, num_words