FROM python:3

WORKDIR /todo_app

COPY requirements.txt /todo_app/
RUN pip install --upgrade pip && pip install -r requirements.txt
