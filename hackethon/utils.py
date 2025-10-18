import re

def youtube_video_id(url):
    """Extracts the YouTube video ID from a URL."""
    if not url:
        return None
    # Regex to find the video ID from various YouTube URL formats
    regex = r"(?:https?://)?(?:www\.)?(?:youtube\.com/(?:[^/\n\s]+/\S+/|watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None
