from sweetube.chunk.base import FineChunk
from sweetube.transcript import Transcriptor
from sweetube.detection import Detector


def run(video, only_manually, only_hate):
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

    # Filter and sort results
    filtered_result = [
        e for e in detected_result
        if (e['label'] not in [
            'neither',
            *(['offensive_language'] if only_hate else [])
        ]) and e['confidence'] > 0.6
    ]
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
