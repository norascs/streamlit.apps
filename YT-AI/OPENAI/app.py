import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
import openai

# OpenAI API key setup
OPENAI_API_KEY = 'your_openai_api_key' 
openai.api_key = OPENAI_API_KEY

def get_video_id(url):
    """Extract the video ID from a YouTube URL."""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})', 
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except NoTranscriptFound:
        st.error("No suitable captions found for this video.")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

def summarize_text_openai(transcription):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": transcription}
            ]
        )
        summary = response['choices'][0]['message']['content']
        return summary
    except Exception as e:
        st.error(f"Error during summary: {e}")
        return None

def summarize_youtube_video(video_url):
    video_id = get_video_id(video_url)
    if not video_id:
        st.error("Invalid YouTube URL.")
        return None

    st.write(f"Extracted video ID: {video_id}")

    transcript = get_transcript(video_id)
    if transcript:
        st.write("Transcript successfully fetched.")
        return summarize_text_openai(transcript)
    else:
        st.error("No suitable captions found for this video.")
        return None

st.title("YouTube Video Summarizer")
video_url = st.text_input("Enter YouTube Video URL", "https://www.youtube.com/watch?v=zdbVtZIn9IM&t=3s&ab_channel=DwarkeshPatel")

if st.button("Summarize"):
    if video_url:
        summary = summarize_youtube_video(video_url)
        if summary:
            st.subheader("Summary")
            st.write(summary)
        else:
            st.error("Failed to fetch or summarize the transcript.")
    else:
        st.error("Please enter a valid YouTube video URL.")
