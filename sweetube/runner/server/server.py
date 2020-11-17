from flask import Flask, request

from sweetube.runner import run
from sweetube.transcript import TranscriptorFailed

app = Flask(__name__)


@app.route('/videos/<video_id>')
def calculate(video_id):
    only_manually = request.args.get('type') == 'manual'
    only_hate = request.args.get('filter') == 'hate'
    try:
        result = run(video_id, only_manually, only_hate)
    except TranscriptorFailed as e:
        return {"message": e.msg}, 400
    return {"data": result}
