#!/usr/bin/env python
from ansible.module_utils.basic import *
from boto import ec2
from boto import vpc

class AWSLookup:
    """ A Class to do simple lookups in AWS """

    def __init__(self, aws_region):

        self.vpc_conn = vpc.connect_to_region(region_name=aws_region)
        self.ec2_conn = ec2.connect_to_region(region_name=aws_region)
        
    def __get_vpc_by_name(self, vpc_name):
        filters = {'tag:Name' : vpc_name}
        vpcs = self.vpc_conn.get_all_vpcs(filters=filters)
        if len(vpcs) == 0:
            return None
        return vpcs[0]

    def get_vpc_description(self, vpc_name):
        """Return info about VPC and all of its subnets."""
        vpc = self.__get_vpc_by_name(vpc_name)
        if not vpc:
            return None
        subnets = self.vpc_conn.get_all_subnets(filters={"vpcId" : vpc.id})
        vpc_dict =  convert_primitive_dict(vpc.__dict__)
        vpc_dict["name"] = vpc_name
        if subnets:
            vpc_dict["subnets"] = list_to_dict_by_tag(
                    [convert_primitive_dict(x.__dict__) for x in subnets],
                    "Name")
        else:
            vpc_dict["subnets"] = {}

        return vpc_dict

    def get_network_interfaces(self, vpc_name):
        """Return info about network interfaces in the vpc."""
        vpc = self.__get_vpc_by_name(vpc_name)
        if not vpc:
            return None
        return [convert_primitive_dict(x.__dict__)
                for x in self.ec2_conn.get_all_network_interfaces(
                        filters={"vpc-id" : vpc.id})]

    def get_security_groups(self, vpc_name):
        """Return a security group with the given name in the given VPC."""
        vpc = self.__get_vpc_by_name(vpc_name)
        if not vpc:
            return None
        security_groups = self.ec2_conn.get_all_security_groups(
                filters= {'vpc-id' : vpc.id})
        if len(security_groups) > 0:
            return list_to_dict_by_name(
                    [convert_primitive_dict(x.__dict__)
                    for x in security_groups])
        return None

    def get_all_availability_zones(self):
        """Return all availability zones in the curent region."""
        return list_to_dict_by_name(
                [convert_primitive_dict(x.__dict__)
                        for x in self.ec2_conn.get_all_zones()])

def convert_primitive_dict(aws_dict):
    primitive_dict = dict()
    for key,value in aws_dict.iteritems():
        if isinstance(value, unicode) or isinstance(value, bool) or isinstance(value, int):
            primitive_dict[key] = str(value)
        if isinstance(value, vpc.RegionInfo):
            primitive_dict[key] = value.name
        if isinstance(value, ec2.tag.TagSet):
            primitive_tags = dict()
            for tag_key, tag_value in value.iteritems():
                primitive_tags[str(tag_key)] = str(tag_value)
            primitive_dict[key] = primitive_tags
    return primitive_dict

def list_to_dict_by_name(data, name_key = 'name'):
    if not data:
        return {}
    return dict((i[name_key], i) for i in data)

def list_to_dict_by_tag(data, tag):
    return dict((i["tags"][tag], i) for i in data)

def main():
    """ This module does lookups in AWS to find vpc, availability zones and security groups.
    For each type of the lookup (vpc, az, security_group), 'register' is a required parameter,
    the result of the lookup will be stored in that variable. 
    Example:
      - name: lookup vpc
        aws_lookup:
            vpc:
              name: "{{ vpc_name }}"
              register: "vpc_info"
            az:
              register: "azs"
            security_group:
              vpc_name: "{{ vpc_name }}"
              register: "sg"
    The result of the lookup will be in 'vpc_info', 'azs' and 'sg'.
    The module will not fail if a lookup does not return anything, therfore you must verify
    if the object exists in AWS after the lookup. You can do that via assert statements.
    """
    module = AnsibleModule(
            argument_spec=dict(
                    vpc=dict(required=False, default=None),
                    az=dict(required=False, default=None),
                    security_group=dict(required=False, default=None),
                    network_interface=dict(required=False, default=None),
                    region=dict(required=False, default='us-west-2'),
                    ),
            supports_check_mode=True
            )
    region = module.params['region']
    aws_lookup = AWSLookup(region)    
    ansible_facts = {}
    if isinstance(module.params['vpc'], basestring):
        vpc_params = eval(module.params['vpc'])
    else:
        vpc_params = module.params['vpc']
    if isinstance(module.params['az'], basestring):
        az_params = eval(module.params['az'])
    else:
        az_params = module.params['az']
    if isinstance(module.params['network_interface'], basestring):
        eni_params = eval(module.params['network_interface'])
    else:
        eni_params = module.params['network_interface']
    if vpc_params is not None:
        vpc_dict = aws_lookup.get_vpc_description(vpc_params['vpc_name'])
        ansible_facts[vpc_params['register']] = vpc_dict

    if az_params is not None:
        az_dict = aws_lookup.get_all_availability_zones()
        ansible_facts[az_params['register']] = az_dict
    if isinstance(module.params['security_group'], basestring):
        security_group_params = eval(module.params['security_group'])
    else:
        security_group_params = module.params['security_group']
    if security_group_params is not None:
        group_dict = aws_lookup.get_security_groups(
                vpc_name=security_group_params['vpc_name'])
        ansible_facts[security_group_params['register']] = group_dict

    if eni_params is not None:
        network_interface_dict = aws_lookup.get_network_interfaces(
                vpc_name=eni_params['vpc_name'])
        ansible_facts[eni_params['register']] = network_interface_dict

    module.exit_json(changed=False, ansible_facts=ansible_facts)

main()
