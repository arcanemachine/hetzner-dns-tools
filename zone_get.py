#!/usr/bin/python3

import json
import os
import requests
import sys

import hetzner_dns_helpers as helpers


def zone_get(hetzner_dns_token=None, zone_id=None, name=None, id_only=False):
    """
    Get info about an existing zone.

    - Lookups can be performed using 'name' or 'zone_id'.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    - If 'zone_id' passed in args or as environment variable (ZONE_ID),
      then use it to acquire the desired zone.

    - If (domain) 'name' passed in args or as environment variable (NAME),
      then use it to acquire the desired zone.

    - If 'id_only' passed in args or as environment variable (ID_ONLY),
      return just the zone ID if one exists.
    """
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    # if (domain) name exists, use it to obtain the zone (but only if
    # zone_id is falsy)
    if (name or 'NAME' in os.environ)\
            and (zone_id is None and 'ZONE_ID' not in os.environ):
        from zone_list import zone_list

        # get name from environment variable
        if name is None:
            name = os.environ['NAME']

        # get list of zones
        response_dict = zone_list()

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # check for matching zone
        matching_zone = None
        dns_zones = response_dict['zones']
        for zone in dns_zones:
            if zone['name'] == name:
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
            result = matching_zone['zone']['id']

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

    # if we don't have a zone_id by now, then get it from environment variable
    if zone_id is None:
        zone_id = os.environ['ZONE_ID']

    # get response
    try:
        response = requests.get(
            url=f"https://dns.hetzner.com/api/v1/zones/{zone_id}",
            headers={"Auth-API-Token": hetzner_dns_token,
                     "Content-Type": "application/json; charset=utf-8"})

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


if __name__ == "__main__":
    zone_get()
