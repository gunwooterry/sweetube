import click


def text(sorted_result, transcription_index):
    click.echo('type                  confidence    start time (s)    text')
    click.echo('------------------------------------------------------------------')
    for e in sorted_result:
        label = e['label']
        confidence = e['confidence']
        start_time = transcription_index[e['text']].start
        text = e['text']
        click.echo(f'{label.ljust(18)}    {confidence:10.03f}    {start_time:14.02f}    {text}')


def json(sorted_result, transcription_index):
    import json
    click.echo(json.dumps([
        {
            'label': e['label'],
            'confidence': e['confidence'],
            'start_time': transcription_index[e['text']].start,
            'text': e['text'],
        }
        for e in sorted_result
    ]))


def unsupported(sorted_result, transcription_index):
    click.echo('Unsupported output format', err=True)
