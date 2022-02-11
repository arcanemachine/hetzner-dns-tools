#!/usr/bin/python3

import json
import os
import requests
import sys

import hetzner_dns_helpers as helpers

from record_list import record_list
from zone_get import zone_get


def record_get(hetzner_dns_token=None,
               record_id=None,
               zone_id=None,
               zone_name=None,
               name=None,
               ttl=None,
               record_type=None,
               value=None,
               get_first_record=False,
               allow_multiple_records=False,
               allow_multiple_zones=False,
               id_only=False):
    """
    Get info about an existing record.
    https://dns.hetzner.com/api-docs/#operation/GetRecord

    - Lookups can be performed directly with 'record_id', or indirectly
      using a combination of 'name', 'ttl', 'record_type', 'value',
      'zone_id', and 'zone_name'.

    - If indirect lookups are performed, an exception will be raised if
      multiple records are returned, *UNLESS* you specify a truthy
      value for the 'allow_multiple_records' or the 'get_first_record'
      parameters.

    - If 'id_only' passed in args or as environment variable (ID_ONLY),
      return just the record ID if one exists.

      - If 'id_only' and 'allow_multiple_records' are truthy, then return
        a list of record IDs.

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

    if not id_only and os.environ.get('ID_ONLY'):
        # get id_only from environment variable
        id_only = os.environ['ID_ONLY']

    # if record_id exists, do a direct lookup to obtain the record
    if record_id:
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

            # if id_only, return just the record ID
            if id_only:
                if __name__ == '__main__':
                    print(response_dict['record']['id'])
                    sys.exit(0)  # exit successfully
                else:
                    return response_dict['record']['id']

            # when running via the terminal, print output to console then exit
            if __name__ == '__main__':
                print(decoded_response)
                sys.exit(0)  # exit successfully

            return response_dict

        except requests.exceptions.RequestException as err:
            helpers.handle_request_exception(err)

    # do an indirect lookup of all relevant records and filter via given params
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
        record_type = os.environ['TYPE']

    if value is None and os.environ.get('VALUE'):
        # get value from environment variable
        value = os.environ['VALUE']

    if not get_first_record\
            and os.environ.get('GET_FIRST_RECORD'):
        # get get_first_record from environment variable
        get_first_record = os.environ['GET_FIRST_RECORD']

    if not allow_multiple_records\
            and os.environ.get('ALLOW_MULTIPLE_RECORDS'):
        # get allow_multiple_records from environment variable
        allow_multiple_records = os.environ['ALLOW_MULTIPLE_RECORDS']

    if not allow_multiple_zones\
            and os.environ.get('ALLOW_MULTIPLE_ZONES'):
        # get allow_multiple_zones from environment variable
        allow_multiple_zones = os.environ['ALLOW_MULTIPLE_ZONES']

    # BEGIN validation #

    # if no record_id exists, ensure that zone_name or zone_id exist,
    # in order to prevent pulling records from multiple zones
    if not record_id and not zone_name and not zone_id\
            and not allow_multiple_zones:
        error_message = "In order to prevent records from being pulled from "\
            "more than one zone, you must specify one (or more) of: "\
            "record_id, zone_id, or zone_name. You can override this "\
            "behavior by assigning a truthy value to 'allow_multiple_zones'."
        helpers.exit_with_error(error_message)

    # ensure that one or more optional parameters exist before doing
    # an indirect lookup
    if not record_id\
            and not name and not ttl and not record_type and not value:
        error_message =\
            "You must provide a record_id or one or more of the following: "\
            "name, ttl, record_type (environment variable: TYPE), or value."
        helpers.exit_with_error(error_message)

    # if zone_name passed, lookup the zone that matches it to get zone_id
    if zone_name:
        zone_name_id = zone_get(zone_name=zone_name, id_only=True)
        if not zone_id:
            zone_id = zone_name_id
        elif zone_id != zone_name_id:
            error_message =\
                "The zone_id you entered does not match the zone_id of "\
                "the zone_name you entered."
            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error
            else:
                raise ValueError(error_message)

    # END validation #

    records = record_list(hetzner_dns_token=hetzner_dns_token,
                          zone_id=zone_id)['records']

    # iterate over the given parameters, adding any matching records that
    # are not yet in the list
    if (zone_id or zone_name) and\
            (not name and not ttl and not record_type and not value):
        filtered_records = records
    else:
        filtered_records = []
        if name:
            for record in records:
                if record['name'] == name\
                        and record not in filtered_records:
                    filtered_records.append(record)
        if ttl:
            for record in records:
                if record['ttl'] == ttl\
                        and record not in filtered_records:
                    filtered_records.append(record)
        if record_type:
            for record in records:
                if record['type'] == record_type\
                        and record not in filtered_records:
                    filtered_records.append(record)
        if value:
            for record in records:
                if record['value'] == value\
                        and record not in filtered_records:
                    filtered_records.append(record)

    # if no records found, return empty dictionary
    if len(filtered_records) == 0:
        # when running via the terminal, print output to console then exit
        if __name__ == '__main__':
            print({})
            sys.exit(0)  # exit successfully
        return {}

    # if one record found, return it
    if len(filtered_records) == 1:
        # if id_only, return just the record ID
        if id_only:
            if __name__ == '__main__':
                print(filtered_records[0]['id'])
                sys.exit(0)  # exit successfully
            else:
                return filtered_records[0]['id']

        # when running via the terminal, print output to console then exit
        if __name__ == '__main__':
            print(json.dumps(filtered_records[0]))
            sys.exit(0)  # exit successfully
        return filtered_records[0]

    # handle multiple records
    if len(filtered_records) > 1:
        records_count = len(filtered_records)
        plural = "s" if records_count != 1 else ""
        if get_first_record:
            # if id_only, return just the record ID
            if id_only:
                if __name__ == '__main__':
                    print(filtered_records[0]['id'])
                    sys.exit(0)  # exit successfully
                else:
                    return filtered_records[0]['id']

            # when running via the terminal, print output to console then exit
            if __name__ == '__main__':
                print(json.dumps(filtered_records[0]))
                sys.exit(0)  # exit successfully
            return filtered_records[0]
        elif id_only and allow_multiple_records:
            id_list = []
            for record in filtered_records:
                id_list.append(record['id'])

            if __name__ == '__main__':
                print(json.dumps(id_list))
                sys.exit(0)  # exit successfully
            else:
                return id_list

        elif allow_multiple_records and not id_only:
            # when running via the terminal, print output to console,
            # then exit
            if __name__ == '__main__':
                print(json.dumps(filtered_records))
                sys.exit(0)  # exit successfully
            return filtered_records
        else:
            error_message =\
                f"Found {records_count} record{plural}. Assign a truthy "\
                "value to 'allow_multiple_records' To get all relevant "\
                "records, or use 'get_first_record' to get only the "\
                "first record. Capitalize these values if using "\
                "environment variables."
            if __name__ == '__main__':
                print(f"Error: {error_message}")
                sys.exit(1)  # exit with error
            else:
                raise ValueError(error_message)


if __name__ == '__main__':
    record_get()
