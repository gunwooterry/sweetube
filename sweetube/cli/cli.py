from urllib.parse import urlparse, parse_qsl

from sweetube.transcript import Transcriptor
from sweetube.detection import Detector


class CLIError(RuntimeError):
    def __init__(self, msg):
        super().__init__(msg)


def parse_url(url):
    if type(url) == str:
        url = urlparse(arg)
    if url.hostname is None:
        return arg
    if url.hostname not in ['youtube.com', 'www.youtube.com', 'm.youtube.com']:
        raise CLIError('Supplied URL is not of YouTube')
    if url.path != '/watch':
        raise CLIError('Supplied URL path is not for videos')
    qs = dict(parse_qsl(url.query))
    if 'v' not in qs:
        raise CLIError('Supplied URL query does not specify any video')
    return qs['v']


def cli(video):
    video_id = parse_url(video)

    transcriptor = Transcriptor()
    transcript_result = transcriptor.fetch(video_id)

    inverted_index = {e['text']: e for e in transcript_result}

    detector = Detector()
    detected_result = detector.detect([e['text'] for e in transcript_result])

    sorted_result = sorted(detected_result, key=lambda e: (e['label'] == 'offensive_language', -e['confidence']))

    print('type                  confidence    start time (s)    text')
    print('------------------------------------------------------------------')
    for e in filter(lambda e: e['label'] != 'neither', sorted_result):
        label = e['label']
        confidence = e['confidence']
        start_time = inverted_index[e['text']]['start']
        text = e['text']
        print(f'{label.ljust(18)}    {confidence:10.03f}    {start_time:14.02f}    {text}')


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('YouTube URL or video ID should be input as an argument.', file=sys.stderr)
    *_, arg = sys.argv
    cli(arg)
