#!/usr/bin/python3

import json
import os
import requests
import sys

import hetzner_dns_helpers as helpers


def zone_update(hetzner_dns_token=None,
                zone_id=None,
                name=None,
                new_name=None,
                ttl=None):
    """
    *******************************************************************
    *THIS FUNCTION DOES NOT WORK! USE CREATE/DELETE FUNCTIONS INSTEAD!*
    *******************************************************************

    Update an existing zone. Updateable values are 'name' and 'ttl'.
    https://dns.hetzner.com/api-docs/#operation/UpdateZone

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    * zone_id *OR* new_name args/environment variables (ZONE_ID/NEW_NAME)
      *MUST* be passed, but *NOT BOTH*.

    - If 'new_name' passed in args or as environment variable (NEW_NAME),
      then use 'name' to acquire the desired zone. (It's the domain name.)

    - If doing a lookup by 'zone_id', use 'name' to update the name.

    - If doing a lookup by 'name', use 'new_name' to update the name.

    * 'name' and/or 'ttl' *MUST* be passed if using 'zone_id'.

    * 'new_name' *MUST* be passed if using 'name'.

    * 'zone_id' and 'name' *CANNOT* be used together.

    """

    if True:
        error_message = "This module doesn't work! Use create/delete instead!"

        if __name__ == '__main__':
            print(f"Error: {error_message}")
            sys.exit(1)  # exit with error

        raise ValueError(error_message)

    # BEGIN validation #

    # must use name and/or ttl if using zone_id
    if (zone_id is None and 'ZONE_ID' not in os.environ)\
            and ((name is None and 'NAME' not in os.environ)
                 or (ttl is None and 'TTL' not in os.environ)):
        error_message =\
            "Must use name and/or ttl with zone_id"

        if __name__ == '__main__':
            print(f"Error: {error_message}")
            sys.exit(1)  # exit with error

        raise ValueError(error_message)

    # must use name if using new_name
    if new_name is not None or 'NEW_NAME' in os.environ:
        if name is None and 'NAME' not in os.environ:
            error_message =\
                "Must use name if using new_name"

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error

            raise ValueError(error_message)

    # cannot use zone_id and new_name together
    if (zone_id or 'ZONE_ID' in os.environ)\
            and (new_name or 'NEW_NAME' in os.environ):
        error_message = "Cannot use zone_id and new_name together."

        if __name__ == '__main__':
            print(f"Error: {error_message}")
            sys.exit(1)  # exit with error

        raise ValueError(error_message)

    # END validation #

    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if name is None:
        # get name from environment variable
        name = os.environ.get('NAME')

    if new_name is None:
        # get new_name from environment variable
        new_name = os.environ.get('NEW_NAME')

    if ttl is None:
        if os.environ.get('TTL'):
            # get TTL from environment variable
            ttl = int(os.environ['TTL'])
        else:
            # use default value for TTL
            ttl = 86400

    # if new_name is given (and no zone_id was passed), then use name to
    # obtain the zone
    if new_name and not zone_id:
        from zone_list import zone_list

        # get list of zones
        response_dict = zone_list()

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # check for matching zone
        dns_zones = response_dict['zones']
        for zone in dns_zones:
            if zone['name'] == name:
                zone_id = zone['id']
                name = new_name  # swap name with new_name to update the record
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
        # get response
        response = requests.put(
            url=f'https://dns.hetzner.com/api/v1/zones/{zone_id}',
            headers={'Content-Type': 'application/json',
                     'Auth-API-Token': hetzner_dns_token},
            data=json.dumps({'name': name,
                             'ttl': ttl}))

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # when running via the terminal, print output to console
        if __name__ == '__main__':
            print(decoded_response)
            sys.exit(0)  # exit successfully

        return response_dict

    except requests.exceptions.RequestException as e:
        if __name__ == '__main__':
            # when running via the terminal, print error to console
            print(f"Error: {e}")
            sys.exit(1)  # exit with error
        else:
            raise requests.exceptions.RequestException(e)


if __name__ == '__main__':
    zone_update()
