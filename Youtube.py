import googleapiclient.discovery
import pymongo
import pandas as pd
import pymysql
import streamlit as st
from datetime import datetime, timedelta
from isodate import parse_duration

#Api key connection
def api_connect():
    api_key="AIzaSyDakPgQp5JaDdDEzmah0dFTehXb1Abu1gQ"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)
    return youtube
youtube=api_connect()

#get channels info
def get_channel_info(channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()
    
    for i in response['items']:
        data=dict(Channel_Name=i['snippet']['title'],
                  Channel_Id=i['id'],
                  Subscribers=i['statistics']['subscriberCount'],
                  Views=i['statistics']['viewCount'],
                  Total_Videos=i['statistics']['videoCount'],
                  Channel_Description=i['snippet']['description'],
                  Playlist_Id=i['contentDetails']['relatedPlaylists']['uploads'])
    return data

#get video id's
def get_videos_ids(channel_id):
    video_ids=[]
    response=youtube.channels().list(id=channel_id,
                                     part='contentDetails').execute()
    Playlist_Id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token=None
    while True:
        response1=youtube.playlistItems().list(part='snippet',
                                           playlistId=Playlist_Id,
                                               maxResults=50,
                                               pageToken=next_page_token).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=response1.get('nextPageToken')
    
        if next_page_token is None:
            break
    return video_ids

#get video info
def get_video_info(video_ids):
    video_data=[]
    for video_id in video_ids:                  #yt-api ref 
        request=youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id)
        response=request.execute()

        for item in response["items"]:         #(to get specified details here we used nested for loop)
            data=dict(Channel_Name=item["snippet"]["channelTitle"],
                      Channel_Id=item['snippet']['channelId'],
                      Video_Id=item['id'],
                      Title=item['snippet']['title'],
                      Tags=" ".join(item['snippet'].get('tags',["NA"])),
                      Thumbnail=item['snippet']['thumbnails']['default']['url'],
                      Description=item['snippet'].get('description'),
                      Published=item['snippet']['publishedAt'],
                      Duration=item['contentDetails']['duration'],
                      Views=item['statistics'].get('viewCount'),
                      Likes=item['statistics'].get('likeCount'),
                      Comments=item['statistics'].get('commentCount'),
                      Favorite_Count=item['statistics']['favoriteCount'],
                      Definition=item['contentDetails']['definition'],
                      Captions_Status=item['contentDetails']['caption'])
            video_data.append(data)
    return video_data

#get comment info
def get_comment_info(video_ids):
    Comment_data=[]
    try:
        for video_id in video_ids:
            request=youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,maxResults=50)
            response=request.execute()

            for item in response['items']:
                data=dict(Comment_Id=item['snippet']['topLevelComment']['id'],
                          Video_Id=item['snippet']['topLevelComment']['snippet']['videoId'],
                          Comment_Text=item['snippet']['topLevelComment']['snippet']['textDisplay'],
                          Comment_Author=item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                          Comment_Published_Date=item['snippet']['topLevelComment']['snippet']['publishedAt'])

                Comment_data.append(data)
    except:
        pass
    return Comment_data

#upload to mongoDB
client=pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mydb= client["YotubeData"]

def channel_details(channel_id):
    chl_details=get_channel_info(channel_id)
    vid_ids=get_videos_ids(channel_id)
    vid_details=get_video_info(vid_ids)
    cmt_details=get_comment_info(vid_ids)

    collection1=mydb["channel_details"]
    collection1.insert_one({"channel_information":chl_details,
                            "video_information":vid_details,
                           "comment_information":cmt_details})
    
    return "upload completed successfully"

#Mysql con
myconnection = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='youtube_data')
cur = myconnection.cursor()

