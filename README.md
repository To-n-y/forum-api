# Forum API

[![Code checks](https://github.com/To-n-y/forum-api/actions/workflows/checks.yml/badge.svg)](https://github.com/To-n-y/forum-api/actions/workflows/checks.yml)

This project uses: **Python**, **FastAPI** and **SQLAlchemy**

## Installing application
First you should create env folder using commands:

```shell script
mkdir project
cd project
python -m venv env
cd env
cd Scripts
activate.bat
```

To install the application use following commands:
```shell script
cd..
cd..
python -m pip install --upgrade pip
git clone https://github.com/To-n-y/forum-api.git
pip install -r requirements.txt
```

## Environment configuration

**.env** file is already added

## Running the application in dev mode

You can run your application in dev mode that enables live coding using:
```shell script
uvicorn app.main:app
```
## Using Docker to run an App
First your should mount the database, go to Docker and then Settings -> Resources -> FileSharing. Add project folder and click Apply & Restart
To run an app using Docker, you need to run Docker containers by typing simple command:
```
docker-compose up
```
Now you can access the app at http://127.0.0.1:8000
