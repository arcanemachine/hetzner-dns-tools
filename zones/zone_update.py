#!/usr/bin/python3

import json
import os
import requests
import sys


def zone_update(hetzner_dns_token=None,
                zone_id=None,
                name=None,
                new_name=None,
                ttl=86400):
    """
    Update an existing zone.

    - If doing a lookup by zone_id, use the name parameter to update the name.
    - If doing a lookup by name, use the new_name parameter to update the name.
    """
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if name is None:
        # get token from environment variable
        name = os.environ['NAME']

    if new_name is None:
        # get token from environment variable
        new_name = os.environ.get('NEW_NAME')

    if os.environ.get('TTL'):
        # get ttl from environment variable
        ttl = int(os.environ['TTL'])

    # return error/exception if not enough parameters passed
    if zone_id is None and 'ZONE_ID' not in os.environ\
            and new_name is None and 'NEW_NAME' not in os.environ\
            and ttl is None and 'TTL' not in os.environ:
        error_message =\
            "Not enough parameters. Needs one of: zone_id, new_name, ttl"

        if __name__ == '__main__':
            print(f"Error: {error_message}")
            sys.exit(1)  # exit with error

        raise ValueError(error_message)

    # return error/exception if using zone_id and new_name together
    if zone_id or 'ZONE_ID' in os.environ:
        if new_name or 'NEW_NAME' in os.environ:
            error_message = "Cannot use zone_id and new_name together."

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error

            raise ValueError(error_message)

    # if no zone_id exists and domain name is given, use it to obtain the zone
    if not zone_id:
        from zone_list import zone_list

        if name is None:
            name = os.environ['NAME']

        # get list of zones
        response_dict = zone_list()

        # check for errors
        if response_dict.get('error') or response_dict.get('message'):
            error_message = ""
            if response_dict.get('error'):
                error_message = response_dict['error']['message']
            elif response_dict.get('message'):
                error_message = response_dict['message']

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error
            else:
                raise ValueError(error_message)

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
            url=f"https://dns.hetzner.com/api/v1/zones/{zone_id}",
            headers={"Content-Type": "application/json",
                     "Auth-API-Token": hetzner_dns_token},
            data=json.dumps({"name": name,
                             "ttl": ttl}))

        decoded_response = response.content.decode('utf-8')
        response_dict = json.loads(decoded_response)

        # check for errors
        if response_dict.get('error') or response_dict.get('message'):
            error_message = ""
            if response_dict.get('error'):
                error_message = response_dict['error']['message']
            elif response_dict.get('message'):
                error_message = response_dict['message']

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error
            else:
                raise ValueError(error_message)

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


if __name__ == "__main__":
    zone_update()
