![flask-python](https://user-images.githubusercontent.com/61613314/127002007-406ce046-46d4-4eed-95fd-6aa255b502e9.png)

![todo](https://user-images.githubusercontent.com/61613314/127002129-4874194b-11f9-4380-b5bb-4af3be1c0b29.gif)

# TODO application
This is an application built with Flask

# Overveiw
What this application implements is as follows.
- registering a TODO list(create, update, delete)
- simple deployment

# Usage
## generate
if debug
```
$ python main.py
```
and access 127.0.0.1:8080

if deploy
```
$ docker-compose up --build
```
and access port 80(HTTP)

# Requirements
- Python 3.7.7
- Flask 1.1.2
- SQLAlchemy 1.3.20
- gunicorn 20.0.4
- jquery 3.4.1
- bootstrap 4.5

# Author
Jumpei Motohashi

# Licence
no licence!! Feel free to use it!!