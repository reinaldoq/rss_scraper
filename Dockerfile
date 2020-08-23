FROM python:3.6
ENV PYTHONUNBUFFERED 1
ADD . /source
WORKDIR /source
RUN pip install -r requeriments.txt
RUN export FLASK_APP=server.py
RUN LC_ALL=en_US
RUN export LC_ALL
CMD python -m flask run --host=0.0.0.0
