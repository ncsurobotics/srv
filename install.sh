sudo mkdir /usr/local/lib/python2.7/dist-packages/srv
sudo cp -r . /usr/local/lib/python2.7/dist-packages/srv
sudo rm -f /usr/local/lib/python2.7/dist-packages/srv/*.sh

sudo cp srvStartCams.sh ~/bin/srvCamStart
sudo cp srvStartServer.sh ~/bin/srvServerStart
sudo cp srvWatch.sh ~/bin/srvWatch
sudo cp srvSwapCams.sh ~/bin/srvSwapCams

sudo chmod +x ~/bin/srvCamStart
sudo chmod +x ~/bin/srvServerStart
sudo chmod +x ~/bin/srvWatch
sudo chmod +x ~/bin/srvSwapCams
