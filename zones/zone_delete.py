#!/usr/bin/python3

import json
import os
import requests


def zone_delete(hetzner_dns_token=None, zone_id=None):
    if hetzner_dns_token is None:
        try:
            hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']
        except KeyError:
            print("Missing zone_id")

    if zone_id is None:
        try:
            zone_id = os.environ['ZONE_ID']
        except KeyError:
            print("Missing ZONE_ID")

    try:
        response = requests.delete(
            url=f"https://dns.hetzner.com/api/v1/zones/{zone_id}",
            headers={
                "Auth-API-Token": hetzner_dns_token,
            },
        )

        decoded_response = response.content.decode('utf-8')

        # when running via the terminal, print output to console
        if __name__ == '__main__':
            print(decoded_response)

        return json.loads(decoded_response)

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == "__main__":
    zone_delete()
