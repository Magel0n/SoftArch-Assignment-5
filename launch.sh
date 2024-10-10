#!/bin/bash

cd ./shared
python3 -m pip install grpcio grpcio_tools 
python3 -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. ./xee.proto
sudo apt-get install python3-tk -y

# A mongoDB preparation
#rm -rf /var/lib/mongodb
#rm -rf /tmp/mongodb-27017.sock
curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu
jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install mongodb-org -y

sudo mkdir -p /var/lib/mongodb
sudo systemctl restart mongod
sudo service mongod start
sudo chown -R mongodb:mongodb /var/lib/mongodb
sudo chown mongodb:mongodb /tmp/mongodb-27017.sock
sudo service mongod restart

python3 ../authenticator/server.py &
pid1="$!"
python3 ../like_handler/server.py &
pid2="$!"
python3 ../xeet_poster/server.py &
pid3="$!"
python3 ../xeet_retriever/server.py &
pid4="$!"

python3 ../app/app.py


echo "Do you need to save posts for future launching?(Y/N)"
read ANS
if [ "$ANS" = "Y" ] || [ "$ANS" = "y" ]
then
    echo "Saved"
else
	echo "Removing..."
	sudo rm -rf /var/lib/mongodb
	sudo mkdir -p /var/lib/mongodb
fi



echo "Killing background processes..."
kill $pid1
kill $pid2
kill $pid3
kill $pid4
echo "Done"

