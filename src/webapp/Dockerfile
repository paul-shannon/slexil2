FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY requirements-versioned.txt /tmp/
COPY slexil_package-2.3.14-py3-none-any.whl /tmp
RUN pip install -r /tmp/requirements-versioned.txt
RUN pip install /tmp/slexil_package-2.3.14-py3-none-any.whl
WORKDIR /app
RUN mkdir /app/assets
COPY main.py /app/
COPY assets/ /app/assets/




