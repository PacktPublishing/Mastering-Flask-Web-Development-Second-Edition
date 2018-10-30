Chapter 9 - Creating Asynchronous Tasks with Celery
===================================================


To run the application
----------------------

```
./init.sh
source venv/bin/activate
export FLASK_APP=main.py
flask run
```


Run RabbitMQ
------------

```
docker build -t blog-rmq .
docker run -d -p 15672:15672 -p 5672:5672 blog-rmq
```


Run celery worker
-----------------

```
celery -A celery_runner worker -l info
```
