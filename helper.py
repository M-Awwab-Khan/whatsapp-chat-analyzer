from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import string
import emoji
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
    active_users = df['user'].value_counts().head()
    proportion_active_users = round(df['user'].value_counts(normalize=True)*100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return active_users, proportion_active_users

def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = process_message(df)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = process_message(df)
    words = []
    for msg in df['message']:
        for word in msg.lower().split():
            words.append(word)
    
    most_common_20_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_20_df

def process_message(df):
    f = open('romanurdustopwords.txt', 'r')
    stopwords = f.read()

    temp = df[(df['message'] != '<Media omitted>\n') & (df['user'] != 'group_notification')]

    def remove_stopwords_and_punctuation(msg):
        words = []
        for word in msg.lower().split():
            if word not in stopwords and word not in string.punctuation:
                words.append(word)
        return " ".join(words)
    temp['message'] = temp['message'].apply(remove_stopwords_and_punctuation)
    return temp

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    x = timeline['month'] + '-' + timeline['year'].astype(str)
    time = x.tolist()

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline