#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth
import google.oauth2.service_account as service_account

#
# Use Google Service Account - See https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#module-google.oauth2.service_account
#

credentials = service_account.Credentials.from_service_account_file(filename=os.path.join(os.path.dirname(__file__), 'service-credentials.json'))
project = 'dcsclab5-365301'
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
zone = 'us-west1-b'

def wait_for_operation(operation):
    print('\tWaiting for operation to finish...', end='')
    while True:
        result = service.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            if 'error' in result:
                raise Exception(result['error'])
            print('done!')
            return result
        time.sleep(1)

def list_instances():
    result = service.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

def create_instance_1(name):
    # get the os image
    image_response = service.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2204-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    
    # get all files as metadata strings
    vm1_script = open(os.path.join(os.path.dirname(__file__), 'vm1-script.sh'), 'r').read()
    vm1_pyscript = open(os.path.join(os.path.dirname(__file__), 'vm1-pyscript.py'), 'r').read()
    vm2_script = open(os.path.join(os.path.dirname(__file__), 'vm2-script.sh'), 'r').read()

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'lab5-294@dcsclab5-365301.iam.gserviceaccount.com',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write',
                'https://www.googleapis.com/auth/compute'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [
                {
                    'key': 'startup-script',
                    'value': vm1_script
                }, 
                {
                    'key': 'vm1-pyscript',
                    'value': vm1_pyscript
                }, 
                {
                    'key': 'vm2-script',
                    'value': vm2_script
                }
            ]
        }
    }

    return service.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

if __name__ == "__main__":
    instances = list_instances()
    if instances == None:
        print('No running instances found!')
    else:
        print("Your running instances are:")
        for instance in instances:
            print(f"\t{instance['name']}")
		
    print("Setting up instance 1...")
    operation = create_instance_1('vm1')
    wait_for_operation(operation['name'])