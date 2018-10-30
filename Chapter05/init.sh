if [ ! -d "venv" ]; then
    echo --------------------
    echo Creating virtualenv
    echo --------------------
    virtualenv venv
fi
source venv/bin/activate

pip install -r requirements.txt

export FLASP_APP=main.py
if [ ! -d "migrations" ]; then
    echo --------------------
    echo INIT THE migrations folder
    echo --------------------
    export FLASK_APP=main.py; flask db init
fi
echo --------------------
echo Generate migration DDL code
echo --------------------
flask db migrate
echo --------------------
echo Run the DDL code and migrate
echo --------------------
echo --------------------
echo This is the DDL code that will be run
echo --------------------
flask db upgrade
echo --------------------
echo Generating test data
echo --------------------
python test_data.py

