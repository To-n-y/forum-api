run:
	uvicorn main:app --reload

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
