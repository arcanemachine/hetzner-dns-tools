#!/usr/bin/python3

import json
import os
import sys
import requests

from . import hetzner_dns_helpers as helpers


def zone_list(hetzner_dns_token=None):
    """
    Get list of all zones.
    https://dns.hetzner.com/api-docs/#operation/GetZones


    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    - If using Bash environment variables, ensure that values are assigned
      in ALL_CAPS.
          - e.g. zone_id in Python -> ZONE_ID in environment variable
    """
    if os.environ.get('SHOW_HELP'):
        # print the docstring and exit
        print(zone_list.__doc__)
        sys.exit(0)

    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    # get response
    try:
        response = requests.get(url='https://dns.hetzner.com/api/v1/zones',
                                headers={'Auth-API-Token': hetzner_dns_token})

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        if __name__ == '__main__':
            # when running via the terminal, print output to console
            print(decoded_response)
            sys.exit(0)  # exit successfully

        return response_dict

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


if __name__ == '__main__':
    zone_list()
