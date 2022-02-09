#!/usr/bin/python3

import json
import os
import requests
import sys


def zone_get(hetzner_dns_token=None, zone_id=None, name=None, id_only=False):
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    # raise exception if using zone_id and id_only together
    if zone_id or 'ZONE_ID' in os.environ:
        if id_only or 'ID_ONLY' in os.environ:
            error_message = "Cannot use zone_id and id_only together."

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error

            raise ValueError(error_message)

    # raise exception if using zone_id and name together
    if zone_id or 'ZONE_ID' in os.environ:
        if name or 'NAME' in os.environ:
            error_message = "Cannot use zone_id and name together."

            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error

            raise ValueError(error_message)

    # if domain name is given, use it to obtain the zone
    if name or 'NAME' in os.environ:
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

    if zone_id is None:
        # get zone_id from environment variable
        zone_id = os.environ['ZONE_ID']

    try:
        # get response
        response = requests.get(
            url=f"https://dns.hetzner.com/api/v1/zones/{zone_id}",
            headers={"Auth-API-Token": hetzner_dns_token,
                     "Content-Type": "application/json; charset=utf-8"})

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
    zone_get()
