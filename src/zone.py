import os
import click
import configparser
import requests
from datetime import datetime
import hmac
import hashlib
import base64
from bs4 import BeautifulSoup as soup

@click.command()
@click.option('--zone-name', multiple=True)
def describe_availability_zones(zone_name):
    action = 'DescribeAvailabilityZones'

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
    for i, name in enumerate(zone_name):
        payload.update({'ZoneName.' + str(i+1): name})
    res = requests.get(request, params=payload)
    for tag in soup(res.text, "html.parser").findAll(True):
        if tag.text is not '' and len(tag.contents) is 1:
            print(" : ".join([tag.name, tag.text]))
