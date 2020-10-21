from operator import itemgetter

from hatesonar import Sonar


class Detector:
    def __init__(self, pretrained=True):
        self.pretrained = pretrained
        if pretrained:
            self.model = Sonar()

    def detect(self, scripts: list):
        detections = []
        for script in scripts:
            detection = self.model.ping(text=script)
            highest_confidence = sorted(detection['classes'], key=itemgetter('confidence'), reverse=True)[0]
            detections.append([detection['text'], highest_confidence])

        return detections


if __name__ == '__main__':
    results = Detector().detect(['I hate you.', 'I love you.', "At least I'm not a nigger"])

    # print sample
    for result in results[:3]:
        print(result)
