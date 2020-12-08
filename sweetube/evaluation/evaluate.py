import csv

from tqdm import tqdm


class Evaluator:
    def __init__(self):
        csvfile = open('transcript_evaluation.csv', 'rt')
        reader = csv.DictReader(csvfile, delimiter=',')
        self.reader = list(reader)
        self.preprocess()
        self.tp = 0
        self.fp = 0
        self.fn = 0
        self.tn = 0

    def preprocess(self):
        for r in tqdm(self.reader):
            r['me'] = r['me'] == 'TRUE' if r['me'] else False
            r['model'] = r['model'] == 'TRUE' if r['model'] else False

    def evaluate(self):
        for i, r in tqdm(enumerate(self.reader)):
            t = r['me']
            p = r['model']
            if t:
                if p:
                    self.tp += 1
                else:
                    self.fn += 1

            else:
                if p:
                    self.fp += 1
                else:
                    self.tn += 1

        self.precision = self.tp / (self.tp + self.fp)
        self.recall = self.tp / (self.tp + self.fn)
        self.f = (2 * self.precision * self.recall) / (self.precision + self.recall)

        return self


if __name__ == '__main__':
    results = Evaluator().evaluate()

    print('precision:', results.precision)
    print('recall:', results.recall)
    print('f-score:', results.f)
    print(f'tp: {results.tp}, tn: {results.tn}, fp: {results.fp}, fn: {results.fn}')
