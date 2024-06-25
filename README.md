# YouTube Video Validator and Recommender for Educational Websites

# Why this model?
* Suppose you want to study a particular topic.
* You go to ChatGPT and ask it "Give me a youtube video on a certain topic"
* Surprisingly, the output given by ChatGPT, or many other AI chatbots are outdated.
* The youtube video link doesn't exist in many cases.
* This model primarily checks if a youtube link is available or not using Google API and Python.
* If the video is unavailable, this uses pretrained LLMs like GPT2 model from transformers library to fetch relevant data.
  
# Description

This Python script integrates with the Google API and pretrained language models (LLMs) to provide robust video validation and recommendation features for educational websites. Key functionalities include checking video availability, generating search queries based on user-provided topics, and ranking videos by relevance and popularity. The system ensures efficient integration and enhances educational content delivery by providing users with curated video recommendations.

# Features
* Video Validation: Verifies the availability of YouTube videos using the Google API.
Keyword-Based Search: Dynamically generates search queries using pretrained language models (LLMs) to fetch relevant educational videos.
* Enhanced Integration: Seamless integration with educational platforms for optimized content delivery.
Data Management: Compiles video metadata into a structured dataset and exports it to CSV format for further analysis or integration.


# Code Overview
* Google API Integration: Utilizes the YouTube Data API v3 for video searches and metadata retrieval.
* Pretrained LLMs: Implements a pretrained GPT-2 model to generate contextually relevant search queries based on user input.
* Pandas for Data Handling: Manages and exports video information using the Pandas library for structured dataset creation.
  
# Example Usage
To use this script, ensure you have Python installed along with the required dependencies listed in requirements.txt. Use your actual Google API key.


youtube_url = "https://www.youtube.com/watch?v=mfKWz_i8jE0&list=PLpzy7FIRqpGD0kxI48v8QEVVZd744Phi4"
main(youtube_url)
Installation
Clone the repository:
Install dependencies:


Acknowledgments
This project utilizes the Google API and Hugging Face Transformers library.
Inspired by the need for enhanced educational content delivery through automated video recommendation systems.
