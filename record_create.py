#!/usr/bin/python3

import json
import os
import sys
import requests

import hetzner_dns_helpers as helpers


def record_create(hetzner_dns_token=None,
                  name=None,
                  ttl=None,
                  record_type=None,
                  value=None,
                  zone_id=None,
                  zone_name=None,
                  id_only=False):
    """
    Create a new record.
    https://dns.hetzner.com/api-docs/#operation/CreateRecord

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    * name *MUST* passed in args or as environment variable (NAME).
      It is used to set the name of the new record (e.g. 'www').

    """
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if name is None:
        # get name from environment variable
        name = os.environ['NAME']

    if ttl is None:
        if os.environ.get('TTL'):
            # get ttl from environment variable
            ttl = int(os.environ['TTL'])
        else:
            # use default value for TTL
            ttl = 86400

    if record_type is None:
        # get record_type from environment variable
        record_type = os.environ['TYPE']

    if value is None:
        # get value from environment variable
        value = os.environ['VALUE']

    if zone_name is None and os.environ.get('ZONE_NAME'):
        # get ttl from environment variable
        zone_name = os.environ['ZONE_NAME']

    # if zone_name exists, use it to obtain the zone_id
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
        params = {'name': name,
                  'ttl': ttl,
                  'type': record_type,
                  'value': value,
                  'zone_id': zone_id}
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
