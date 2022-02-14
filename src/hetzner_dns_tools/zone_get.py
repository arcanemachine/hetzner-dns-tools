#!/usr/bin/python3

import json
import os
import requests
import sys

from . import hetzner_dns_helpers as helpers

from .zone_list import zone_list


def zone_get(hetzner_dns_token=None,
             zone_id=None,
             name=None,
             zone_name=None,
             id_only=False):
    """
    Get info about an existing zone.
    https://dns.hetzner.com/api-docs/#operation/GetZone

    Required Parameters: One of: `zone_id` or `name/zone_name`
      - `name` and `zone_name` are interchangeable in all zone functions
    Optional Parameters: `id_only`


    - Lookups can be performed using 'zone_id' or 'name/zone_name'.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    - If 'zone_id' passed in args or as environment variable (ZONE_ID),
      then use it to acquire the desired zone.

    - If (domain) 'name/zone_name' passed in args or as environment
      variable (NAME or ZONE_NAME), then use it to acquire the desired
      zone.

    - If 'id_only' passed in args or as environment variable (ID_ONLY),
      return just the zone ID if one exists.

    - If using Bash environment variables, ensure that values are assigned
      in ALL_CAPS.
          - e.g. zone_id in Python -> ZONE_ID in environment variable
    """
    if os.environ.get('SHOW_HELP'):
        # print the docstring and exit
        print(zone_get.__doc__)
        sys.exit(0)

    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if (name is None and os.environ.get('NAME'))\
            or (zone_name is None and os.environ.get('ZONE_NAME')):
        # get name/zone_name from environment variable
        zone_name = os.environ['ZONE_NAME']\
            if os.environ.get('ZONE_NAME') else os.environ.get('NAME')

    if not id_only and os.environ.get('ID_ONLY'):
        # get id_only from environment variable
        id_only = os.environ['ID_ONLY']

    zone = None

    # if zone_name exists, use it to obtain the zone (skip if zone_id exists)
    if (zone_name or 'ZONE_NAME' in os.environ) and zone_id is None:

        # get list of zones
        response_dict = zone_list()

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # check for matching zone
        dns_zones = response_dict['zones']
        for dns_zone in dns_zones:
            if dns_zone['name'] == zone_name:
                zone = {'zone': dns_zone}
                zone_id = zone['zone']['id']
                break

        # if no matching zone found, halt and notify of error
        if zone is None:
            error_message = "zone not found"

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error
            else:
                raise ValueError(error_message)

    # if we don't have a zone_id by now, then get it from environment variable
    if zone_id is None:
        zone_id = os.environ.get('ZONE_ID')

    # raise an exception if no zone_id or zone_name have been passed
    if not zone_id and not zone_name:
        helpers.exit_with_error("Must specify one of: zone_id, zone_name")

    # get response
    try:
        response = requests.get(
            url=f'https://dns.hetzner.com/api/v1/zones/{zone_id}',
            headers={'Auth-API-Token': hetzner_dns_token,
                     'Content-Type': 'application/json; charset=utf-8'})

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # assign value of response_dict to zone
        zone = response_dict

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)

    # return the expected zone ID or zone
    if id_only:
        # return the zone_id
        zone_id = zone['zone']['id']

        if __name__ == '__main__':
            print(zone_id)
            sys.exit(0)  # exit successfully

        return zone_id
    else:
        # return all zone data
        if __name__ == '__main__':
            print(json.dumps(zone))
            sys.exit(0)  # exit successfully

        return zone


if __name__ == '__main__':
    zone_get()