# Channel Table Creation           
def channels_table(channel_name_s):
    myconnection = pymysql.connect(host = '127.0.0.1',user='root',password='Prajith581998@',database='youtube_data')
    cur = myconnection.cursor()
    
    create_query='''create table if not exists channels(Channel_Name varchar(100),
                                            Channel_Id varchar(100) primary key,Subscribers int,
                                            Channel_Views int,Total_Videos int,Channel_Description text,
                                            Playlist_Id varchar(100))'''
    cur.execute(create_query)
    myconnection.commit()
    
        
    single_channel_detail=[]
    mydb= client["YotubeData"]
    collection1=mydb["channel_details"]
    for chl_data in collection1.find({"channel_information.Channel_Name": channel_name_s},{"_id":0}):
        single_channel_detail.append(chl_data["channel_information"])    
    df_single_channel_detail=pd.DataFrame(single_channel_detail)
    
    for index,row in df_single_channel_detail.iterrows():                  #here we inserted sql col names
        insert_query='''insert into channels(Channel_Name,Channel_Id,Subscribers,Channel_Views,
                                             Total_Videos,Channel_Description,Playlist_Id)
                                             values(%s,%s,%s,%s,%s,%s,%s)'''

                                                    #here we inserted df col names
        values=(row['Channel_Name'],row['Channel_Id'],row['Subscribers'],    
                row['Views'],row['Total_Videos'],row['Channel_Description'],row['Playlist_Id'])
        
        try:
            cur.execute(insert_query,values)
            myconnection.commit()
        except:
            exists= f"Given Channel Name {channel_name_s} is already exists"
            return exists
            
