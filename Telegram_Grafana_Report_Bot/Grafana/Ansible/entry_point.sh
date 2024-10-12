#!/bin/bash
# Shell script parse temporary playbook to standard playbook file for ansible pod.

# Workaround for Docker's File Inode Change Issue:
cat /ansible/temporary_playbook.yaml > /ansible/playbook.yaml

# Parse Ansible playbook:
sed -i "s|\${GRAFANA_URL}|$GRAFANA_URL|g" /ansible/playbook.yaml
sed -i "s|\${GRAFANA_TOKEN}|$GRAFANA_TOKEN|g" /ansible/playbook.yaml

# Start ansible playbook:
ansible-playbook -i /ansible/inventory.ini /ansible/playbook.yaml
exit 0