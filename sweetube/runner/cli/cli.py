from urllib.parse import urlparse, parse_qsl
import click

from sweetube.transcript import TranscriptorFailed
from sweetube.runner.cli import output
from sweetube.runner import run


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
    # Run Application
    try:
        result = run(video, only_manually, only_hate)
    except TranscriptorFailed as e:
        click.echo(e.msg, err=True)
        raise click.exceptions.Exit(-1)

    # Export output to stdout
    output_fn = getattr(output, output_format, output.unsupported)
    output_fn(result)


if __name__ == '__main__':
    main()
