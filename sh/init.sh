set -x

virtualenv ./venv
source ./venv/bin/activate

pip install -r ./requirements.txt

mkdir logs

mkdir ddgcorp/migrations
touch ddgcorp/migrations/__init__.py

./manage.py makemigrations
./manage.py migrate

echo type: \"source ./venv/bin/activate\"
