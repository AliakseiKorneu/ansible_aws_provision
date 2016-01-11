# Deployment-LAMP-stack-to-AWS

Create:
*VPC
**RDS Security Group
***RDS Subnet Group
****RDS Instance
**Security Group
***EC2 Instance
****EBS
**ELB Security Group
***ELB
**ADD EC2 instances to ELB


to /etc/ansible/hosts
```
[local]
localhost
```

to ~/.boto
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

to start
```
ansible-playbook -i /etc/ansible/hosts site.yml
```
TODO:
* Automatization authentfication to ec2 instances throw SSH (Security?)




