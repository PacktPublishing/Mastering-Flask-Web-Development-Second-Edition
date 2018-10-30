Chapter 12 -  Testing Flask Apps
================================


To run the application
----------------------

```
./init.sh
source venv/bin/activate
export FLASK_APP=main.py
flask run
```

Run the tests and coverage
--------------------------

```
python run_test_server.py &
coverage run --source webapp --branch -m unittest discover
```

