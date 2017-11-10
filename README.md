# AWS provisioning playbook for Ansible

can be used to provision the following infrastructure:
* VPC (with subnets and route tables)
* Security Groups
* ELB
* EC2 Instances (with attaching to the ELB)
* RDS Instance

to ~/.boto
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

to start
```
ansible-playbook site.yml -i inventories/dev/
```





