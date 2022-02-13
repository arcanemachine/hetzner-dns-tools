#!/usr/bin/python3

import json
import os
import sys
import requests

from . import hetzner_dns_helpers as helpers


def zone_create(hetzner_dns_token=None,
                name=None,
                id_only=False,
                ttl=None,
                zone_name=None):
    """
    Create a new zone.
    https://dns.hetzner.com/api-docs/#operation/CreateZone

    Required Parameters: `name/zone_name`
      - `name` and `zone_name` are interchangeable in all zone functions
    Optional Parameters: `ttl`


    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    * name *MUST* passed in args or as environment variable.
      It is used to set the (domain) name of the new zone.

      - TIP: zone_create and zone_delete allow ZONE_NAME and NAME to
        be used interchangeably.

    - If 'id_only' passed in args or as environment variable (ID_ONLY),
      return just the zone ID after creating the new zone.

    - If using Bash environment variables, ensure that values are assigned
      in ALL_CAPS.
          - e.g. zone_id in Python -> ZONE_ID in environment variable
    """
    if os.environ.get('SHOW_HELP'):
        # print the docstring and exit
        print(zone_create.__doc__)
        sys.exit(0)

    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if name is None:
        # get domain name from environment variable
        name = os.environ['ZONE_NAME']\
            if os.environ.get('ZONE_NAME') else os.environ['NAME']
    elif zone_name:
        # allow zone_name and name to be used interchangeably
        # for zone_create and zone_delete
        name = zone_name

    if ttl is None:
        if os.environ.get('TTL'):
            # get TTL from environment variable
            ttl = int(os.environ['TTL'])
        else:
            # use default value for TTL
            ttl = 86400

    try:
        response = requests.post(url='https://dns.hetzner.com/api/v1/zones',
                                 headers={'Content-Type': 'application/json',
                                          'Auth-API-Token': hetzner_dns_token},
                                 data=json.dumps({'name': name,
                                                  'ttl': ttl}))

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # return the expected value
        if id_only or os.environ.get('ID_ONLY') == '1':
            # return the zone_id
            result = response_dict['zone']['id']

            if __name__ == '__main__':
                print(result)
                sys.exit(0)  # exit successfully

            return result
        else:
            # return all zone data
            if __name__ == '__main__':
                print(json.dumps(response_dict))
                sys.exit(0)  # exit successfully

            return response_dict

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


if __name__ == '__main__':
    zone_create()
