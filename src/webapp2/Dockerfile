FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY requirements-versioned.txt /tmp/
COPY slexil-2.6.2-py3-none-any.whl /tmp
RUN pip install -r /tmp/requirements-versioned.txt
RUN pip install /tmp/*.whl
RUN mkdir /app/assets
COPY ./app /app
COPY assets/ /app/assets/





