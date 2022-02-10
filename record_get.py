#!/usr/bin/python3

import json
import os
import requests
import sys

import hetzner_dns_helpers as helpers


def record_get(hetzner_dns_token=None,
               record_id=None,
               zone_id=None,
               zone_name=None,
               name=None,
               ttl=None,
               record_type=None,
               value=None,
               allow_multiple_records=False,
               id_only=False):
    """
    Get info about an existing record.
    https://dns.hetzner.com/api-docs/#operation/GetRecord

    - Lookups can be performed directly with 'record_id', or indirectly
      using a combination of 'name', 'ttl', 'record_type', 'value',
      'zone_id', and 'zone_name'.

    - If indirect lookups are performed, an exception will be raised if
      multiple records are returned, *UNLESS* you specify a truthy
      value for the 'allow_multiple_records' parameter.

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

    if allow_multiple_records is None\
            and os.environ.get('ALLOW_MULTIPLE_RECORDS'):
        # get allow_multiple from environment variable
        allow_multiple_records = os.environ['ALLOW_MULTIPLE_RECORDS']

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

            # when running via the terminal, print output to console then exit
            if __name__ == '__main__':
                print(decoded_response)
                sys.exit(0)  # exit successfully

            return response_dict

        except requests.exceptions.RequestException as err:
            helpers.handle_request_exception(err)

    # TODO: do an indirect lookup of all records and filter via given params
    else:
        from record_list import record_list
        from zone_get import zone_get

        # if zone_name passed, lookup the zone that matches it to get zone_id
        if zone_name:
            zone = zone_get(zone_name=zone_name)
            if not zone_id:
                zone_id = zone['zone']['id']
            elif zone_id != zone['zone']['id']:
                error_message =\
                    "The zone_id you entered does not match the zone_id of "\
                    "the zone_name you entered."
                if __name__ == '__main__':
                    print(f"Error: {error_message}")
                    sys.exit(1)  # exit with error
                else:
                    raise ValueError(error_message)

        records = record_list(hetzner_dns_token=hetzner_dns_token,
                              zone_id=zone_id)['records']

        # iterate over the given parameters, adding any matchine records that
        # are not yet in the list
        filtered_records = []
        if zone_id:
            for record in records:
                if record['zone_id'] == zone_id\
                        and record not in filtered_records:
                    filtered_records.append(record)
        if zone_name:
            for record in records:
                if record['zone_name'] == zone_name\
                        and record not in filtered_records:
                    filtered_records.append(record)
        if name:
            for record in records:
                if record['name'] == name and record not in filtered_records:
                    filtered_records.append(record)
        if ttl:
            for record in records:
                if record['ttl'] == ttl and record not in filtered_records:
                    filtered_records.append(record)
        if record_type:
            for record in records:
                if record['type'] == record_type\
                        and record not in filtered_records:
                    filtered_records.append(record)
        if value:
            for record in records:
                if record['value'] == value and record not in filtered_records:
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
            # when running via the terminal, print output to console then exit
            if __name__ == '__main__':
                print(filtered_records[0])
                sys.exit(0)  # exit successfully
            return filtered_records[0]

        # if multiple records found, raise an exception unless
        # 'allow_multiple_records' is truthy
        if len(filtered_records) > 1:
            if allow_multiple_records:
                # when running via the terminal, print output to console,
                # then exit
                if __name__ == '__main__':
                    print(filtered_records)
                    sys.exit(0)  # exit successfully
                return filtered_records
            else:
                error_message =\
                    "Multiple requests returned. If you want to allow "\
                    "multiple records, pass in the allow_multiple_records "\
                    "parameter or set the ALLOW_MULTIPLE_RECORDS environment "\
                    "variable."
                if __name__ == '__main__':
                    print(f"Error: {error_message}")
                    sys.exit(1)  # exit with error
                else:
                    raise ValueError(error_message)


if __name__ == '__main__':
    record_get()
