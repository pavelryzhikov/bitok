#install
virtualenv -p /usr/bin/python3.4 python3.4-env
pip install -r requirements.txt


#commit
pip freeze > requirements.txt

