from urllib.parse import urlparse, parse_qsl
import click

from sweetube.chunk.base import FineChunk
from sweetube.transcript import Transcriptor, TranscriptorFailed
from sweetube.detection import Detector
from sweetube.chunk import SimpleChunk
from sweetube.cli import output


def parse_url(ctx, param, value):
    url = urlparse(value)
    if url.hostname is None:
        return value
    if url.hostname not in ['youtube.com', 'www.youtube.com', 'm.youtube.com']:
        raise click.BadArgumentUsage('Supplied URL is not of YouTube')
    if url.path != '/watch':
        raise click.BadArgumentUsage('Supplied URL path is not for videos')
    qs = dict(parse_qsl(url.query))
    if 'v' not in qs:
        raise click.BadArgumentUsage('Supplied URL query does not specify any video')
    return qs['v']


@click.command()
@click.argument('video', callback=parse_url)
@click.option(
    '-m', 'only_manually', is_flag=True, default=False,
    help='Only search subscriptions manually created')
@click.option(
    '-s', '--short', '--hate', 'only_hate', is_flag=True, default=False,
    help='Only search hate speeches (and ignore offensive languages)')
@click.option(
    '-o', 'output_format', type=click.Choice(['text', 'json'], case_sensitive=False), default='text',
    help='Output format (text/json)')
def main(video, only_manually, only_hate, output_format):
    """Calculate and return hate speeches in a specific YouTube video"""
    # Fetch Transcript
    try:
        transcriptor = Transcriptor(only_manually=only_manually)
        transcript_result = transcriptor.fetch(video)
    except TranscriptorFailed as e:
        click.echo(e.msg, err=True)
        raise click.exceptions.Exit(-1)

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

    # Export output to stdout
    output_fn = getattr(output, output_format, output.unsupported)
    output_fn(sorted_result, inverted_index)


if __name__ == '__main__':
    main()
