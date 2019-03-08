FROM python:2.7
ADD requirements.txt /code/
WORKDIR /code
VOLUME /code
RUN pip install -r requirements.txt
ADD . /code
CMD ["uwsgi", "--http", "0.0.0.0:8000", "--wsgi-file", "run.py", "--callable", "app_dispatch"]