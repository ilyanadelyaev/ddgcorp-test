# Test-task for DDGCorp

Task manager on Django framework with REST-api and JS layout.

* Django
* React.js
* WebSokets
* Redis.io


## Init
```
[sudo] pip install virtualenv
./sh/init.sh
source venv/bin/activate
```

## Test
* pep8
* pylint
```
./sh/test.sh
```

## Run
```
c0 $ ./redis-server  # default config
c1 $ ./sh/run.sh
```

## Clean
```
deactivate
./sh/clean.sh
```
