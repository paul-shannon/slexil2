FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN pip install update git+https://github.com/paul-shannon/slexil2
WORKDIR /app
RUN mkdir /app/assets
COPY main.py /app/
COPY assets/ /app/assets/




