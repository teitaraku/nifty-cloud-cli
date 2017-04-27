import click
from niftycloud_request import NiftyCloudRequest
from niftycloud_parser import NiftyCloudParser

@click.command()
@click.option('--zone-name', multiple=True)
def describe_availability_zones(zone_name):
    payload = {'Action': 'DescribeAvailabilityZones'}
    for i, name in enumerate(zone_name):
        payload.update({'ZoneName.' + str(i+1): name})

    res = NiftyCloudRequest().request(payload)
    NiftyCloudParser(res).simple()
