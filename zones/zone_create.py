#!/usr/bin/python3

import json
import os
import sys
import requests


def zone_create(hetzner_dns_token=None, name=None, id_only=False):
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if name is None:
        # get domain name from environment variable
        name = os.environ['NAME']

    try:
        response = requests.post(url="https://dns.hetzner.com/api/v1/zones",
                                 headers={"Content-Type": "application/json",
                                          "Auth-API-Token": hetzner_dns_token},
                                 data=json.dumps({"name": name,
                                                  "ttl": 86400}))

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

        # return the expected result
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

        return response_dict

    except requests.exceptions.RequestException as e:
        if __name__ == '__main__':
            # when running via the terminal, print error to console
            print(f"Error: {e}")
            sys.exit(1)  # exit with error
        else:
            raise requests.exceptions.RequestException(e)


if __name__ == "__main__":
    zone_create()
