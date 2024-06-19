from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Load pre-trained model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Example topic
topic = "Kalki"
prompt = f"Generate a search query for the latest and most popular videos on: {topic}"

# Encode the prompt
inputs = tokenizer.encode(prompt, return_tensors="pt")

# Generate response
outputs = model.generate(
    inputs,
    max_length=50,
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id,
    attention_mask=torch.ones(inputs.shape, dtype=torch.long)
)

# Decode the output
query = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(query)

from googleapiclient.discovery import build
from datetime import datetime

# Use your actual API key
api_key = 'AIzaSyAUnFK5NkwZqY2D2grr72rUOIuaPOAbMaE'

youtube = build('youtube', 'v3', developerKey=api_key)

# Generate a search query
query = "Kalki"

# Function to fetch videos
def fetch_videos(youtube, query, max_pages=5):
    videos = []
    page_token = None
    for _ in range(max_pages):
        search_request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=10,
            order="relevance",  # Use 'relevance' to get a mix of popular and relevant results
            pageToken=page_token
        )
        search_response = search_request.execute()

        # Extract video IDs
        video_ids = [item['id']['videoId'] for item in search_response['items'] if 'videoId' in item['id']]

        if not video_ids:
            break

        # Fetch video statistics
        video_request = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids)
        )
        video_response = video_request.execute()
        videos.extend(video_response['items'])

        page_token = search_response.get('nextPageToken')
        if not page_token:
            break

    return videos

# Function to calculate average view count
def calculate_average_view_count(videos):
    view_counts = [int(video['statistics'].get('viewCount', 0)) for video in videos]
    return sum(view_counts) / len(view_counts)

# Function to filter videos
def filter_videos(videos, average_view_count):
    filtered_videos = []
    for video in videos:
        published_at = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        view_count = int(video['statistics'].get('viewCount', 0))
        if published_at.year >= 2022 or view_count >= average_view_count:
            filtered_videos.append(video)
    return filtered_videos

# Function to rank videos by view count
def rank_videos_by_view_count(videos):
    print(type(sorted(videos, key=lambda video: int(video['statistics'].get('viewCount', 0)), reverse=True)[:10]))
    return  sorted(videos, key=lambda video: int(video['statistics'].get('viewCount', 0)), reverse=True)[:10]

# Fetch videos
videos = fetch_videos(youtube, query)

# Calculate average view count of videos published after 2022
average_view_count = calculate_average_view_count([video for video in videos if datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').year >= 2022])

# Filter videos based on the average view count
filtered_videos = filter_videos(videos, average_view_count)

# Rank filtered videos by view count
ranked_videos = rank_videos_by_view_count(filtered_videos)

# Print ranked videos
for video in ranked_videos:
    print(f"Title: {video['snippet']['title']}, Views: {video['statistics'].get('viewCount', 'N/A')},  At: {video['snippet']['publishedAt']}")
