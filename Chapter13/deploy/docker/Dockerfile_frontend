FROM tiangolo/uwsgi-nginx:python3.6

# Create and set directory where the code will live
RUN mkdir /srv/app
WORKDIR /srv/app

# Copy our code
COPY . .
# Install all python packages required
RUN pip install -r requirements.txt
RUN sh install_flask_youtube.sh

# Setup NGINX and uWSGI
COPY ./deploy/uwsgi.ini /etc/uwsgi/uwsgi.ini
ENV NGINX_WORKER_OPEN_FILES 2048
ENV NGINX_WORKER_CONNECTIONS 2048
ENV LISTEN_PORT 80

EXPOSE 80
