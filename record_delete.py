#!/usr/bin/python3

import json
import os
import sys
import requests

import hetzner_dns_helpers as helpers


def record_delete(hetzner_dns_token=None,
                  record_id=None,
                  # require_confirmation=False
                  ):
    """
    Delete an existing zone.

    - Lookups can be performed directly with 'record_id'.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token
    """
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if record_id is None and os.environ.get('RECORD_ID'):
        # get record_id from environment variable
        record_id = os.environ['RECORD_ID']

    if record_id:
        try:
            response = requests.delete(
                url=f'https://dns.hetzner.com/api/v1/records/{record_id}',
                headers={'Auth-API-Token': hetzner_dns_token})

            decoded_response = response.content.decode('utf-8')
            response_dict = json.loads(decoded_response)

            # check response for errors
            helpers.check_response_for_errors(response_dict)

            # when running via the terminal, print output to console
            if __name__ == '__main__':
                print("OK")
                sys.exit(0)  # exit successfully

            return "OK"

        except requests.exceptions.RequestException as err:
            helpers.handle_request_exception(err)
    else:
        error_message = "Must specify record_id"

        if __name__ == '__main__':
            print(f"Error: {error_message}")
            sys.exit(1)  # exit with error
        else:
            raise ValueError(error_message)


if __name__ == '__main__':
    record_delete()
