# Import file with secerts 
import secrets as sec 
# API client library
import googleapiclient.discovery
import dateutil
from numpy import minimum
import pandas as pd


# Data viz packages
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# API key
DEVELOPER_KEY = sec.API_KEY
# APP type
api_service_name = "youtube"
api_version = "v3"

# Access API client using no auth. Becuase the data that is accessed no need for credential 
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)



channel_ids = ['UCVpankR4HtoAVtYnFDUieYA','UC2Qw1dzXDBAZPwS7zm37g8g','UCOHe7b4N6URcwY2ZqpyjLbg','UC4eYXhJI4-7wSWc8UNRwD4A','UC6cvmD53Do5_wtViBfeT5Ww']


# Dataframe containing the channel statistics
def get_channel_stats(youtube, channel_ids):
  
    channel_data = [] #empty list to store returned data
    #The request tells what attributes to get from the channel data
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics', 
                id=','.join(channel_ids))
    response = request.execute() 

    #loop items and adding data to a dictionary 
    for i in range(len(response['items'])):
        data = dict(channelName = response['items'][i]['snippet']['title'],
                    subscribers = response['items'][i]['statistics']['subscriberCount'],
                    views = response['items'][i]['statistics']['viewCount'],
                    totalVideos = response['items'][i]['statistics']['videoCount'],
                    playlistId = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        channel_data.append(data)
    
    return pd.DataFrame(channel_data)


playlist_id = "PLWa4R2I19VH6mND1HUBeHJN1NMzi6VAFR"

#List of video IDs of all videos in the playlist 
def get_video_ids(youtube, playlist_id):
  
    video_ids = [] #empty list to store data

    request = youtube.playlistItems().list( 
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 50)
    response = request.execute()
    
  # 
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

   # The below code will re-run the request to overide the API limit of 50. currently the default is 5 and the max is 50 but we want to get all the video stats.    
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token)
            response = request.execute()
    
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
      
    return video_ids

video_ids = get_video_ids(youtube,playlist_id)
#len(video_ids)


def get_video_details(youtube, video_ids):
 
    all_video_info = []
    
    request = youtube.videos().list( part = "snippet, contentDetails, statistics", id=video_ids)

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute() 

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }
            video_info = {}
            video_info['video_id'] = video['id']
            # This in case of gaps in data. If the data is missing it will be null
            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)

    return pd.DataFrame(all_video_info)
video_df = get_video_details(youtube, video_ids)
print(video_df)


