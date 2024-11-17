FROM registry.zooket.ir/devops-images/python/python:3.12

ADD . /central-swagger/
WORKDIR /central-swagger

COPY ./backend /central-swagger

RUN pip config set global.index-url https://jfrog.stage-express.ir/artifactory/api/pypi/python/simple &&  \
    pip --timeout 100 install -r requirements.txt


ENV TZ=Asia/Tehran
ENV PROMETHEUS_MULTIPROC_DIR /tmp
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000","--log-level","info","--workers","4"]

