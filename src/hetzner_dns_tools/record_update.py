#!/usr/bin/python3

import json
import os
import sys

import requests

from . import hetzner_dns_helpers as helpers
from .record_list import record_list
from .zone_list import zone_list


def record_update(
    hetzner_dns_token=None,
    record_type=None,
    name=None,
    record_id=None,
    value=None,
    ttl=None,
    zone_id=None,
    zone_name=None,
    debug=0,
    id_only=False,
):
    """
    Update a record.
    https://dns.hetzner.com/api-docs/#operation/UpdateRecord

    Required Parameters:
      - `hetzner_dns_token`, `record_type`, `value`, `zone_id`, `record_id`

    Optional Parameters:
      - `ttl`


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
    if os.environ.get("SHOW_HELP"):
        # print the docstring and exit
        print(record_update.__doc__)
        sys.exit(0)

    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ["HETZNER_DNS_TOKEN"]

    if record_type is None:
        # get record_type from environment variable
        record_type = (
            os.environ["RECORD_TYPE"]
            if os.environ.get("RECORD_TYPE")
            else os.environ["TYPE"]
        )

    if name is None:
        # get name from environment variable
        name = os.environ["NAME"] if os.environ.get("NAME") else "@"

    if value is None:
        # get value from environment variable
        value = os.environ["VALUE"]

    if ttl is None:
        if os.environ.get("TTL"):
            # get ttl from environment variable
            ttl = int(os.environ["TTL"])
        else:
            # use default value for TTL
            ttl = 86400

    if zone_name is None and os.environ.get("ZONE_NAME"):
        # get zone name from environment variable
        zone_name = os.environ["ZONE_NAME"]

    if name is None and os.environ.get("NAME"):
        # get record name from environment variable
        name = os.environ["NAME"]

    if debug == 0 and os.environ.get("DEBUG"):
        # get debug from environment variable
        debug = int(os.environ["DEBUG"])

    # if zone_name exists, use it to obtain the zone_id
    if zone_name:

        # get list of zones
        response_dict = zone_list(hetzner_dns_token=hetzner_dns_token)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # check for matching zone
        dns_zones = response_dict["zones"]
        for zone in dns_zones:
            if zone["name"] == zone_name:
                zone_id = zone["id"]
                break

        # if no matching zone found, then exit with error
        if zone_id is None:
            helpers.exit_with_error("zone not found")

    if not zone_name and not zone_id and not os.environ.get("ZONE_ID"):
        # if neither zone_name or zone_id exist, then exit with error
        helpers.exit_with_error("Must include one of: zone_id, zone_name")
    if zone_id is None:
        # get zone_id from environment variable
        zone_id = os.environ["ZONE_ID"]

    # if name exists, use it to obtain the record_id
    if name:

        # get list of records
        response_dict = record_list(hetzner_dns_token=hetzner_dns_token)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # check for matching record in zone
        dns_records = response_dict["records"]
        record_id_count = 0
        for record in dns_records:
            if record["name"] == name and record["type"] == record_type:
                record_id = record["id"]
                record_id_count += 1

        # if no matching name found, then exit with error
        if record_id is None:
            helpers.exit_with_error("name not found in records")

        # if no matching name found, then exit with error
        if record_id_count > 1:
            helpers.exit_with_error(
                "more than one record found for name and type, record_id must be provided"
            )

    if record_id is None:
        # get record_id from environment variable
        record_id = os.environ["RECORD_ID"]

    if record_id is None:
        # if record_id exist, then exit with error
        helpers.exit_with_error("Must include (or able to retrieve): record_id")

    try:
        params = {
            "ttl": ttl,
            "type": record_type,
            "value": value,
            "name": name,
            "zone_id": zone_id,
        }

        if debug > 0:
            print("DEBUG : request: record_id=%s" % record_id, file=sys.stderr)
            print(json.dumps(params), file=sys.stderr)

        response = requests.put(
            url="https://dns.hetzner.com/api/v1/records/" + record_id,
            headers={
                "Content-Type": "application/json",
                "Auth-API-Token": hetzner_dns_token,
            },
            data=json.dumps(params),
        )

        decoded_response = response.content.decode("utf-8")
        response_dict = json.loads(decoded_response)
        if debug > 0:
            print("DEBUG : response:", file=sys.stderr)
            print(json.dumps(response_dict), file=sys.stderr)

        # check response for errors
        helpers.check_response_for_errors(response_dict)

        # return all zone data
        if __name__ == "__main__":
            print(json.dumps(response_dict))
            sys.exit(0)  # exit successfully

        return response_dict

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


if __name__ == "__main__":
    record_update()
