from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError
import pandas as pd 
import sys
from dotenv import load_dotenv
import os

# Google API Key
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")

# User input
if len(sys.argv) != 2:
    print("Add a video ID after the script name")
    sys.exit(1)
    
vid_id = sys.argv[1]

yt_client = build("youtube", "v3", developerKey=api_key)

def get_comments(client, video_id, token=None):
    try:
        response = (client.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            textFormat = "plainText",
            maxResults = 100,
            pageToken = token
            ).execute())
        return response
    except HttpError as e:
        print(e.resp.status)
        return None
    except Exception as e:
        print(e)
        return None
    
comments = []
next = None

# Put comments data into comments list initialized above
while True:
    resp = get_comments(yt_client, vid_id, next)
    
    if not resp:
        break
    
    for i in resp["items"]:
        snip = i['snippet']['topLevelComment']['snippet']
        comments.append({
            "Author":snip["authorDisplayName"],
            "Comment":snip["textDisplay"],
            "Number of Likes":snip["likeCount"]
            })
        
    next = resp.get("nextPageToken")
    if not next:
        break
     
print(f"Total Comments fetched:{len(comments)}")
df = pd.DataFrame(comments)

# Only Keep a maximum of 1000 comments for analysis, sorted by likes count
df = df.sort_values(by="Number of Likes", ascending=False)[:1000].drop_duplicates()

print(df.head())
