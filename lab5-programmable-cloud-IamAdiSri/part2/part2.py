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
name = 'part1'
snapshot_name = 'base-snapshot-part1'

#
# Stub code - just lists all instances
#
def list_instances():
    result = service.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

# [START wait_for_operation]
def wait_for_operation(operation):
    print('\tWaiting for operation to finish...', end='')
    while True:
        result = service.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print('done!')
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)
# [END wait_for_operation]

def create_instance_from_snapshot(name, snapshot):
    # Get the source snapshot
    source_disk_image = f'global/snapshots/{snapshot}'

    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    
    # load startup script
    startup_script = open(os.path.join(os.path.dirname(__file__), 'startup-script.sh'), 'r').read()

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceSnapshot': source_disk_image,
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
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }]
        }
    }

    return service.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

if __name__=="__main__":
    print("Your running instances are:")
    for instance in list_instances():
        print(f"\t{instance['name']}")
    
    print("Creating disk snapshot...")
    snapshot_body = {
        'name': snapshot_name
    }

    operation = service.disks().createSnapshot(project=project, zone=zone, disk=name, body=snapshot_body).execute()
    wait_for_operation(operation['name'])

    output_file = open(os.path.join(os.path.dirname(__file__), 'TIMING.md'), 'w')
    for i in range(3):
        print(f"Creating instance part2-{i}...")
        start_time = time.time()
        
        operation = create_instance_from_snapshot(f"part2-{i}", snapshot_name)
        wait_for_operation(operation['name'])
        
        end_time = time.time()
        print(f"\tTime taken = {end_time-start_time}")
        output_file.write(f"Time taken for instance {i} = {end_time-start_time}\n")
        
        print('\tOpening port 5000 on the VM...')
        cid = service.instances().get(project=project, zone=zone, instance=name).execute()
        tags_body = {
            'items': ['allow-5000'],
            'fingerprint': cid['tags']['fingerprint']
        }
        response = service.instances().setTags(project=project, zone=zone, instance=name, body=tags_body).execute()
        
        print(f"\tVisit http://{cid['networkInterfaces'][0]['accessConfigs'][0]['natIP']}:5000 to access the flask application.")
    output_file.close()


