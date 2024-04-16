FROM tiangolo/uwsgi-nginx-flask:python3.11
COPY requirements-versioned.txt /tmp/
COPY slexil-2.8.0-py3-none-any.whl /tmp
RUN pip install -r /tmp/requirements-versioned.txt
RUN pip install /tmp/*.whl
RUN mkdir /app/assets
COPY ./app /app
COPY assets/ /app/assets/
RUN mkdir /app/eafs
COPY eafs/ /app/eafs
#COPY /etc/nginx/nginx.conf /etc/nginx/nginx.conf_orig
#COPY nginxLongKeepAlive.conf /etc/nginx/nginx.conf
#COPY nginxLongKeepAlive.conf /tmp/






