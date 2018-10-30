DIR=/Users/daniel.gaspar/workspace/python/mastering_flask_v2/New_Code/Chapter_11/chapter_11/Flask-YouTube
pushd $DIR
pip uninstall flask-youtube
python setup.py build
python setup.py install
popd

