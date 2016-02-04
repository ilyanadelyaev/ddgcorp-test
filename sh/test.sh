set -x

./manage.py test -v 2

pep8 ./ddgcorp

pylint  --errors-only ./ddgcorp
