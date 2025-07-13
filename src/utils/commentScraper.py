from googleapiclient.errors import HttpError
import pandas as pd 

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

def comments_df(yt_client, vid_id): 
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
     
    df = pd.DataFrame(comments)

    return df