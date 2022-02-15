#!/usr/bin/python3

import json
import os
import requests
import sys

from . import hetzner_dns_helpers as helpers
from .record_list import record_list
from .zone_get import zone_get


def record_get(hetzner_dns_token=None,
               record_id=None,
               zone_id=None,
               zone_name=None,
               record_type=None,
               name=None,
               value=None,
               first_record_only=False,
               allow_multiple_records=False,
               search_all_zones=False,
               id_only=False):
    """
    Get info about an existing record.
    https://dns.hetzner.com/api-docs/#operation/GetRecord

    Required* Parameters: One of: `record_id` or `zone_id` or `zone_name`

    Optional Parameters:
      Filters: record_type, name, value
      Formats: id_only
      Options: first_record_only, allow_multiple_records, search_all_zones


    * This function will raise an exception if multiple records are
      returned, *unless* the `first_record_only` *or*
      `allow_multiple_records` parameters are truthy.

    - Lookups can be performed directly with 'record_id', or indirectly
      using a combination of 'name', 'record_type', 'value', 'zone_id',
      and 'zone_name'.
        - Due to how record_list is structured, 'ttl' is not an
          available filter.

    - If doing an indirect lookup, you must either specify a 'zone_id' or
      'zone_name', or assign a truthy value to 'search_all_zones'.

    - If indirect lookups are performed, an exception will be raised if
      multiple records are returned, *UNLESS* you specify a truthy
      value for the 'allow_multiple_records' or the 'first_record_only'
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

    if record_type is None and os.environ.get('TYPE'):
        # get record_type from environment variable
        record_type = os.environ['RECORD_TYPE']\
            if os.environ.get('RECORD_TYPE') else os.environ['TYPE']

    if name is None and os.environ.get('NAME'):
        # get name from environment variable
        name = os.environ.get('NAME', None)

    if value is None and os.environ.get('VALUE'):
        # get value from environment variable
        value = os.environ['VALUE']

    if not first_record_only\
            and os.environ.get('FIRST_RECORD_ONLY'):
        # get first_record_only from environment variable
        first_record_only = os.environ['FIRST_RECORD_ONLY']

    if not allow_multiple_records\
            and os.environ.get('ALLOW_MULTIPLE_RECORDS'):
        # get allow_multiple_records from environment variable
        allow_multiple_records = os.environ['ALLOW_MULTIPLE_RECORDS']

    if first_record_only and allow_multiple_records:
        helpers\
            .exit_with_error("This combination of options doesn't make sense.")

    if not search_all_zones\
            and os.environ.get('SEARCH_ALL_ZONES'):
        # get search_all_zones from environment variable
        search_all_zones = os.environ['SEARCH_ALL_ZONES']

    # BEGIN validation #

    # if no record_id exists, ensure that zone_name or zone_id exist,
    # in order to prevent pulling records from multiple zones
    if not record_id and not zone_name and not zone_id\
            and not search_all_zones:
        error_message = "In order to prevent records from being pulled from "\
            "more than one zone, you must specify one (or more) of: "\
            "record_id, zone_id, or zone_name. You can override this "\
            "behavior by assigning a truthy value to 'search_all_zones'."
        helpers.exit_with_error(error_message)

    # ensure that one or more optional parameters exist before doing
    # an indirect lookup
    if not record_id and not search_all_zones and not zone_name\
            and not name and not record_type and not value:
        error_message =\
            "You must provide a record_id or one or more of the following: "\
            "name, record_type (environment variable: TYPE), or value, "\
            "*OR* you must set a truthy value for 'search_all_zones.'"
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
    if (zone_id or zone_name) and (not name and not record_type and not value):
        filtered_records = records
    else:
        filtered_records = []
        for record in records:
            # if record does not meet any one qualifying criterion,
            # then skip over it and continue the loop
            if name and record['name'] != name:
                continue
            if record_type and record['type'] != record_type:
                continue
            if value and record['value'] != value:
                continue
            # if the record has not fail any of the qualifications,
            # then add it to the list
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
        if first_record_only:
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
                "records, or use 'first_record_only' to get only the "\
                "first record. Capitalize these values if using "\
                "environment variables."
            helpers.exit_with_error(error_message)


if __name__ == '__main__':
    record_get()
