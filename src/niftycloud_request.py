import os
import configparser
import requests
from datetime import datetime
import hmac, hashlib, base64
from itertools import zip_longest

class NiftyCloudRequest():
    def __init__(self):
        config = configparser.SafeConfigParser()
        config.read('./config.ini')
        self.endpoint = os.getenv("ENDPOINT", config.get('common', 'ENDPOINT'))
        self.signature_version = os.getenv("SIGNATURE_VERSION", config.get('common', 'SIGNATURE_VERSION'))
        self.access_key = os.getenv("ACCESS_KEY", config.get('user', 'ACCESS_KEY'))
        self.secret_key = os.getenv("SECRET_ACCESS_KEY", config.get('user', 'SECRET_ACCESS_KEY'))

    def request(self, payload):
        request_url = self.endpoint# + '?Action=' + self.action
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%S") + ".%03dZ" % (now.microsecond // 1000)

        payload.update({'AccessKeyId': self.access_key})
        payload.update({'SignatureVersion': self.signature_version})
        payload.update({'Timestamp': timestamp})

        if self.signature_version is '0':
            signature = self.__calc_version0(payload)
        elif self.signature_version is '1':
            signature = self.__calc_version1(payload)

        payload.update({'Signature': signature})

        return requests.get(request_url, params=payload)

    def __calc_version0(self, payload):
        action = payload['Action']
        timestamp = payload['Timestamp']
        string_to_sign = action + timestamp
        digester = hmac.new(bytes(self.secret_key, 'UTF-8'), bytes(string_to_sign, 'UTF-8'), hashlib.sha1)
        return base64.b64encode(digester.digest())

    def __calc_version1(self, payload):
        string_to_sign = ''
        for k, v in payload.items():
            string_to_sign = string_to_sign + k + v
        digester = hmac.new(bytes(self.secret_key, 'UTF-8'), bytes(string_to_sign, 'UTF-8'), hashlib.sha1)
        print("string_to_sign: ", string_to_sign)
        return base64.b64encode(digester.digest())
