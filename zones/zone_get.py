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
            print("Missing hetzner_dns_token")

    # raise exception if using zone_id and id_only together
    if zone_id or os.environ.get('ZONE_ID') and id_only\
            or os.environ.get('ID_ONLY'):
        raise ValueError("Cannot use zone_id and id_only together.")

    # if domain name is given, use it to obtain the zone
    if name or os.environ.get('NAME'):
        from zone_list import zone_list

        if name is None:
            name = os.environ['NAME']

        # get the zones
        dns_zones = zone_list()['zones']

        # check for result
        result = None
        for zone in dns_zones:
            if zone['name'] == name:
                result = {'zone': zone}

        # if no result found, raise an exception
        if not result:
            raise ValueError("zone not found")

        if id_only or os.environ.get('ID_ONLY') == '1':
            # just return the zone_id
            result = result['zone']['id']

            if __name__ == '__main__':
                print(result)

            return result
        else:
            # return all zone data
            if __name__ == '__main__':
                print(result)

            return result

    if zone_id is None:
        # try to get zone_id from environment variables
        zone_id = os.environ['ZONE_ID']

    try:
        response = requests.get(
            url=f"https://dns.hetzner.com/api/v1/zones/{zone_id}",
            headers={
                "Auth-API-Token": hetzner_dns_token,
                "Content-Type": "application/json; charset=utf-8",
            },
        )

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        if 'error' in response_dict:
            if response_dict['error'].get('code') == 404:
                # if no result found, raise a ValueError
                raise ValueError("zone not found")
            else:
                # if exception cause is unknown, return generic exception
                raise Exception(response_dict['error']['message'])

        # when running via the terminal, print output to console
        if __name__ == '__main__':
            print(decoded_response)

        return json.loads(decoded_response)

    except requests.exceptions.RequestException:
        print('HTTP Request failed')


if __name__ == "__main__":
    zone_get()
