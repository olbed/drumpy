rm -rf ./dist
source venv/bin/activate
pip install -U setuptools wheel twine
python setup.py bdist_wheel
twine upload dist/*
