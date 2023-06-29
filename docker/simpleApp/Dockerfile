FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
WORKDIR /app
COPY ./app /app/



