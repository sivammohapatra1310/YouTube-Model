# YouTube-Model
YouTube Model to sort videos by their relevance.

# YouTube Video Fetcher and Filter
This project fetches the latest and most popular YouTube videos on a specified topic, filters them based on their view count, and ranks them. The project uses the transformers library to generate search queries and the googleapiclient library to interact with the YouTube Data API.

# Features
Generates search queries using a pre-trained GPT-2 model.
Fetches videos from YouTube based on the generated query.
Calculates the average view count of videos published after 2022.
Filters videos to only include those with a view count above the average or published after 2022.
Ranks the filtered videos by view count and prints the top 10 results.

# Prerequisites
Python 3.7 or higher
YouTube Data API key
