set -x

rm -rf ./*/migrations/
rm -rf ./base.sqlite3
rm -rf ./venv
rm -rf ./logs

find ./ddgcorp -name "*.pyc" -exec rm -rf {} \;
