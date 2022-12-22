#!/bin/bash

# [START startup_script]
cd /home/work_dir/flask-tutorial
export FLASK_APP=flaskr
flask init-db
nohup flask run -h 0.0.0.0 &
# [END startup_script]
