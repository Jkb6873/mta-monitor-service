#PYTHON 2
# python -m pip install --user virtualenv
# [ ! -d venv ] && virtualenv venv

#PYTHON 3
[ ! -d venv ] && python3 -m venv ./venv

# source virtualenv
source venv/bin/activate

# install packages
pip install -r requirements.txt

if [[ -f ".env" ]]; then
  source .env
fi

export FLASK_APP=app.py

if [[ $1 == "test" ]]; then
  #run tests
  pytest -v -s
else
  #start server
  python3 -m flask run
fi
