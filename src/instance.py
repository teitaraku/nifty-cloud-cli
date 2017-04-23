import os
import click
import configparser
import requests
from datetime import datetime
import hmac
import hashlib
import base64
from bs4 import BeautifulSoup as soup
from itertools import zip_longest

@click.command()
@click.option('--instance-id', multiple=True)
@click.option('--tenancy', type=click.Choice(['default', 'dedicated', 'all']), multiple=True)
def describe_instances(instance_id, tenancy):
    action = 'DescribeInstances'

    config = configparser.SafeConfigParser()
    config.read('./config.ini')
    endpoint = os.getenv("ENDPOINT", config.get('common', 'ENDPOINT'))
    access_key = os.getenv("ACCESS_KEY", config.get('user', 'ACCESS_KEY'))
    secret_key = os.getenv("SECRET_ACCESS_KEY", config.get('user', 'SECRET_ACCESS_KEY'))

    request = endpoint + '?Action=' + action
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03dZ" % (now.microsecond // 1000)
    string_to_sign = action + timestamp
    digester = hmac.new(bytes(secret_key, 'UTF-8'), bytes(string_to_sign, 'UTF-8'), hashlib.sha1)
    signature = base64.b64encode(digester.digest())
    payload = {'AccessKeyId': access_key, 'SignatureVersion': '0', 'Signature': signature, 'Timestamp': timestamp}

    for i, e in enumerate(zip_longest(instance_id, tenancy)):
        _instance_id, _tenancy = e
        payload.update({'InstanceId.' + str(i+1): _instance_id if _instance_id is not None else ''})
        payload.update({'Tenancy.' + str(i+1): _tenancy if _tenancy is not None else 'default'})

    print(payload)
    res = requests.get(request, params=payload)
    for tag in soup(res.text, "html.parser").findAll(True):
        if tag.text is not '' and len(tag.contents) is 1:
            print(" : ".join([tag.name, tag.text]))

@click.command()
@click.option('--instance-id', help='[required] instance name')
@click.option('--attribute', type=click.Choice(['instanceType', 'disableApiTermination', 'instanceName', 'description', 'ipType', 'groupId', 'accountingType']))
@click.option('--value')
@click.option('--nifty-reboot', type=click.Choice(['force', 'true', 'false']), default='true')
@click.option('--force', is_flag=False)
@click.option('--tenancy', type=click.Choice(['default', 'dedicated', 'all']))
def modify_instance_attribute(instance_id, attribute, value, nifty_reboot, force, tenancy):
    action = 'ModifyInstanceAttribute'

    config = configparser.SafeConfigParser()
    config.read('./config.ini')
    endpoint = os.getenv("ENDPOINT", config.get('common', 'ENDPOINT'))
    access_key = os.getenv("ACCESS_KEY", config.get('user', 'ACCESS_KEY'))
    secret_key = os.getenv("SECRET_ACCESS_KEY", config.get('user', 'SECRET_ACCESS_KEY'))

    request = endpoint + '?Action=' + action
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03dZ" % (now.microsecond // 1000)
    string_to_sign = action + timestamp
    digester = hmac.new(bytes(secret_key, 'UTF-8'), bytes(string_to_sign, 'UTF-8'), hashlib.sha1)
    signature = base64.b64encode(digester.digest())
    payload = {'AccessKeyId': access_key, 'SignatureVersion': '0', 'Signature': signature, 'Timestamp': timestamp}

    payload.update({'InstanceId': instance_id})
    payload.update({'Attribute': attribute})
    payload.update({'Value': value})
    payload.update({'NiftyReboot': nifty_reboot})
    if nifty_reboot is not None:
        payload.update({'Force': 'true' if force is True else 'false'})

    payload.update({'Tenancy': tenancy})

    print(payload)
    res = requests.get(request, params=payload)
    for tag in soup(res.text, "html.parser").findAll(True):
        if tag.text is not '' and len(tag.contents) is 1:
            print(" : ".join([tag.name, tag.text]))
