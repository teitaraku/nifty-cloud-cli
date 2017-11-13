import click
from itertools import zip_longest
from nifcloud_request import NifCloudRequest
from nifcloud_parser import NifCloudParser

@click.command()
@click.option('--instance-id', multiple=True)
@click.option('--tenancy', type=click.Choice(['default', 'dedicated', 'all']), multiple=True)
def describe_instances(instance_id, tenancy):

    payload = {'Action': 'DescribeInstances'}
    for i, e in enumerate(zip_longest(instance_id, tenancy)):
        instance_id_, tenancy_ = e
        payload.update({'InstanceId.' + str(i+1): instance_id_ if instance_id_ is not None else ''})
        payload.update({'Tenancy.' + str(i+1): tenancy_ if tenancy_ is not None else 'default'})

    res = NifCloudRequest().request(payload)
    print(NifCloudParser(res).xml())

@click.command()
@click.option('--instance-id', help='[required] instance name')
@click.option('--attribute', type=click.Choice(['instanceType', 'disableApiTermination', 'instanceName', 'description', 'ipType', 'groupId', 'accountingType']))
@click.option('--value')
@click.option('--nifty-reboot', type=click.Choice(['force', 'true', 'false']), default='true')
@click.option('--force', is_flag=False)
@click.option('--tenancy', type=click.Choice(['default', 'dedicated', 'all']))
def modify_instance_attribute(instance_id, attribute, value, nifty_reboot, force, tenancy):
    payload = {'Action': 'ModifyInstanceAttribute'}
    payload.update({'InstanceId': instance_id})
    payload.update({'Attribute': attribute})
    payload.update({'Value': value})
    payload.update({'NiftyReboot': nifty_reboot})
    if nifty_reboot is not None:
        payload.update({'Force': 'true' if force is True else 'false'})
    payload.update({'Tenancy': tenancy})

    res = NifCloudRequest().request(payload)
    NifCloudParser(res).xml()
