from datetime import datetime

from flask import Flask, request, jsonify

from sweetube.runner import run
from sweetube.transcript import TranscriptorFailed

app = Flask(__name__)


@app.route('/videos/<video_id>')
def calculate(video_id):
    only_manually = request.args.get('type') == 'manual'
    only_hate = request.args.get('filter') == 'hate'
    get_csv = request.args.get('csv') is not None
    try:
        result = run(video_id, only_manually, only_hate, get_csv)
    except TranscriptorFailed as e:
        return {'message': e.msg}, 400
    return jsonify({'data': result})

@app.route('/feedback', methods=['POST'])
def feedback():
    from pprint import pprint
    video_id = request.json['video_id']
    is_valid = request.json['is_valid']
    phrase = request.json['phrase']
    now = datetime.now().isoformat()
    with open('./feedback.csv', 'a+') as f:
        f.write(f'{now},{video_id},{is_valid},{phrase}\n')
    return jsonify({"status": "ok"})
