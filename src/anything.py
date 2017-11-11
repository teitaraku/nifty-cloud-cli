import click
from niftycloud_request import NiftyCloudRequest
from niftycloud_parser import NiftyCloudParser
from itertools import zip_longest

@click.command()
@click.option('--action', help='[required] Action name')
@click.option('--key', multiple=True)
@click.option('--value', multiple=True)
def anything_request(action, key, value):

    payload = {'Action': action}
    for e in zip_longest(key, value):
        key_, value_ = e
        payload.update({key_: value_})

    res = NiftyCloudRequest().request(payload)
    NiftyCloudParser(res).simple()
