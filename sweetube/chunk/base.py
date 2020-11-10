from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List
import requests
from tqdm import tqdm


@dataclass
class TranscriptData:
    text: str
    start: float
    duration: float

    @classmethod
    def parsedict(cls, value):
        return TranscriptData(value['text'], value['start'], value['duration'])

    @staticmethod
    def combine(arr: List['__class__']) -> '__class__':
        return TranscriptData(
            ' '.join([d.text.strip() for d in arr]),
            arr[0].start,
            sum([d.duration for d in arr]),
        )

    def split(self, sep='.'):
        texts = self.text.split(sep)
        cur = 0
        res = []
        for t in texts:
            duration = self.duration * len(t) / len(self.text)
            res.append(self.__class__(
                t.strip(),
                self.start + cur,
                duration,
            ))
            cur += duration
        return res

    def punctuate(self):
        self.text = self.text.replace('\n', ' ')
        data = {
            'text': self.text,
        }
        res = requests.post('http://bark.phon.ioc.ee/punctuator', data=data)
        texts = res.content.decode().split('.')
        cur = 0
        res = []
        for t in texts:
            duration = self.duration * len(t) / len(self.text)
            res.append(self.__class__(
                t.strip(),
                self.start + cur,
                duration,
            ))
            cur += duration
        return res


class ChunkABC(metaclass=ABCMeta):
    def chunk(self, transcripts):
        data = [TranscriptData.parsedict(t) for t in transcripts]
        return self._chunk(data)

    @abstractmethod
    def _chunk(self, data: List[TranscriptData]) -> List[TranscriptData]:
        pass


class SimpleChunk(ChunkABC):
    def __init__(self, threshold_words=15):
        self.threshold = threshold_words

    def _chunk(self, data: List[TranscriptData]) -> List[TranscriptData]:
        splitted_data = [e for d in data for e in d.split('.')]
        partitioned_data = []
        exceeded = True
        for d in splitted_data:
            if d.text.endswith(('.', '!', '?')):
                if exceeded:
                    partitioned_data.append([d])
                else:
                    partitioned_data[-1].append(d)
                exceeded = True
            else:
                if exceeded:
                    partitioned_data.append([d])
                else:
                    partitioned_data[-1].append(d)
                exceeded = self.threshold > 0 and sum(len(d.text.split(' ')) for d in partitioned_data[-1]) > self.threshold
        return [TranscriptData.combine(arr) for arr in partitioned_data]


class FineChunk(SimpleChunk):
    def __init__(self, threshold_words=15):
        super().__init__(threshold_words)

    def _chunk(self, data: List[TranscriptData]) -> List[TranscriptData]:
        result = super()._chunk(data)
        splitted_data = [e for d in tqdm(result) for e in d.punctuate()]

        self.threshold = 3
        partitioned_data = []

        for d in splitted_data:
            if len(d.text.split(' ')) > self.threshold:
                partitioned_data.append([d])
            else:  # 너무 짧은 경우만 앞이랑 이어주기
                partitioned_data[-1].append(d)
        return [TranscriptData.combine(arr) for arr in partitioned_data]
