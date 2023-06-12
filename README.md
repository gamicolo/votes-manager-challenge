API for votes managment. Developed with Python, FastApi, Pytest, SQLALchemy, Docker

## To run the unit tests
```
pytest
```

## To run the api
```
docker build . -t votes-manager
docker run --name votes-manager-container -p 8000:8000/tcp votes-manager
```

## clean:
```
docker stop votes-manager-container
docker rm votes-manager-container
```

## OpenApi doc
```
127.0.0.1:8000
```
