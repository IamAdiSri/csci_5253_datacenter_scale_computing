#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth

credentials, project = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
zone = 'us-west1-b'

def create_instance(name):
    # Get the OS image
    image_response = service.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2204-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    
    # get all files as metadata strings
    startup_script = open(os.path.join(os.path.dirname(__file__), 'vm2-script.sh'), 'r').read()

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
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [
                {
                    # Startup script is automatically executed by the
                    # instance upon startup.
                    'key': 'startup-script',
                    'value': startup_script
                }
            ]
        }
    }

    return service.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

# [START wait_for_operation]
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
# [END wait_for_operation]


if __name__ == '__main__':
    name = 'vm2'

    print('Setting up instance 2...')
    operation = create_instance(name)
    wait_for_operation(operation['name'])

    print('Setting up firewall rules...')
    create_firewall = True
    for firewall in service.firewalls().list(project=project).execute()['items']:
        if firewall['name'] == 'allow-5000':
            print('Port 5000 is already accessible.')
            create_firewall = False
            break
    if create_firewall:
        firewall_body = {
            "name": 'allow-5000',
            "description": "Allows access from 5000 ports",
            "targetTags": [
                'allow-5000'
            ],
            "allowed": [{
                'IPProtocol': 'TCP',
                'ports': [5000]
            }],
            'direction': 'INGRESS'
        }

        operation = service.firewalls().insert(project=project, body=firewall_body).execute()
        print('Added firewall exception for port 5000.')

    print('Setting tag on instance...')
    cid = service.instances().get(project=project, zone=zone, instance=name).execute()
    tags_body = {
        'items': ['allow-5000'],
        'fingerprint': cid['tags']['fingerprint']
    }

    operation = service.instances().setTags(project=project, zone=zone, instance=name, body=tags_body).execute()

    print(f"Visit http://{cid['networkInterfaces'][0]['accessConfigs'][0]['natIP']}:5000 to access the flask application.")