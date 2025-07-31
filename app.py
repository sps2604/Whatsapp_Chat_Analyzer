import streamlit as st
import matplotlib.pyplot as plt
from streamlit import columns
import seaborn as sns
import preprocess,helper


st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocess.preprocess(data)

    #st.dataframe(df)


    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt",user_list)

    num_messages = 0
    words = 0
    num_media_messages = 0
    num_links = 0
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        pass

    st.title('Top Statistics')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header("Total Messages")
        st.title(num_messages)
    with col2:
        st.header("Total Words")
        st.title(words)
    with col3:
        st.header("Total Media Messages ")
        st.title(num_media_messages)
    with col4:
        st.header("Total URLs ")
        st.title(num_links)

    # Monthly Timeline
    st.title('Monthly Timeline')
    monthly_timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(monthly_timeline['time'], monthly_timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # Daily Timeline
    st.title('Daily Timeline')
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # activity map
    st.title('Activity Map')
    col1, col2 = st.columns(2)

    with col1:
        st.header("Most busy day")
        busy_day = helper.weekly_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_day.index, busy_day.values, color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    with col2:
        st.header("Most busy month")
        busy_month = helper.monthly_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(busy_month.index, busy_month.values, color='orange')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

    st.title("Weekly Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user, df)
    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)
    # Finding the busiest user in the group

    if selected_user == 'Overall':
        st.title('Most Busy User')
        x, new_df = helper.most_busy_user(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    # Wordcloud
    st.title('Word Cloud')
    wc_df = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(wc_df)
    st.pyplot(fig)

    # Most Common Words
    most_common_df = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation = 'vertical')
    st.title('Most Common Words')
    st.pyplot(fig)

    # Emoji Analysis
    emoji_df = helper.emoji_helper(selected_user, df)
    st.title('Emoji Analysis')

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct="%0.2f")
        st.pyplot(fig)