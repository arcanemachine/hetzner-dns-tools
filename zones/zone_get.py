#!/usr/bin/python3

import json
import os
import requests


def zone_get(hetzner_dns_token=None, zone_id=None, name=None, id_only=False):
    result = None

    if hetzner_dns_token is None:
        # try to get token from environment variables
        try:
            hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']
        except KeyError:
            print("Missing zone_id")

    # if domain name is given, use it to obtain the zone
    if name:
        from .zone_list import zone_list
        dns_zones = zone_list()['zones']

        result = None
        for zone in dns_zones:
            if zone['name'] == name:
                result = {'zone': zone}

        if not result:
            raise ValueError("No match found")

        if id_only or os.environ.get('ID_ONLY') == '1':
            # just return the zone_id
            return result['zone']['id']
        else:
            return result

    if zone_id is None:
        # try to get zone_id from environment variables
        try:
            zone_id = os.environ['ZONE_ID']
        except KeyError:
            print("Missing ZONE_ID")

    try:
        response = requests.get(
            url=f"https://dns.hetzner.com/api/v1/zones/{zone_id}",
            headers={
                "Auth-API-Token": hetzner_dns_token,
                "Content-Type": "application/json; charset=utf-8",
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
    zone_get()
