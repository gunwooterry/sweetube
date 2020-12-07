init: download_punctuator
	poetry install

download_punctuator:
	gdown https://drive.google.com/uc?id=0B7BsN5f2F1fZd1Q0aXlrUDhDbnM
	mkdir -p data
	mv Demo-Europarl-EN.pcl data/

run:
	python -W ignore ./server.py
