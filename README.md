# Deployment-LAMP-stack-to-AWS

Create:
* VPC
* RDS Security Group
* RDS Subnet Group
* RDS Instance
* Security Group
* 2 EC2 Instances
* EBS
* ELB Security Group
* ELB
* ADD EC2 instances to ELB

Configure:
* Install Apache2
* Install PHP (+modules)
* Install MySQL
* Instalk nginx and configured it as proxy

Test:
* Test 200 HTTP Response

Destroy:
*Destroy all infrastrusture


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




