FROM ubuntu
RUN  apt-get update && \
     apt-get install -y supervisor python3-pip python3-dev libmysqlclient-dev mysql-client
RUN mkdir /srv/app
WORKDIR /srv/app
COPY . .
RUN pip3 install -r requirements.txt
RUN sh install_flask_youtube.sh

COPY ./deploy/supervisor_worker.conf /etc/supervisor/conf.d/celery_worker.conf
COPY ./deploy/docker/worker_entrypoint.sh .
ENTRYPOINT ["sh", "./worker_entrypoint.sh"]
