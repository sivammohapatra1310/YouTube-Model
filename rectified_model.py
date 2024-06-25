from googleapiclient.discovery import build
from datetime import datetime
import pandas as pd
import re
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Load pre-trained model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Use your actual API key
api_key = 'AIzaSyAUnFK5NkwZqY2D2grr72rUOIuaPOAbMaE'

youtube = build('youtube', 'v3', developerKey=api_key)

def extract_video_id(url):
    video_id = re.search(r'v=([a-zA-Z0-9_-]{11})', url)
    return video_id.group(1) if video_id else None

def check_video_validity(video_id):
    request = youtube.videos().list(part="snippet", id=video_id)
    response = request.execute()
    return response['items']

def fetch_videos(youtube, query, max_pages=5):
    videos = []
    page_token = None
    seen_video_ids = set()
    
    for _ in range(max_pages):
        search_request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=10,
            order="relevance",
            pageToken=page_token
        )
        search_response = search_request.execute()

        video_ids = [item['id']['videoId'] for item in search_response['items'] if 'videoId' in item['id']]
        video_ids = [video_id for video_id in video_ids if video_id not in seen_video_ids]
        seen_video_ids.update(video_ids)

        if not video_ids:
            break

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

def calculate_average_view_count(videos):
    view_counts = [int(video['statistics'].get('viewCount', 0)) for video in videos]
    return sum(view_counts) / len(view_counts)

def filter_videos(videos, average_view_count):
    filtered_videos = []
    for video in videos:
        published_at = datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        view_count = int(video['statistics'].get('viewCount', 0))
        if published_at.year >= 2022 or view_count >= average_view_count:
            filtered_videos.append(video)
    return filtered_videos

def rank_videos_by_view_count(videos):
    return sorted(videos, key=lambda video: int(video['statistics'].get('viewCount', 0)), reverse=True)[:10]

def generate_search_query(topic):
    prompt = f"Generate a search query for the latest and most popular videos on: {topic}"
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs,
        max_length=50,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        attention_mask=torch.ones(inputs.shape, dtype=torch.long)
    )
    query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return query

def main(youtube_url):
    video_id = extract_video_id(youtube_url)
    if video_id:
        video_data = check_video_validity(video_id)
        if video_data:
            print("The video is available.")
            print(f"Video link: https://www.youtube.com/watch?v={video_id}")
            return

        # Extract keywords from video title and generate search query using GPT-2
        print("Enter your search query:")
        topic = input("Enter topic:")
        query = generate_search_query(topic)

        videos = fetch_videos(youtube, query)
        average_view_count = calculate_average_view_count([video for video in videos if datetime.strptime(video['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').year >= 2022])
        filtered_videos = filter_videos(videos, average_view_count)
        ranked_videos = rank_videos_by_view_count(filtered_videos)

        # Create a dataset
        dataset = []
        for video in ranked_videos:
            video_info = {
                'Title': video['snippet']['title'],
                'Video ID': video['id'],
                'Views': video['statistics'].get('viewCount', 'N/A'),
                'Published At': video['snippet']['publishedAt'],
                'Video Link': f"https://www.youtube.com/watch?v={video['id']}"
            }
            dataset.append(video_info)
            print(f"Video link: {video_info['Video Link']}")

        # Save dataset to CSV
        df = pd.DataFrame(dataset)
        df.to_csv('youtube_videos_dataset.csv', index=False)
        print("Dataset saved to youtube_videos_dataset.csv")
    else:
        print("Invalid YouTube URL.")

# Example usage
youtube_url = "https://www.youtube.com/watch?v=mfKWz_i8jE0&list=PLpzy7FIRqpGD0kxI48v8QEVVZd744Phi4"
main(youtube_url)
