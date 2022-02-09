#!/usr/bin/python3

import json
import os
import sys
import requests


def zone_list(hetzner_dns_token=None):
    """
    Get list of all zones.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token
    """

    # get token from environment variable
    if hetzner_dns_token is None:
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    # get response
    try:
        response = requests.get(url="https://dns.hetzner.com/api/v1/zones",
                                headers={"Auth-API-Token": hetzner_dns_token})

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

        if __name__ == '__main__':
            # when running via the terminal, print output to console
            print(decoded_response)
            sys.exit(0)  # exit successfully

        return response_dict

    except requests.exceptions.RequestException as e:
        # when running via the terminal, print output to console then exit
        if __name__ == '__main__':
            print(f"Error: {e}")
            sys.exit(1)  # exit with error
        else:
            raise requests.exceptions.RequestException(e)


if __name__ == "__main__":
    zone_list()
