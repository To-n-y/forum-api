test:
	pytest -s -v

.PHONY: test

run:
	uvicorn app.main:app --reload

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
