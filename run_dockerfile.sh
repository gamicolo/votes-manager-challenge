docker stop votes-manager-container
docker rm votes-manager-container

docker build . -t votes-manager
docker run --name votes-manager-container -p 8000:8000/tcp votes-manager
