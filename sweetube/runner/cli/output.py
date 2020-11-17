import click


def text(result):
    click.echo('type                  confidence    start time (s)    text')
    click.echo('------------------------------------------------------------------')
    for e in result:
        label = e['label']
        confidence = e['confidence']
        start_time = e['start_time']
        text = e['text']
        click.echo(f'{label.ljust(18)}    {confidence:10.03f}    {start_time:14.02f}    {text}')


def json(result):
    import json
    click.echo(json.dumps(result))


def unsupported(sorted_result, transcription_index):
    click.echo('Unsupported output format', err=True)
