# Test-task for DDGCorp

Task manager on Django framework with REST-api and JS layout.

* Django
* React.js
* WebSokets
* Redis.io


## Init and Add test data
```
[sudo] pip install virtualenv
./sh/init.sh
./sh/add_data.sh
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
