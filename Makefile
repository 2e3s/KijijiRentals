SHELL := /bin/bash

test:
	mypy --config-file=mypy.ini --strict ./run.py
	flake8 ./*.py --max-line-length=100
