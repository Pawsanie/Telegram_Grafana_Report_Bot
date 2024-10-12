FROM alpine/ansible:2.17.0

COPY Grafana/Ansible/playbook.yaml /ansible/temporary_playbook.yaml
COPY Grafana/Ansible/technical_user.json /ansible/technical_user.json
COPY Grafana/Ansible/entry_point.sh /ansible/entry_point.sh
COPY Grafana/Ansible/inventory.ini /ansible/inventory.ini

# Make shell entrypoint exequteble:
RUN chmod +x ./ansible/entry_point.sh

# Work directory:
WORKDIR /ansible

# Run:
CMD ["./entry_point.sh"]