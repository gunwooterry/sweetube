import os

from punctuator import Punctuator


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PUNCTUATOR = Punctuator(os.path.join(BASE_DIR, 'data/Demo-Europarl-EN.pcl'))
