from . import commentScraper
from googleapiclient.discovery import build 
import sys
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Google API Key
load_dotenv()
api_key = os.getenv("YOUTUBE_API_KEY")

# User input
#if len(sys.argv) != 2:
#    print("Add a video ID after the script name")
#    sys.exit(1)
    
#vid_id = sys.argv[1]

yt_client = build("youtube", "v3", developerKey=api_key)

def get_score(vid_id, client=yt_client):
    comment_df = commentScraper.comments_df(client,vid_id).sort_values(by="Number of Likes", ascending=False)[:100].drop_duplicates()

    tokenizer = AutoTokenizer.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'model')
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)
    model.eval()

    text = comment_df["Comment"].tolist()

    # Run inference
    inputs = tokenizer(text, return_tensors="pt",padding=True, truncation=True)

    with torch.no_grad():
        logits = model(**inputs).logits
        prediction = torch.argmax(logits, dim=1)

    comment_df["Predicted_class"] = prediction.numpy()
    return comment_df
