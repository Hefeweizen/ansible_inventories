# A collection of convenient Ansible dynamic inventory scripts

## RKE Cluster
```
$ export ANSIBLE_RKE_INVENTORY=../rke_project/cluster.yml
$ ansible -i rke/read_rke_cluster.py all -m shell -a 'uptime'
host001.example.net | SUCCESS | rc=0 >>
 09:32:00 up 22 days, 21:09,  1 user,  load average: 0.34, 0.13, 0.11

host003.example.net | SUCCESS | rc=0 >>
 09:32:00 up 22 days, 21:09,  1 user,  load average: 0.11, 0.04, 0.01

host002.example.net | SUCCESS | rc=0 >>
 09:32:00 up 22 days, 21:09,  1 user,  load average: 0.20, 0.30, 0.28
```