# Video Table creation
def videos_table(channel_name_s):
    myconnection = pymysql.connect(host = '127.0.0.1',user='root',password='Prajith581998@',database='youtube_data')
    cur = myconnection.cursor()

    create_query='''create table if not exists videos(Channel_Name varchar(100),Channel_Id varchar(100),Video_Id varchar(100) primary key,
                                        Title varchar(100),Tags text,Thumbnail varchar(200),Description text,
                                        Published varchar(50),Duration Time,Views bigint,Likes bigint,
                                        Comments int,Favorite_Count int,Definition varchar(200),Captions_Status varchar(200))'''
    cur.execute(create_query)
    myconnection.commit()

    single_video_detail=[]
    mydb= client["YotubeData"]
    collection1=mydb["channel_details"]
    for chl_data in collection1.find({"channel_information.Channel_Name": channel_name_s},{"_id":0}):
        single_video_detail.append(chl_data["video_information"])
    df_single_video_detail=pd.DataFrame(single_video_detail[0])


    for index, row in df_single_video_detail.iterrows():
        # Parse ISO 8601 duration string to timedelta
        duration = parse_duration(row['Duration'])

        # Convert timedelta to seconds
        duration_seconds = duration.total_seconds()

        # Calculate hours, minutes, and seconds
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)

        # Format duration as HH:MM:SS for MySQL TIME data type
        duration_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)

        # Define the SQL insert query
        insert_query = '''insert into videos(Channel_Name, Channel_Id, Video_Id, Title, Tags,
                                             Thumbnail, Description, Published, Duration, Views,
                                             Likes, Comments, Favorite_Count, Definition, Captions_Status)
                          values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        # Define the values to be inserted into the database
        values = (row['Channel_Name'], row['Channel_Id'], row['Video_Id'], row['Title'], row['Tags'],    
                  row['Thumbnail'], row['Description'], row['Published'], duration_time, row['Views'],
                  row['Likes'], row['Comments'], row['Favorite_Count'], row['Definition'], row['Captions_Status'])

        # Execute the SQL insert query
        cur.execute(insert_query, values)
        myconnection.commit()
        
# Comment Table Creation
def comments_table(channel_name_s):
    myconnection = pymysql.connect(host='127.0.0.1', user='root', password='Prajith581998@', database='youtube_data')
    cur = myconnection.cursor()

    create_query = '''create table if not exists comments (Comment_Id VARCHAR(100) PRIMARY KEY,
                        Video_Id VARCHAR(100),Comment_Text TEXT,
                        Comment_Author VARCHAR(100),Comment_Published_Date VARCHAR(100))'''
    cur.execute(create_query)
    myconnection.commit()
    
    single_comments_detail=[]
    mydb= client["YotubeData"]
    collection1=mydb["channel_details"]
    for chl_data in collection1.find({"channel_information.Channel_Name": channel_name_s},{"_id":0}):
        single_comments_detail.append(chl_data["comment_information"])
    df_single_comments_detail=pd.DataFrame(single_comments_detail[0])
            
            
    for index, row in df_single_comments_detail.iterrows():
        insert_query = '''INSERT INTO comments (Comment_Id, Video_Id, Comment_Text, Comment_Author, Comment_Published_Date)
                          VALUES (%s, %s, %s, %s, %s)'''

        values = (row['Comment_Id'], row['Video_Id'], row['Comment_Text'], row['Comment_Author'], row['Comment_Published_Date'])
        
        cur.execute(insert_query, values)
        myconnection.commit()
        
def tables(single_channel):
    exists= channels_table(single_channel)
    if exists:
        return exists
    else:
        videos_table(single_channel)
        comments_table(single_channel)
    
    return "Tables Created Successfully"

def show_channels_table():
    ch_list=[]                                     
    mydb= client["YotubeData"]
    collection1=mydb["channel_details"]
    for chl_data in collection1.find({},{"_id":0,"channel_information":1}):
        ch_list.append(chl_data['channel_information'])
    df=st.dataframe(ch_list)
    
    return df

def show_videos_table():
    vid_list=[]
    mydb= client["YotubeData"]
    collection1=mydb["channel_details"]
    for vid_data in collection1.find({},{"_id":0,"video_information":1}):
        for i in range(len(vid_data["video_information"])):
            vid_list.append(vid_data["video_information"][i])
    df1=st.dataframe(vid_list)
    
    return df1

def show_comments_table():
    com_list=[]                                     
    mydb= client["YotubeData"]
    collection1=mydb["channel_details"]
    for com_data in collection1.find({},{"_id":0,"comment_information":1}):
        for i in range(len(com_data["comment_information"])):
            com_list.append(com_data["comment_information"][i])
    df2=st.dataframe(com_list)
    
    return df2

#StreamLit
st.title(":blue[YOUTUBE DATA HAVERSTING]")
channel_id=st.text_input("Enter the Channel ID")

if st.button("Get data"):
    ch_ids=[]
    mydb= client["YotubeData"]
    collection1=mydb["channel_details"]
    
    for ch_data in collection1.find({},{"_id":0,"channel_information":1}):
        ch_ids.append(ch_data["channel_information"]["Channel_Id"])
    
    if channel_id in ch_ids:
        st.success("Channel details already exsists")
    
    else:
        insert=channel_details(channel_id)
        st.success(insert)

all_channels=[]
mydb= client["YotubeData"]
collection1=mydb["channel_details"]
for chl_data in collection1.find({},{"_id":0,"channel_information":1}):
    all_channels.append(chl_data['channel_information']['Channel_Name'])

unique_channel=st.selectbox("Select the Channel",all_channels)

if st.button("Migrate Data"):
    Table=tables(unique_channel)
    st.success(Table)
    
#SQL Connection
myconnection = pymysql.connect(host = '127.0.0.1',user='root',password='Prajith581998@',database='youtube_data')
cur = myconnection.cursor()

question=st.selectbox("Select any question to get insights",
                      ("1.name all the videos and channel name",
                      "2.channels with most number of videos",
                      "3.top 10 most viewed videos and their respective channels",
                      "4.comments in each video, and their video names",
                      "5.videos with highest likes, and their channel names",
                      "6.number of likes for each video",
                      "7.total number of views for each channel",
                      "8.names of all the channels that have published videos in the year 2022",
                      "9.average duration of all videos in each channel",
                      "10.videos have the highest number of comments"))


if question == '1.name all the videos and channel name':
    query1 = "select Title as videos, Channel_Name as ChannelName from videos;"
    cur.execute(query1)
    myconnection.commit()
    t1=cur.fetchall()
    st.write(pd.DataFrame(t1, columns=["Video Title","Channel Name"]))

elif question == '2.channels with most number of videos':
    query2 = "select Channel_Name as ChannelName,Total_Videos as NO_Videos from channels order by Total_Videos desc;"
    cur.execute(query2)
    myconnection.commit()
    t2=cur.fetchall()
    st.write(pd.DataFrame(t2, columns=["Channel Name","No Of Videos"]))

elif question == '3.top 10 most viewed videos and their respective channels':
    query3 = '''select Views as views , Channel_Name as ChannelName,Title as VideoTitle from videos 
                        where Views is not null order by Views desc limit 10;'''
    cur.execute(query3)
    myconnection.commit()
    t3 = cur.fetchall()
    st.write(pd.DataFrame(t3, columns = ["views","channel Name","video title"]))

elif question == '4.comments in each video, and their video names':
    query4 = "select Comments as No_comments ,Title as VideoTitle from videos where Comments is not null;"
    cur.execute(query4)
    myconnection.commit()
    t4=cur.fetchall()
    st.write(pd.DataFrame(t4, columns=["No Of Comments", "Video Title"]))

elif question == '5.videos with highest likes, and their channel names':
    query5 = '''select Title as VideoTitle, Channel_Name as ChannelName, Likes as LikesCount from videos 
                       where Likes is not null order by Likes desc;'''
    cur.execute(query5)
    myconnection.commit()
    t5 = cur.fetchall()
    st.write(pd.DataFrame(t5, columns=["video Title","channel Name","like count"]))

elif question == '6.number of likes for each video':
    query6 = '''select Likes as likeCount,Title as VideoTitle from videos;'''
    cur.execute(query6)
    myconnection.commit()
    t6 = cur.fetchall()
    st.write(pd.DataFrame(t6, columns=["like count","video title"]))

elif question == '7.total number of views for each channel':
    query7 = "select Channel_Name as ChannelName, Channel_Views as Channelviews from channels;"
    cur.execute(query7)
    myconnection.commit()
    t7=cur.fetchall()
    st.write(pd.DataFrame(t7, columns=["channel name","total views"]))

elif question == '8.names of all the channels that have published videos in the year 2022':
    query8 = '''select Title as Video_Title, Published as VideoRelease, Channel_Name as ChannelName from videos 
                where extract(year from Published) = 2022;'''
    cur.execute(query8)
    myconnection.commit()
    t8=cur.fetchall()
    st.write(pd.DataFrame(t8,columns=["Name", "Video Publised On", "ChannelName"]))

elif question == '9.average duration of all videos in each channel':
    query9 =  "SELECT Channel_Name as ChannelName, AVG(Duration) AS average_duration FROM videos GROUP BY Channel_Name;"
    cur.execute(query9)
    myconnection.commit()
    t9=cur.fetchall()
    t9 = pd.DataFrame(t9, columns=['ChannelTitle', 'Average Duration'])
    T9=[]
    for index, row in t9.iterrows():
        channel_title = row['ChannelTitle']
        average_duration = row['Average Duration']
        average_duration_str = str(average_duration)
        T9.append({"Channel Title": channel_title ,  "Average Duration": average_duration_str})
    st.write(pd.DataFrame(T9))

elif question == '10.videos have the highest number of comments':
    query10 = '''select Title as VideoTitle, Channel_Name as ChannelName, Comments as Comments from videos 
                       where Comments is not null order by Comments desc;'''
    cur.execute(query10)
    myconnection.commit()
    t10=cur.fetchall()
    st.write(pd.DataFrame(t10, columns=['Video Title', 'Channel Name', 'NO Of Comments']))