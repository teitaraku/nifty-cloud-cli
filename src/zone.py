import click
from nifcloud_request import NifCloudRequest
from nifcloud_parser import NifCloudParser

@click.command()
@click.option('--zone-name', multiple=True)
def describe_availability_zones(zone_name):
    payload = {'Action': 'DescribeAvailabilityZones'}
    for i, name in enumerate(zone_name):
        payload.update({'ZoneName.' + str(i+1): name})

    res = NifCloudRequest().request(payload)
    NifCloudParser(res).xml()
