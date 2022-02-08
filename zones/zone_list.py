#!/usr/bin/python3

import json
import os
import requests


def zone_list(hetzner_dns_token=None):
    if hetzner_dns_token is None:
        try:
            hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']
        except KeyError:
            print("Missing zone_id")

    try:
        response = requests.get(
            url="https://dns.hetzner.com/api/v1/zones",
            headers={
                "Auth-API-Token": os.environ['HETZNER_DNS_TOKEN'],
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
    zone_list()
