from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled


class TranscriptorFailed(RuntimeError):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg


class Transcriptor:
    def __init__(self, *, lang='en', only_manually=False):
        self.lang = lang
        self.only_manually = only_manually

    def fetch(self, video_id):
        try:
            if self.only_manually:
                transcript = YouTubeTranscriptApi.list_transcripts(video_id).find_manually_created_transcript([self.lang])
            else:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, [self.lang])
        except NoTranscriptFound:
            raise TranscriptorFailed(f'Transcript does not exist in the video {video_id}')
        except TranscriptsDisabled:
            raise TranscriptorFailed(f'Transcription is disabled for the video {video_id}')
        return transcript


if __name__ == '__main__':
    res = Transcriptor().fetch('X8jsijhllIA')
    print(res)
