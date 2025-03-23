from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(question):
    video_url = question.replace("summarize video", "").strip()
    try:
        video_id = video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text=""
        for entry in transcript:
            text += entry["text"] + " "
        return text
    except Exception as e:
        return str (e)

     