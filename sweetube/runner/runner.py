import csv

from sweetube.chunk.base import FineChunk
from sweetube.transcript import Transcriptor
from sweetube.detection import Detector


def run(video, only_manually, only_hate, get_csv=False):
    """Calculate and return hate speeches in a specific YouTube video"""
    # Fetch Transcript
    transcriptor = Transcriptor(only_manually=only_manually)
    transcript_result = transcriptor.fetch(video)

    # Chunk Transcript
    transcript_result = FineChunk(threshold_words=30).chunk(transcript_result)

    inverted_index = {e.text: e for e in transcript_result}

    # Detect hate speeches
    detector = Detector()
    detected_result = detector.detect([e.text for e in transcript_result])

    if get_csv:
        f = open(f'output_{video}.csv', 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        wr.writerow(['Video ID', 'model', 'me', 'timestamp', 'transcript'])

    # Filter and sort results
    filtered_result = []
    for e in detected_result:
        detected = False

        if e['label'] == 'hate_speech' and e['confidence'] > 0.6:
            detected = True

        if not only_hate:
            if e['label'] == 'offensive_language' and e['confidence'] > 0.6:
                detected = True
            elif '__' in e['text']:
                e['label'] = 'offensive_language'
                detected = True

        if detected:
            filtered_result.append(e)

        if get_csv:
            wr.writerow([video, detected, None, inverted_index[e['text']].start, e['text']])

    if get_csv:
        f.close()

    sorted_result = sorted(filtered_result, key=lambda e: (e['label'] == 'offensive_language', -e['confidence']))

    # Return Output
    return [
        {
            'label': e['label'],
            'confidence': e['confidence'],
            'start_time': inverted_index[e['text']].start,
            'text': e['text'],
        }
        for e in sorted_result
    ]
