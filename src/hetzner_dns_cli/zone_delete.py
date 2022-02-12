#!/usr/bin/python3

import json
import os
import sys
import requests

from . import hetzner_dns_helpers as helpers
from .zone_list import zone_list


def zone_delete(hetzner_dns_token=None,
                zone_id=None,
                zone_name=None,
                name=None):
    """
    Delete an existing zone.

    Required Parameters: One of: `zone_id` or `zone_name/name`


    - Lookups can be performed using 'zone_name/name' *OR* 'zone_id'.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

      - TIP: zone_create and zone_delete allow ZONE_NAME and NAME to
        be used interchangeably.

    - If using Bash environment variables, ensure that values are assigned
      in ALL_CAPS.
          - e.g. zone_id in Python -> ZONE_ID in environment variable
    """
    if os.environ.get('SHOW_HELP'):
        # print the docstring and exit
        print(zone_delete.__doc__)
        sys.exit(0)

    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if zone_name is None:
        # get name from environment variable
        zone_name = os.environ['NAME']\
            if os.environ.get('NAME') else os.environ.get('ZONE_NAME', None)
    elif name:
        # allow zone_name and name to be used interchangeably
        # for zone_create and zone_delete
        zone_name = name

    if os.environ.get('ZONE_ID'):
        zone_id = os.environ['ZONE_ID']

    # if zone_name exists, use it to obtain zone (skip if zone_id exists)
    if zone_name and not zone_id:

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
            helpers.exit_with_error("zone not found")

    # raise an exception if no zone_id or zone_name have been passed
    if not zone_id and not zone_name:
        helpers.exit_with_error("Must specify one of: zone_id, zone_name")

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
