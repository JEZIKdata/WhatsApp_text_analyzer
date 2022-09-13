import streamlit as st
import preprocess
import stats
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# setting style of graphs

plt.style.use("dark_background")

st.sidebar.title("Whatsapp Chat Analyzer")

# uploading a file

uploaded_file = st.sidebar.file_uploader("")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    # converting the bytecode to the text-file

    data = bytes_data.decode("utf-8")

    # sending the file data to the preprocess function

    df = preprocess.preprocess(data)

    # fetch unique users

    user_list = df['User'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()

    # including overall,this will be responsible for showcasing the  overall chat group analysis

    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox(
        "Show analysis with respect to", user_list)

    st.title("Whats App Chat Analysis for " + selected_user)
    if st.sidebar.button("Show Analysis"):

        # getting the stats of the selected user from the stats script

        num_messages, num_words, media_omitted, links = stats.fetchstats(
            selected_user, df)

        # first phase is to showcase the basic stats like number of users,number of messages,number of media shared and all,so for that i requrire the 4 columns

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.title(num_messages)

        with col2:
            st.subheader("Total No. of Words")
            st.title(num_words)

        with col3:
            st.subheader("Total Media Shared")
            st.title(media_omitted)

        with col4:
            st.subheader("Total Links Shared")
            st.title(links)

        # finding the busiest users in the group

        if selected_user == 'Overall':

            # dividing the space into two columns
            # first col is the bar chart and the second col is the dataframe representing the

            st.subheader('Most Active Users')
            busycount, newdf = stats.fetchbusyuser(df)        
            
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                bar = ax.bar(x=busycount.index, height=busycount.values, color=["#2e8e35","#64aa5f","#93c689","#bfe2b6","#ebffe4"])
                plt.xticks(rotation='vertical', size=18)
                plt.ylabel("Number of messages", size=23)
                plt.yticks(labels=None, size=17)
                plt.bar_label(bar,label_type='edge')
                plt.grid(visible=None)
                st.pyplot(fig)

            with col2:
                st.dataframe(newdf)

        # Monthly timeline

        st.subheader("Timeline")
        time = stats.monthtimeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(time['Time'], time['Message'], color="#2e8e35", linewidth=3)
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        plt.ylabel("Number of messages", size=21)
        plt.grid(visible=None)
        st.pyplot(fig)

        # Activity maps

        st.subheader("Activity")

        col1, col2 = st.columns(2)

        with col1:

            st.write("Most Busy Day")

            busy_day = stats.weekactivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color=["#2e8e35","#64aa5f","#93c689","#bfe2b6","#ebffe4", "#ebffe4", "#ebffe4"])
            plt.xticks(rotation='vertical', size=17)
            plt.yticks(size=17)
            plt.ylabel("Number of messages", size=20)
            plt.grid(visible=None)
            plt.tight_layout()
            st.pyplot(fig)

        with col2:

            st.write("Most Busy Hour")
            busy_hour = stats.houractivitymap(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_hour.index, busy_hour.values, color="#2e8e35")
            plt.xticks(busy_hour.index, size=17)
            plt.yticks(size=17)
            plt.ylabel("Number of messages", size=20)
            plt.grid(visible=None)
            plt.tight_layout()
            st.pyplot(fig)
           
        # Word Cloud

        st.subheader('Word Cloud')
        df_img = stats.createwordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_img)
        plt.grid(visible=None)
        plt.tight_layout()
        st.pyplot(fig)

        # most common words in the chat

        st.subheader('Most commmon words')
        most_common_df = stats.getcommonwords(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color=["#ebffe4","#bfe2b6","#93c689","#64aa5f","#2e8e35"])
        #plt.xticks(rotation='vertical')
        plt.grid(visible=None)
        st.pyplot(fig)

        # Emoji Analysis

        emoji_df = stats.getemojistats(selected_user, df)
        emoji_df.columns = ['Emoji', 'Count']

        st.subheader("Emoji Analysis")

        emojicount = list(emoji_df['Count'])
        perlist = [(i/sum(emojicount))*100 for i in emojicount]
        emoji_df['Percentage use'] = np.array(perlist)
        st.dataframe(emoji_df)