import click
from nifcloud_request import NifCloudRequest
from nifcloud_parser import NifCloudParser
from itertools import zip_longest

@click.command()
@click.option('--rule-name', multiple=True)
def nifty_describe_separate_instance_rules(rule_name):
    payload = {'Action': 'NiftyDescribeSeparateInstanceRules'}
    if rule_name is not None:
        for i, name in enumerate(rule_name):
            payload.update({'SeparateInstanceRuleName.' + str(i+1): name})
    #Filter未対応
    res = NifCloudRequest().request(payload)
    NifCloudParser(res).xml()

@click.command()
@click.option('--rule-name', help='[required]')
@click.option('--instance-id', multiple=True)
@click.option('--unique-id', multiple=True)
@click.option('--description')
@click.option('--availability-zone', help='[required]')
def nifty_create_separate_instance_rule(rule_name, instance_id, unique_id, description, availability_zone):
    payload = {'Action': 'NiftyCreateSeparateInstanceRule'}
    payload.update({'SeparateInstanceRuleName': rule_name})
    if instance_id is not None:
        for i, name in enumerate(instance_id):
            payload.update({'InstanceId.' + str(i+1): name})
    elif unique_id is not None:
        for i, name in enumerate(unique_id):
            payload.update({'InstanceUniqueId.' + str(i+1): name})
    if description is not None:
        payload.update({'SeparateInstanceRuleDescription': description})
    payload.update({'Placement.AvailabilityZone': availability_zone})

    res = NifCloudRequest().request(payload)
    NifCloudParser(res).xml()

@click.command()
@click.option('--rule-name', help='[required]')
def nifty_delete_separate_instance_rule(rule_name):
    payload = {'Action': 'NiftyDeleteSeparateInstanceRule'}
    payload.update({'SeparateInstanceRuleName': rule_name})

    res = NifCloudRequest().request(payload)
    NifCloudParser(res).xml()
