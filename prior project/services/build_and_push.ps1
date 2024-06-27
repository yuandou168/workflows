docker-compose build
cd ipfs-service
docker push nicoja/ipfs-service2
cd ..
cd webdav-service
docker push nicoja/ipfs-service2
cd ..