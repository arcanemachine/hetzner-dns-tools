#!/usr/bin/python3

import json
import os
import requests

from . import hetzner_dns_helpers as helpers
from .record_get import record_get


def delete_record_by_id(hetzner_dns_token, record_id):
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

        return "OK"

    except requests.exceptions.RequestException as err:
        helpers.handle_request_exception(err)


def record_delete(hetzner_dns_token=None,
                  record_id=None,
                  record_ids=None,
                  zone_id=None,
                  zone_name=None,
                  name=None,
                  ttl=None,
                  record_type=None,
                  value=None,
                  first_record_only=None,
                  delete_multiple_records=False,
                  search_all_zones=False):
    """
    Delete an existing record.
    https://dns.hetzner.com/api-docs/#operation/DeleteRecord

    Required* Parameters: One of: record_id or zone_id or zone_name

    Optional Parameters:
      Filters: record_type, name, value, ttl,
      Options: delete_multiple_records, first_record_only, search_all_zones*


    * This function will raise an exception if multiple records are
      returned, *unless* the `first_record_only` *or*
      `delete_multiple_records` parameters are truthy.

    - Deletions can be performed directly with 'record_id', or indirectly
      via a lookup that uses any combination of 'name', 'ttl',
      'record_type', 'value', 'zone_id', and/or 'zone_name'.

    - If doing a lookup, you must either specify a 'zone_id' or
      'zone_name', or assign a truthy value to 'search_all_zones'.

    * hetzner_dns_token *MUST* be passed in args or as environment
      variable (HETZNER_DNS_TOKEN). You can get a DNS API token
      here: https://dns.hetzner.com/settings/api-token

    - If using Bash environment variables, ensure that values are assigned
      in ALL_CAPS.
          - e.g. zone_id in Python -> ZONE_ID in environment variable
    """
    if hetzner_dns_token is None:
        # get token from environment variable
        hetzner_dns_token = os.environ['HETZNER_DNS_TOKEN']

    if record_id is None and os.environ.get('RECORD_ID'):
        # get record_id from environment variable
        record_id = os.environ['RECORD_ID']

    if record_ids is None and os.environ.get('RECORD_IDS'):
        # get record_ids from environment variable
        record_ids = os.environ['RECORD_IDS']

    if not first_record_only\
            and os.environ.get('FIRST_RECORD_ONLY'):
        # get first_record_only from environment variable
        first_record_only = os.environ['FIRST_RECORD_ONLY']

    if not search_all_zones\
            and os.environ.get('SEARCH_ALL_ZONES'):
        # get search_all_zones from environment variable
        search_all_zones = os.environ['SEARCH_ALL_ZONES']

    if not delete_multiple_records\
            and os.environ.get('DELETE_MULTIPLE_RECORDS'):
        # get delete_multiple_records from environment variable
        delete_multiple_records = os.environ['DELETE_MULTIPLE_RECORDS']

    # do an indirect lookup of all relevant records that match the parameters
    # and allow a single match to be returned
    if not record_id:
        if zone_id is None and os.environ.get('ZONE_ID'):
            # get zone_id from environment variable
            zone_id = os.environ['ZONE_ID']

        if zone_name is None and os.environ.get('ZONE_NAME'):
            # get zone_name from environment variable
            zone_name = os.environ['ZONE_NAME']

        if name is None and os.environ.get('NAME'):
            # get name from environment variable
            name = os.environ.get('NAME', None)

        if ttl is None and os.environ.get('TTL'):
            # get ttl from environment variable
            ttl = int(os.environ['TTL'])

        if record_type is None and os.environ.get('TYPE'):
            # get record_type from environment variable
            record_type = os.environ['RECORD_TYPE']\
                if os.environ.get('RECORD_TYPE') else os.environ['TYPE']

        if value is None and os.environ.get('VALUE'):
            # get value from environment variable
            value = os.environ['VALUE']

        # this method will return a string if one record is returned,
        # and a list if multiple records are returned
        record_get_id_result =\
            record_get(zone_id=zone_id,
                       zone_name=zone_name,
                       name=name,
                       ttl=ttl,
                       record_type=record_type,
                       value=value,
                       id_only=True,
                       first_record_only=first_record_only,
                       allow_multiple_records=delete_multiple_records,
                       search_all_zones=search_all_zones)

        if type(record_get_id_result) == list:
            records_count = len(record_get_id_result)

            # do not delete multiple records unless explicitly requested
            if not delete_multiple_records:
                error_message = f"Found {records_count} records. To "\
                    "delete multiple records via a query, assign a truthy "\
                    "value to 'delete_multiple_records', or use "\
                    "'first_record_only' to get only the "\
                    "first record. Capitalize these values if using "\
                    "environment variables."
                helpers.exit_with_error(error_message)

            else:
                record_ids = record_get_id_result
        else:
            if record_get_id_result:
                record_id = record_get_id_result
            else:
                helpers.exit_with_error("record not found")

    if record_id and record_ids:
        helpers.exit_with_error(
            "Cannot use 'record_id' and 'record_ids' at the same time.")
    elif record_id:
        delete_record_by_id(hetzner_dns_token, record_id)
    elif record_ids:
        for record_id_value in record_ids:
            delete_record_by_id(hetzner_dns_token, record_id_value)
    else:
        helpers.exit_with_error("No 'record_id' or 'record_ids' found.")


if __name__ == '__main__':
    record_delete()
