from urlextract import URLExtract
extractor = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    num_words = 0
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    num_links = 0
    for msg in df['message']:
        num_links += len(extractor.find_urls(msg))
        num_words += len(msg.split())
    return num_messages, num_words, num_media, num_links

def most_active_users(df):
    return df['user'].value_counts().head()