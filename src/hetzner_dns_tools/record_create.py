#!/usr/bin/python3

import json
import os
import sys
import requests

from . import hetzner_dns_helpers as helpers
from .zone_list import zone_list


def record_create(hetzner_dns_token=None,
                  record_type=None,
                  name=None,
                  value=None,
                  ttl=None,
                  zone_id=None,
                  zone_name=None,
                  id_only=False):
    """
    Create a new record.
    https://dns.hetzner.com/api-docs/#operation/CreateRecord

    Required Parameters:
      - `hetzner_dns_token`, `record_type`, `value`, `zone_id`

    Optional Parameters:
      - `zone_name`, `name`, `ttl`, `id_only`


    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    * If name is not passed, then '@' will be used.

    * MX records must be given a priority and server using the
      'value' field.
        - e.g. '10 your-domain.com'  # priority: 10, server: your-domain.com

    * SRV records must be given a priority, weight, port and target using
      the 'value' field.
        - e.g. '1 2 3 your-domain.com' # priority: 1, weight: 2,
                                       # port: 3, target: your-domain.com

    - If using Bash environment variables, ensure that values are assigned
      in ALL_CAPS.
        - e.g. zone_id in Python -> ZONE_ID in environment variable
    """
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if record_type is None:
        # get record_type from environment variable
        record_type = os.environ['RECORD_TYPE']\
            if os.environ.get('RECORD_TYPE') else os.environ['TYPE']

    if name is None:
        # get name from environment variable
        name = os.environ['NAME'] if os.environ.get('NAME') else '@'

    if value is None:
        # get value from environment variable
        value = os.environ['VALUE']

    if ttl is None:
        if os.environ.get('TTL'):
            # get ttl from environment variable
            ttl = int(os.environ['TTL'])
        else:
            # use default value for TTL
            ttl = 86400

    if zone_name is None and os.environ.get('ZONE_NAME'):
        # get ttl from environment variable
        zone_name = os.environ['ZONE_NAME']

    # if zone_name exists, use it to obtain the zone_id
    if zone_name:

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

        # if no matching zone found, then exit with error
        if zone_id is None:
            helpers.exit_with_error("zone not found")

    if not zone_name and not zone_id and not os.environ.get('ZONE_ID'):
        # if neither zone_name or zone_id exist, then exit with error
        helpers.exit_with_error("Must include one of: zone_id, zone_name")
    if zone_id is None:
        # get zone_id from environment variable
        zone_id = os.environ['ZONE_ID']

    try:
        params = {'ttl': ttl,
                  'type': record_type,
                  'value': value,
                  'zone_id': zone_id}
        if name:
            params['name'] = name

        response = requests.post(url='https://dns.hetzner.com/api/v1/records',
                                 headers={'Content-Type': 'application/json',
                                          'Auth-API-Token': hetzner_dns_token},
                                 data=json.dumps(params))

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # return the expected result
        if id_only or os.environ.get('ID_ONLY') == '1':
            # return the zone_id
            result = response_dict['record']['id']

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

        return response_dict

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


if __name__ == '__main__':
    record_create()
