#!/usr/bin/env python3

'''
This script interprets an RKE cluster.yml file, and provides those nodes as an
ansible inventory.

The file to be interpreted should be specified as an environment variable:
```
ANSIBLE_RKE_INVENTORY=path/to/file/cluster.yml
```

'''

import argparse
import json
import os


import yaml


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--list', action='store_true')
    parser.add_argument('--host')

    return parser.parse_args()


def fetch_rke_cluster():
    # test if ENV_VAR is set

    # confirm actual content
    # stat for non-0 file?

    with open(os.environ['ANSIBLE_RKE_INVENTORY'], 'r') as f:
        return yaml.load(f)


def gen_inv_list(rke_cluster):
    ansible_inv = {
        '_meta': {
            'hostvars': {}
        },
        'all': {
            'children': [],
            'hosts': []
        }
    } 

    groups = ['ungrouped', 'controlplane', 'etcd', 'worker']

    # generate bare structure of group
    for group in groups:
        ansible_inv['all']['children'].append(group)

        ansible_inv[group] = {
               'hosts': [],
               'vars': {},
               'children': [],
           }

        for node in rke_cluster['nodes']:
            nodename = node['hostname_override'] or node['address']
            if nodename not in ansible_inv['all']['hosts']:
                ansible_inv['all']['hosts'].append(nodename)
                ansible_inv['_meta']['hostvars'][nodename] = get_vars(node)
            
            if group in node['role']:
                ansible_inv[group]['hosts'].append(nodename)

    return ansible_inv


def gen_inv_host(rke_cluster, host):
    single_host = {}

    for node in rke_cluster['nodes']:
        if host == node['address']:
            single_host = get_vars(node)
            break # no need to search further
        elif host == node['hostname_override']:
            single_host = get_vars(node)
            break # no need to search further

    return single_host


def get_vars(node):
    single_host = {}

    if node['user']:
        single_host['ansible_user'] = node['user']

    return single_host


def main():
    args = parse_arguments()

    if args.host:
        inventory = gen_inv_host(fetch_rke_cluster(), args.host)
    else:
        inventory = gen_inv_list(fetch_rke_cluster())

    print(json.dumps(inventory))


if __name__=="__main__":
    main()
