from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from pydub import AudioSegment
from pathlib import Path


"""get video transcript from id with timestamps"""
def retrieve_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)
    return transcript
