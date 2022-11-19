# youtube_video_stats

## Project description 

This is the first phase of an analysis tool that will allow the user to see statistics for youtube channels. Currently, the program connects to YouTube API via API Key to retrieve YouTube stats based on channel IDs. Then within that channel we can select a playlist and get details about the videos on that playlist. Program currently returns attributes such as subscriber count, views, title, description, etc. 

Based on the channel_data we can visualize Seaborn bar graphs that show us views and subscriber counts per channel_data. 

In the future the user will be able to input their own channels by the name fro command prompt. 

# Before you get Started 

To run this program you will need to install the following:
* Python 3.10 or newer. 
* pandas 
* seasborn 

To work with the Youtube API you will need to: 
* You need a Google Account to access the Google API Console, request an API key, and register your application.

* Create a project in the Google Developers Console and obtain authorization credentials so your application can submit API requests.

* After creating your project, make sure the YouTube Data API is one of the services that your application is registered to use:
    *Go to the API Console and select the project that you just registered.
    *Visit the Enabled APIs page. In the list of APIs, make sure the status is ON for the YouTube Data API v3. 






