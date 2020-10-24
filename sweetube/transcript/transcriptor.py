from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound


class Transcriptor:
    def __init__(self, lang='en'):
        self.lang = lang

    def fetch(self, video_id):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, [self.lang])
        except NoTranscriptFound:
            return None
        return transcript


if __name__ == '__main__':
    res = Transcriptor().fetch('X8jsijhllIA')
    print(res)
