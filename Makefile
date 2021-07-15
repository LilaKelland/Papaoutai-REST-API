install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m unittest tests.unit.models.test_session_model
	python -m unittest tests.integration.models.test_session_model


format:
	black *.py

lint:
	pylint --disable=R,C papaoutai.py

all: install lint test