# hetzner-dns-tools

This library makes it easier to work with Hetzner's [DNS API](https://dns.hetzner.com/api-docs/), namely Zones and Records.

#### **Project Status: All basic CRUD functionality is complete. Tests still need to be written. Bulk record CREATE options not (yet) supported.**

To be specific, `hetzner-dns-tools` makes it easier to manage your zones/records by name instead of having to get the ID first (although you can do that as well). Also, it allows you to retrieve *only* the IDs if needed, without having to manually parse the JSON first.

Limitations: `hetzner-dns-tools` does not currently do bulk operations (although it can delete records in build), and it does not work with query params (it would be easy to add if you are so inclined). Pull requests and forks are welcomed! :)

These tools are made with Python and are designed to be used in Bash or Python.

All examples in this README assume you are in the root directory of this project when running commands.

## Table of Contents

- [Setup](#setup)
- [Setting Parameters](#setting-parameters)
- [How to Use This Library](#how-to-use-this-library)
- [Project Structure](#project-structure)
- [Converting Results to Human-Readable Output](#converting-results-to-human-readable-output)
- [Usage Guide](#usage-guide)

## Setup

- Ensure you have a [Hetzner DNS API token](https://docs.hetzner.com/dns-console/dns/general/api-access-token/).
- Install the `hetzner-dns-tools` package:
  - Via pip (recommended):
    - `pip install hetzner-dns-tools`
  - Via GitHub:
    - Clone the `hetzner-dns-tools` repo: `git clone https://github.com/arcanemachine/hetzner-dns-tools`
    - Navigate to the root folder of the project.
    - Ensure the python3 `build` module is installed: `python3 -m pip install build`
    - Build the project: `python3 -m build`
    - Install the package: `python3 -m pip install .`

Basic usage example: ` HETZNER_DNS_TOKEN=your-hetzner-dns-token hetzner-dns-tools zone list` (Note: To prevent sensitive data from being saved in your Bash history, ensure that this command begins with a space, or set the [environment variable somewhere else](#setting-environment-variables).

### Run In Docker

- Install [Docker Engine](https://docs.docker.com/engine/install/).
- Start the container and view the logs while the project builds: `docker run --name hetzner-dns-tools -dt arcanemachine/hetzner-dns-tools && docker logs -f hetzner-dns-tools`
- After the project finishes building\* press `Ctrl + C` to exit the logs, and open a bash shell in the same container: `docker exec -it hetzner-dns-tools bash`
  - \*You can exit the logs before the build completes. However, `hetzner-dns-tools` will not be available from the command line until the build is complete.
- From this shell, you can run `hetzner-dns-tools` or open `python3` and `import hetzner_dns_tools`.
- When you are finished, you can stop and destroy the container with `docker stop -t 1 hetzner-dns-tools` and `docker rm hetzner-dns-tools`.

**Note:** This library allows indirect lookups to be performed by domain name or other parameters, which will result in multiple requests being issued. To decrease the run time, use zone IDs and record IDs whenever possible.

## Setting Parameters

There are two methods of setting parameters using this library:
  - Bash environment variables
    - e.g. `HETZNER_DNS_TOKEN=your-hetzner-token hetzner-dns-tools zone list`\*
  - Python arguments
    - e.g. `zone_list(hetzner_dns_token='your-hetzner-token')`

> \*If you are using this library via Bash, you may want to look into something like **[direnv](https://direnv.net/)** in order to prevent your DNS token from leaking into your `~/.bash history`.

Any arguments used when calling a Python function will override the values of any environment variables.

Please note that the `name` parameter is used in Hetzner's DNS API calls (specifically in `zone_create` and `record_create`), while the `zone_name` parameter is only used in `hetzner-dns-tools`.


## How to Use This Library

**All API calls require a `hetzner_dns_token` parameter to be set.**

### In Bash

Simply execute the file you want to run. For example: `hetzner-dns-tools zone list` (Ensure that you set `HETZNER_DNS_TOKEN` environment variable before every command. Read [this section](#setting-environment-variables) to learn more about setting environment variables.) Data can be added to the command by setting environment variables, e.g. `NAME=your-domain.com hetzner-dns-tools zone create`.

To get the Python docstring (ie. help file) for a function, set the environment variable `SHOW_HELP` to a truthy value, e.g. `SHOW_HELP=1 hetzner-dns-tools zone get`

To know whether a script executed successfully or not, run `echo $?` after running a command. If the value of `$?` is `0`, the script executed successfully. If the value of `$?` is `1`, the script exited with an error.

Most errors that occur in the Python code (e.g. if you forget to set an environment variable) will raise an exception and print a stack trace in the console. Other errors will begin with `Error:` and contain a description of the error.


### In Python

```
from hetzner_dns_tools.zone_list import zone_list

# THIS EXAMPLE WILL NOT WORK IF YOU HAVEN'T CREATED ANY HETZNER DNS ZONES

# get zone list
dns_zones = zone_list()['zones']

# parse ID from first zone
your_zone_id = dns_zones[0]['id']

print(your_zone_id)
```

## Project Structure

These tools are namespaced by feature into modules:
  - zone_create, zone_get, and zone_delete
  - record_create, record_get, and record_delete

e.g. Running `hetzner-dns-tools zone list` in Bash will list all available DNS zones. (Make sure to pass your `HETZNER_DNS_TOKEN` as an environment variable)


## Converting Results to Human-Readable Output

The default output is nearly impossible for humans to read. Here's how to format it so it looks better:

### In Bash

This method requires you to have `npm` installed:
  - Install the npm package `json` globally:
    - `npm i -g json`
  - Pipe the output of a command to the newly-installed `json` package:
    - `hetzner-dns-tools zone listjson`

If you know of a better method (particularly one that doesn't require `npm` to be installed), please [submit a ticket](https://github.com/arcanemachine/hetzner-dns-tools/issues/new).


### In Python

```
import json
from hetzner_dns_tools.zone_list import zone_list

# get zone list
dns_zones = zone_list()['zones']

# make it readable
readable_dns_zones = json.dumps(dns_zones, indent=2)

print(readable_dns_zones)
```


## Usage Guide

#### Zones
- [zone_list](#zone_list)
- [zone_create](#zone_create)
- [zone_get](#zone_get)
- [zone_delete](#zone_delete)

#### Records
- [record_list](#record_list)
- [record_create](#record_create)
- [record_get](#record_get)
- [record_delete](#record_delete)

**This section assumes that you have exported the `HETZNER_DNS_TOKEN` environment variable before running any Bash commands. Read [the section on setting Bash environment variables](#setting-environment-variables) if you don't know how to do this.)**

**In Bash, results will be returned as a condensed JSON-formatted string, except when string values (e.g. zone IDs) are requested, or when DELETE actions are performed (will return 'OK' if successful).**

**In Python, results will be returned as a dictionary, except when string values (e.g. zone IDs) are requested, or when DELETE actions are performed (will return 'OK'  if successful.**

## **Zones**

## zone_list

*Get list of all zones.* ([Hetzner Docs API - Get All Zones](https://dns.hetzner.com/api-docs/#tag/Zones))


### In Bash

`hetzner-dns-tools zone list`


### In Python

```
from hetzner_dns_tools.zone_list import zone_list

your_zones = zone_list()

print(your_zones)

```


## zone_create

*Create a new zone.* ([Hetzner DNS API Docs - Create Zone](https://dns.hetzner.com/api-docs/#operation/CreateZone))

> **Required Parameters:** `name/zone_name` (`name` and `zone_name` are interchangeable)

> Optional Parameters: `ttl`

**NOTE:** `zone_create` and `zone_delete` allow the `name` and `zone_name` parameters (or the `NAME` and `ZONE_NAME` environment variables) to be used interchangeably. Note that the `name` parameter is used in Hetzner's API, but `zone_name` is commonly used in this library, so I allow both to be used to reduce the cognitive burden of having to switch from one to the other.


### In Bash

To return all data for the zone: `NAME=your-domain.com hetzner-dns-tools zone create` or `ZONE_NAME=your-domain.com hetzner-dns-tools zone create`

To return just the zone ID: `NAME=your-domain.com ID_ONLY=1 hetzner-dns-tools zone create`

To create a new zone with a custom TTL (default: 86400): `NAME=your-domain.com TTL=57600 hetzner-dns-tools zone create`


### In Python

To get all data for the new zone:

```
from hetzner_dns_tools.zone_create import zone_create

# create a new zone and return all zone data
new_zone = zone_create(hetzner_dns_token='your-token',
                       name='your-domain.com')  # can also use zone_name

# print the name of the new zone
print(new_zone['zone']['name'])  # 'your-domain.com'
```

To return just the ID for the new zone:

```
from hetzner_dns_tools.zone_create import zone_create

# create a new zone and return just the zone_id
new_zone_id = zone_create(hetzner_dns_token='your-token',
                          zone_name='your-domain.com',  # can also use name
                          id_only=True)

# print the ID of the new zone
print(new_zone_id)
```

To create a new zone with a custom TTL (default: 86400):

```
from hetzner_dns_tools.zone_create import zone_create

# create a new zone and return all zone data
new_zone = zone_create(hetzner_dns_token='your-token',
                       name='your-domain.com',  # can also use zone_name
                       ttl=57600)

# print the TTL of the new zone
print(new_zone['zone']['ttl'])  # 57600
```


## zone_get

*Get info about an existing zone.* ([Hetzner DNS API Docs - Get Zone](https://dns.hetzner.com/api-docs/#operation/GetZone))

> **Required Parameters:** One of: `zone_id` or `zone_name`

> Optional Parameters: `id_only`


### In Bash

To return all data for the zone by using the zone ID: `ZONE_ID=your-zone-id hetzner-dns-tools zone get`

To return all data for the zone by using the zone's domain name: `ZONE_NAME=your-domain.com hetzner-dns-tools zone get`

To return just the zone ID by using the zone's domain name: `ZONE_NAME=your-domain.com ID_ONLY=1 hetzner-dns-tools zone get`


### In Python

To return all data for the zone by using the zone ID:

```
from hetzner_dns_tools.zone_get import zone_get

zone = zone_get(hetzner_dns_token='your-token',
                zone_id='your-zone-id')

# print the name of the zone
print(zone['zone']['name'])
```


To return all data for the zone by using the zone's domain name:

```
from hetzner_dns_tools.zone_get import zone_get

zone = zone_get(hetzner_dns_token='your-token',
                zone_name='your-domain.com')

# print the ID of the zone
print(zone['zone']['id'])
```


To return just the zone ID by using the zone's domain name:

```
from hetzner_dns_tools.zone_get import zone_get

zone_id = zone_get(hetzner_dns_token='your-token',
                   zone_name='your-domain.com',
                   id_only=True)

# print the ID of the zone
print(zone_id)
```


## zone_update

To update a zone, use `zone_delete` to delete a zone, and then use `zone_create` to create a new one. (I had some issues getting the function to work with Hetzner's backend (it wouldn't allow any changes to be made), plus the ability to delete and create records effectively makes the update function redundant. If you want to try to implement the function yourself, there is a `zone_update.py` file in the [experimental-functions](https://github.com/arcanemachine/hetzner-dns-tools/tree/experimental-functions) branch that may be of some help.


## zone_delete

*Delete an existing zone.* ([Hetzner DNS API Docs - Delete Zone](https://dns.hetzner.com/api-docs/#operation/DeleteZone))

> **Required Parameters:** One of: `zone_id` or `zone_name/name`

Zones can be deleted directly using a `zone_id`, or can be done indirectly by using any of the *Optional Parameters* as a lookup.

Successful delete operations will return the string 'OK', and unsuccessful delete operations will raise a `ValueError` exception.

**NOTE:** `zone_create` and `zone_delete` allow the `name` and `zone_name` parameters (or the `NAME` and `ZONE_NAME` environment variables) to be used interchangeably. Note that the `name` parameter is used in Hetzner's API, but `zone_name` is commonly used in this library, so I allow both to be used to reduce the cognitive burden of having to switch from one to the other.


### In Bash

To delete a zone by its zone ID: `ZONE_ID=your-zone-id hetzner-dns-tools zone delete`

To delete a zone by its zone (ie. domain) name: `ZONE_NAME=your-domain.com hetzner-dns-tools zone delete` or `NAME=your-domain.com hetzner-dns-tools zone delete`


### In Python

To delete a zone by its zone ID:

```
from hetzner_dns_tools.zone_delete import zone_delete

zone_delete(hetzner_dns_token='your-token',
            zone_id='your-zone-id')
```

To delete a zone by its zone (ie. domain) name:

```
from hetzner_dns_tools.zone_delete import zone_delete

zone_delete(hetzner_dns_token='your-token',
            zone_name='your-domain.com')  # can also use 'name'
```


## **Records**

## record_list

*Get list of all records.* ([Hetzner DNS API Docs - Get All Records](https://dns.hetzner.com/api-docs/#operation/GetRecords))

> **Required Parameters:** One of: `zone_id` or `zone_name`


### In Bash

To return all data for all zones: `hetzner-dns-tools record list`

To return all data for a single zone, by zone ID: `ZONE_ID=your-zone-id hetzner-dns-tools record list`

To return all data for a single zone, by zone (ie. domain) name: `ZONE_NAME=your-domain.com hetzner-dns-tools record list`


### In Python

To return all data for all zones:

```
from hetzner_dns_tools.record_list import record_list

records = record_list(hetzner_dns_token='your-token')

print(records)
```

To return all data for a single zone, by zone ID:

```
from hetzner_dns_tools.record_list import record_list

records = record_list(hetzner_dns_token='your-token',
                      zone_id='your-zone-id')

print(records)
```

To return all data for a single zone, by zone (ie. domain) name:

```
from hetzner_dns_tools.record_list import record_list

records = record_list(hetzner_dns_token='your-token',
                      zone_name='your-domain.com')

print(records)
```


## record_create

*Create a new record.* ([Hetzner DNS API Docs - Create Record](https://dns.hetzner.com/api-docs/#operation/CreateRecord))

> **Required Parameters:** `hetzner_dns_token`, `record_type`, `value`, `zone_id`

> Optional Parameters: `zone_name`, `name`\*, `ttl`, `id_only`\
>\
>**\*If `name` is not specified, the root value `@` will be used (except for MX records).**

To get the ID of the zone you want to create the record in, you can use `zone_name` to do an indirect lookup an obtain the `zone_id`. Note that doing this will result in an additional request being made.

**Note:** Hetzner's DNS API requires a the `type` parameter to specify the type of record (e.g. A, AAAA, CNAME, MX, etc.). Because the word `type` is a reserved keyword in Python, the `record` functions all use the `record_type` parameter instead. When using environment variables, either `TYPE` or `RECORD_TYPE` may be used interchangeably.


### In Bash

To create an `A` record for zone ID `your-zone-id` with name `www` and value `1.1.1.1`, and return all record data: `ZONE_ID=your-zone-id TYPE=A NAME=www VALUE=1.1.1.1 hetzner-dns-tools record create`

To return just the record ID after creating the record: `ZONE_ID=your-zone-id RECORD_TYPE=A NAME=www VALUE=1.1.1.1 ID_ONLY=1 hetzner-dns-tools record create`

To create a new record with a custom TTL (default is `86400`), use `TTL`: `ZONE_ID=your-zone-id TYPE=A NAME=www VALUE=1.1.1.1 TTL=57600 hetzner-dns-tools record create`

To create a MX record with a target of `your-domain.com` and a priority of `10`, both values must be entered as such in the `VALUE` field: `ZONE_ID=your-zone-id TYPE=MX VALUE="10 your-mail-server.com" hetzner-dns-tools record create`

To create a SRV record with a priority of `1`, a weight of `2`, at port `3` for a target `your-server.com`, all values must be entered in this order in the `VALUE` field:  `ZONE_ID=your-zone-id TYPE=SRV VALUE="1 2 3 your-server.com" hetzner-dns-tools record create`


### In Python

To create an `A` record for zone ID `your-zone-id` with name `www` and value `1.1.1.1`, and return all record data:

```
from hetzner_dns_tools.record_create import record_create

# create a new record and return all record data
new_record = record_create(hetzner_dns_token='your-token',
                           zone_id='your-zone-id',
                           record_type='A',
                           name='www',
                           value='1.1.1.1')

# print the record's 'created' value
print(new_record['record']['created'])
```

To return just the record ID after creating the record:

```
from hetzner_dns_tools.record_create import record_create

# create a new record and return all record data
new_record_id = record_create(hetzner_dns_token='your-token',
                              zone_id='your-zone-id',
                              record_type='A',
                              name='www',
                              value='1.1.1.1',
                              id_only=True)

# print the new record's ID
print(new_record_id)
```

To create a new MX record with server `your-mail-server.com` and priority `10`:

```
from hetzner_dns_tools.record_create import record_create

# create a new record and return all record data
new_record = record_create(hetzner_dns_token='your-token',
                           zone_id='your-zone-id',
                           record_type='MX',
                           value='10 your.mail-server.com')
```

To create a SRV record with a priority of `1`, a weight of `2`, at port `3` for a target `your-server.com`:

```
from hetzner_dns_tools.record_create import record_create

# create a new record and return all record data
new_record = record_create(hetzner_dns_token='your-token',
                           zone_id='your-zone-id',
                           record_type='SRV',
                           value='1 2 3 your.server.com')
```


## record_get

*Get info about an existing record.* ([Hetzner DNS API Docs - Get Record](https://dns.hetzner.com/api-docs/#operation/GetRecord))

> **Required\* Parameters:** One of: `record_id` or `zone_id` or `zone_name`

> Optional Parameters:\
> &emsp;Filters: `record_type`, `name`, `value`, `ttl`\
> &emsp;Formats: `id_only`\
> &emsp;Options: `first_record_only`, `allow_multiple_records`, `search_all_zones`\*\
>\
>**\*If the `search_all_zones` parameter is given a truthy value, then you do not need to include any of the *Required Parameters*, as their purpose is to ensure that records are only returned for a single zone.**

**Note:** This function will raise an exception if multiple records are returned, \*unless\* the `first_record_only` \*or\* `allow_multiple_records` parameters are truthy.


### **Options**

These parameters can be given truthy values to enable them:

`allow_multiple_records` - If multiple records are returned, return all of them.
`first_record_only` - Return only the first record found. (There is no guarantee of any ordering.)
`search_all_zones` - Allow records to be returned from all zones. No required parameters are needed when using this option.
`id_only` - Returns only the ID of the given record. If this argument and `allow_multiple_records` are both truthy, a list of record IDs will be returned.


### In Bash

To return all data for single record via the record's ID: `RECORD_ID=your-record-id hetzner-dns-tools record get`

To return all MX records for a zone by using a zone ID as a lookup: `ZONE_ID=your-zone-id TYPE=MX ALLOW_MULTIPLE_RECORDS=1 hetzner-dns-tools record get`

To return a zone's A record with a name of 'www' by using a zone (ie. domain) name as a lookup: `ZONE_NAME=your-domain.com TYPE=A NAME=www hetzner-dns-tools record get`

To return all record IDs for a zone by using a zone ID as a lookup: `ZONE_ID=your-zone-id ALLOW_MULTIPLE_RECORDS=1 ID_ONLY=1 hetzner-dns-tools record get`

To return all A records from all zones with a name of '@' (root): `TYPE=A NAME="@" SEARCH_ALL_ZONES=1 ALLOW_MULTIPLE_RECORDS=1 hetzner-dns-tools record get`

To return the first returned A record with a value of `1.2.3.4` and a TTL of `57600` by using a zone (ie. domain) name as a lookup: `ZONE_NAME=your-domain.com TYPE=A VALUE=1.2.3.4 TTL=57600 FIRST_RECORD_ONLY=1 hetzner-dns-tools record get`


### In Python

To return all data for single record via the record's ID:

```
from hetzner_dns_tools.record_get import record_get

record = record_get(hetzner_dns_token='your-token',
                    record_id='your-record-id')
```

To return all MX records for a zone by using a zone ID as a lookup:

```
from hetzner_dns_tools.record_get import record_get

records = record_get(hetzner_dns_token='your-token',
                     zone_id='your-zone-id',
                     record_type='MX',
                     allow_multiple_records=True)
```


To return a zone's A record with a name of 'www' by using a zone (ie. domain) name as a lookup:

```
from hetzner_dns_tools.record_get import record_get

record = record_get(hetzner_dns_token='your-token',
                    zone_id='your-zone-id',
                    record_type='A',
                    name='www')
```

To return all MX records for a zone by using a zone ID as a lookup:

```
from hetzner_dns_tools.record_get import record_get

records = record_get(hetzner_dns_token='your-token',
                     zone_id='your-zone-id',
                     record_type='MX',
                     allow_multiple_records=True)
```


To return all record IDs for a zone by using a zone ID as a lookup:

```
from hetzner_dns_tools.record_get import record_get

# this value will contain a list of zone IDs
record_ids = record_get(hetzner_dns_token='your-token',
                        zone_id='your-zone-id',
                        allow_multiple_records=True,
                        id_only=True)
```

To return all record IDs for a zone by using a zone ID as a lookup:

```
from hetzner_dns_tools.record_get import record_get

# this value will contain a list of zone IDs
record_ids = record_get(hetzner_dns_token='your-token',
                        zone_id='your-zone-id',
                        allow_multiple_records=True,
                        id_only=True)
```

To return all A records from all zones with a name of '@' (root):

```
from hetzner_dns_tools.record_get import record_get

# this value will contain a list of zone IDs
record_ids = record_get(hetzner_dns_token='your-token',
                        search_all_zones=True,
                        record_type='A',
                        name='@',
                        allow_multiple_records=True)
```

To return the first record with a value of `1.2.3.4` and a TTL of `57600` by using a zone (ie. domain) name as a lookup:

```
from hetzner_dns_tools.record_get import record_get

# this value will contain a list of zone IDs
record_ids = record_get(hetzner_dns_token='your-token',
                        zone_name='your-domain.com',
                        value='1.2.3.4',
                        ttle=57600,
                        first_record_only=True)
```


## record_update

As with the `zone` modules, you can use `record_delete` and `record_create` to update a record. This library does not currently have a native `record_update` module.


## record_delete

*Delete an existing record.* ([Hetzner DNS API Docs - Delete Record](https://dns.hetzner.com/api-docs/#operation/DeleteRecord))

> **Required\* Parameters:** One of: `record_id` or `zone_id` or `zone_name`

> Optional Parameters:\
>   &emsp;Filters: `record_type`, `name`, `value` (but not `ttl`\*)\
>   &emsp;Options: `delete_multiple_records`, `first_record_only`, `search_all_zones`\**

Records can be deleted directly using a `record_id`, or can be done indirectly by using any of the *Optional Parameters* as a lookup.

Successful delete operations will return the string 'OK', and unsuccessful delete operations will raise a `ValueError` exception.

\*Due to how `record_list` returns its results, `ttl` is not an available option for filtering records

\*\*If the `search_all_zones` parameter is given a truthy value, then you do not need to include any of the *Required Parameters*, as their purpose is to ensure that records are only returned for a single zone.

**Note:** This function will raise an exception if multiple records are returned, \*unless\* the `first_record_only` \*or\* `allow_multiple_records` parameters are truthy.


### **Options**

These parameters can be given truthy values to enable them:

`delete_multiple_records` - Delete all matching records, even if there is more than one record returned.
`first_record_only` - Delete only the first record returned. (There is no guarantee of any ordering.)
`search_all_zones` - Allow records to be returned from all zones. None of "required" parameters are needed when using this option.


### In Bash

To delete a record by using its record ID: `RECORD_ID=your-record-id hetzner-dns-tools record delete`

To delete a zone's A record with a name of 'www' by using a zone (ie. domain) name as a lookup: `ZONE_NAME=your-domain.com TYPE=A NAME=www hetzner-dns-tools record delete`

To delete all MX records for a zone by using a zone ID as a lookup: `ZONE_ID=your-zone-id TYPE=MX DELETE_MULTIPLE_RECORDS=1 hetzner-dns-tools record delete`

To delete all CNAME records from all zones: `TYPE=CNAME SEARCH_ALL_ZONES=1 DELETE_MULTIPLE_RECORDS=1 hetzner-dns-tools record delete`

To delete the first returned A record with a value of `1.2.3.4` by using a zone (ie. domain) name as a lookup: `ZONE_NAME=your-domain.com TYPE=A VALUE=1.2.3.4 FIRST_RECORD_ONLY=1 hetzner-dns-tools record delete`


## In Python

To delete a record by using the record ID:

```
from hetzner_dns_tools.record_delete import record_delete

record_delete(hetzner_dns_token='your-token',
              record_id='your-record-id')
```

To delete a zone's A record with a name of 'www' by using a zone (ie. domain) name as a lookup:

```
from hetzner_dns_tools.record_delete import record_delete

record_delete(hetzner_dns_token='your-token',
              zone_name='your-domain.com',
              record_type='A',
              name='www')
```

To delete all MX records for a zone by using a zone ID as a lookup:

```
from hetzner_dns_tools.record_delete import record_delete

record_delete(hetzner_dns_token='your-token',
              zone_id='your-zone-id',
              record_type='MX',
              delete_multiple_records=True)
```

To delete all A records from all zones with a name of '@' (root):

```
from hetzner_dns_tools.record_delete import record_delete

# will raise ValueError return 'OK' if delete operation was successful
record_delete(hetzner_dns_token='your-token',
              record_type='A',
              name='@',
              search_all_zones=True)
```

To delete the first returned A record with a value of `1.2.3.4` by using a zone (ie. domain) name as a lookup:

```
from hetzner_dns_tools.record_delete import record_delete

# will raise ValueError return 'OK' if delete operation was successful
record_delete(hetzner_dns_token='your-token',
              zone_name='your-domain.com',
              record_type='A',
              value='1.2.3.4',
              first_record_only=True)
```
\
\
(c) 2022 arcanemachine. Freely distributed under the terms of the [MIT Licence](https://mit-license.org/).
