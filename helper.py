def fetch_stats(selected_user, df):

    if selected_user == 'Overall':
        return df.shape[0]
    
    else:
        return df[df['user'] == selected_user].shape[0]