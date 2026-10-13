.PHONY: run run-local build

# Launches the interactive decision support dashboard and evaluation pipeline
run:
	docker compose up --build

run-local:
	pip install -r requirements.txt
	python src/app.py

build:
	docker build -t apertus-track2b .
