#!/usr/bin/python3

import json
import os
import requests
import sys

import hetzner_dns_helpers as helpers


def record_get(hetzner_dns_token=None,
               record_id=None,
               name=None,
               ttl=None,
               record_type=None,
               value=None,
               zone_name=None,
               allow_multiple=False,
               id_only=False):
    """
    Get info about an existing record.
    https://dns.hetzner.com/api-docs/#operation/GetRecord

    - Lookups can be performed directly with 'record_id', or indirectly
      using a combination of 'name', 'ttl', 'record_type', 'value',
      and 'zone_name'.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token
    """
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if record_id is None:
        # get record_id from environment variable
        record_id = os.environ['RECORD_ID']

    if zone_name is None:
        # get zone_name from environment variable
        zone_name = os.environ.get('ZONE_NAME', None)

    if name is None:
        # get domain name from environment variable
        name = os.environ.get('NAME', None)

    if ttl is None:
        if os.environ.get('TTL'):
            # get ttl from environment variable
            ttl = int(os.environ['TTL'])

    if record_type is None and os.environ.get('TYPE'):
        # get record_type from environment variable
        record_type = os.environ['TYPE']

    if value is None:
        # get value from environment variable
        value = os.environ['VALUE']

    if zone_name is None and os.environ.get('ZONE_NAME'):
        # get ttl from environment variable
        zone_name = os.environ['ZONE_NAME']

    if allow_multiple is None and os.environ.get('ALLOW_MULTIPLE'):
        # get allow_multiple from environment variable
        allow_multiple = os.environ['ALLOW_MULTIPLE']

    # if record_id exists, use it to obtain the record
    if record_type:

    return None

    # if zone_name exists, use it to obtain the zone
    if zone_name or 'ZONE_NAME' in os.environ:
        from zone_list import zone_list

        # get list of zones
        response_dict = zone_list()

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # check for matching zone
        matching_zone = None
        dns_zones = response_dict['zones']
        for zone in dns_zones:
            if zone['name'] == zone_name:
                matching_zone = {'zone': zone}
                break

        # if no matching zone found, halt and notify of error
        if matching_zone is None:
            error_message = "zone not found"

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error
            else:
                raise ValueError(error_message)

        # return the expected zone ID or zone
        if id_only or os.environ.get('ID_ONLY') == '1':
            # return the zone_id
            result = matching_zone['record']['id']

            if __name__ == '__main__':
                print(result)
                sys.exit(0)  # exit successfully

            return result
        else:
            # return all zone data
            if __name__ == '__main__':
                print(json.dumps(matching_zone))
                sys.exit(0)  # exit successfully

            return matching_zone

    # get response
    try:
        response = requests.get(
            url=f'https://dns.hetzner.com/api/v1/records/{record_id}',
            headers={'Auth-API-Token': hetzner_dns_token,
                     'Content-Type': 'application/json; charset=utf-8'})

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # when running via the terminal, print output to console then exit
        if __name__ == '__main__':
            print(decoded_response)
            sys.exit(0)  # exit successfully

        return response_dict

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


if __name__ == '__main__':
    zone_get()
