FROM tiangolo/uwsgi-nginx-flask:python3.11
#FROM tiangolo/meinheld-gunicorn-flask
COPY requirements-versioned.txt /tmp/
COPY slexil-2.9.0-py3-none-any.whl /tmp
RUN pip install -r /tmp/requirements-versioned.txt
RUN pip install /tmp/*.whl
RUN mkdir /app/assets
COPY ./app /app
COPY assets/ /app/assets/
RUN mkdir /app/eafs
RUN mkdir /app/PROJECTS/timingTest
COPY eafs/ /app/eafs
COPY eafs/4EthelAnita230503Slexil.eaf /app/PROJECTS/timingTest/
