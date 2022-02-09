#!/usr/bin/python3

import json
import os
import requests


def zone_create(hetzner_dns_token=None, name=None):
    if hetzner_dns_token is None:
        try:
            hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']
        except KeyError:
            print("Missing hetzner_dns_token")

    if name is None:
        try:
            name = os.environ['name']
        except KeyError:
            print("Missing name")

    try:
        response = requests.post(
            url="https://dns.hetzner.com/api/v1/zones",
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": hetzner_dns_token,
            },
            data=json.dumps({
                "name": name,
                "ttl": 86400
            })
        )

        decoded_response = response.content.decode('utf-8')

        # when running via the terminal, print output to console
        if __name__ == '__main__':
            print(decoded_response)

        # return decoded response
        return json.loads(decoded_response)

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == "__main__":
    zone_create()
