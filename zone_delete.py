#!/usr/bin/python3

import json
import os
import sys
import requests

import hetzner_dns_helpers as helpers


def zone_delete(hetzner_dns_token=None, zone_id=None, zone_name=None):
    """
    Delete an existing zone.

    - Lookups can be performed using 'zone_name' *OR* 'zone_id'.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    * zone_id *OR* name args/environment variables (ZONE_ID/NAME)
      *MUST* be passed, but *NOT BOTH*.
    """
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if zone_name is None:
        # get name from environment variable
        zone_name = os.environ.get('ZONE_NAME', None)

    # if (domain) name exists, use it to obtain the zone
    if zone_name:
        from zone_list import zone_list

        # get list of zones
        response_dict = zone_list()

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # check for matching zone
        dns_zones = response_dict['zones']
        for zone in dns_zones:
            if zone['name'] == zone_name:
                zone_id = zone['id']
                break

        # if no matching zone found, halt and notify of error
        if zone_id is None:
            error_message = "zone not found"

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error
            else:
                raise ValueError(error_message)

    if zone_id is None:
        # get zone_id from environment variable
        zone_id = os.environ['ZONE_ID']

    try:
        response = requests.delete(
            url=f'https://dns.hetzner.com/api/v1/zones/{zone_id}',
            headers={'Auth-API-Token': hetzner_dns_token})

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # when running via the terminal, print output to console
        if __name__ == '__main__':
            print("OK")
            sys.exit(0)  # exit successfully

        return "OK"

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


if __name__ == '__main__':
    zone_delete()
