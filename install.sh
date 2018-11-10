sudo mkdir /usr/local/lib/python2.7/dist-packages/srv
sudo cp -r . /usr/local/lib/python2.7/dist-packages/srv
sudo rm -f /usr/local/lib/python2.7/dist-packages/srv/*.sh

sudo cp srvStartCams.sh ~/bin/srvStartCams
sudo cp srvStartServer.sh ~/bin/srvStartServer
sudo cp srvWatch.sh ~/bin/srvWatch

sudo chmod +x ~/bin/srvStartCams
sudo chmod +x ~/bin/srvStartServer
sudo chmod +x ~/bin/srvWatch
