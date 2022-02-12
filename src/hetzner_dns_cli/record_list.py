#!/usr/bin/python3

import json
import os
import sys
import requests

from . import hetzner_dns_helpers as helpers
from .zone_get import zone_get


def record_list(hetzner_dns_token=None, zone_id=None, zone_name=None):
    """
    Get list of all records.
    https://dns.hetzner.com/api-docs/#operation/GetRecords

    Required Parameters: One of: `zone_id` or `zone_name`


    - Lookups for individual zones can be done using 'zone_name'
      or 'zone_id'.

    - If no 'zone_name' or 'zone_id' is given, all records will
      be returned.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    - If using Bash environment variables, ensure that values are
      assigned in ALL_CAPS.
          - e.g. zone_id in Python -> ZONE_ID in environment variable
    """
    if os.environ.get('SHOW_HELP'):
        # print the docstring and exit
        print(record_list.__doc__)
        sys.exit(0)

    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if zone_id is None and os.environ.get('ZONE_ID'):
        # get zone_id from environment variable
        zone_id = os.environ['ZONE_ID']

    if zone_name is None and os.environ.get('ZONE_NAME'):
        # get zone_name from environment variable
        zone_name = os.environ['ZONE_NAME']

    # if zone_name exists, use it to obtain zone (skip if zone_id exists)
    if (zone_name or 'ZONE_NAME' in os.environ) and not zone_id:

        try:
            # get the desired zone
            response_dict = zone_get(zone_name=zone_name)
        except ValueError:
            # if no matching zone found, halt and notify of error
            helpers.exit_with_error("record not found")

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # get the zone_id
        zone = response_dict['zone']
        zone_id = zone['id']

    # get zone_id from environment variable
    if zone_id is None:
        zone_id = os.environ.get('ZONE_ID')

    try:
        # build params dict
        params = {}
        if zone_id:
            params['zone_id'] = zone_id

        # get response
        response = requests.get(url='https://dns.hetzner.com/api/v1/records',
                                params=params,
                                headers={'Auth-API-Token': hetzner_dns_token})

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        if __name__ == '__main__':
            # when running via the terminal, print output to console then exit
            print(decoded_response)
            sys.exit(0)  # exit successfully

        return response_dict

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


if __name__ == '__main__':
    record_list()
