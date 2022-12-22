#!/bin/bash

# [START startup_script]
sudo apt-get update
sudo apt-get install -y python3 python3-pip git

mkdir /home/work_dir
cd /home/work_dir

curl http://metadata/computeMetadata/v1/instance/attributes/vm2-script -H "Metadata-Flavor: Google" > vm2-script.sh
curl http://metadata/computeMetadata/v1/instance/attributes/vm1-pyscript -H "Metadata-Flavor: Google" > vm1-pyscript.py

pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

python3 vm1-pyscript.py
# [END startup_script]
