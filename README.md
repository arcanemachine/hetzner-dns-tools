# hetzner-dns-cli

### **Project Status: All basic CRUD functionality is complete. Tests still need to be written. Bulk record CREATE options not yet supported.**

This library makes it easier to work with Hetzner's [DNS API](https://dns.hetzner.com/api-docs/), namely Zones and Records.

To be specific, **hetzner-dns-cli** makes it easier to manage your zones/records by name instead of having to get the ID first (although you can do that as well). Also, it allows you to retrieve *only* the IDs if needed, without having to manually parse the JSON first.

Limitations: **hetzner-dns-cli** does not currently do bulk operations (although it can delete records in build), and it does not work with query params (it would be easy to add if you are so inclined). Pull requests and forks are welcomed! :)**

These tools are made with Python and are designed to be used in Bash or Python.

**In Bash, results will be returned as a condensed JSON-formatted string, except when string values (e.g. zone IDs) are requested, or when DELETE actions are performed (will return 'OK' if successful).**

**In Python, results will be returned as a dictionary, except when string values (e.g. zone IDs) are requested, or when DELETE actions are performed (will return 'OK'  if successful.**

All examples in this README assume you are in the root directory of this project when running commands.

## Table of Contents

- [Setup](#setup)
- [How to Set Environment Variables in Bash](#how-to-set-environment-variables-in-bash)
- [Setting Parameters](#setting-parameters)
- [How to Use This Library](#how-to-use-this-library)
- [Project Structure](#project-structure)
- [Converting Results to Human-Readable Output](#converting-results-to-human-readable-output)
- [Usage Guide](#usage-guide)
- [Using in Python Modules](#using-in-python-modules)

## Setup

- Ensure the `requests` Python library is installed: `pip install requests`

- Clone the repo to a folder of your choice: `git clone https://github.com/arcanemachine/hetzner-dns-cli`.

- Navigate to the folder and run the command you want to use.

Example (from project root folder): ` HETZNER_DNS_TOKEN=your-hetzner-dns-token ./zone_list.py` (Note: To prevent sensitive data from being saved in your Bash history, ensure that this command begins with a space, or set the [environment variable somewhere else](#setting-environment-variables).

**All API calls require a `HETZNER_DNS_TOKEN` parameter to be set.**


## How to Set Environment Variables in Bash

If you already know about Bash environment variables, you can safely skip this section. If you don't, you should read this section to avoid leaking your DNS token in your bash history.

### Setting environment variables

**NOTE:** The order of environment variables does not matter: `A=1 B=2 ./your-command.sh` will yield the same results as `B=2 A=1 ./your-command.sh`.

#### For a single command

To set an environment variable for a single command, just enter the key-value pair before the command you want to run. For example: `HETZNER_DNS_TOKEN=your-hetzner-dns-token ./zone_list.py` **(WARNING: This command will be saved to your Bash history! Continue reading to learn how to avoid this)**

To avoid saving the item to your bash history, begin the command with a space:

Example: ` HETZNER_DNS_TOKEN=your-hetzner-dns-token ./zone_list.py` (Make sure there is a space at the beginning!)

Please note that this method of setting environment variables is cumbersome and error-prone. Continue reading to learn better and easier ways of setting environment variables.


#### Setting persistent environment variables

##### For the current terminal session

You can set environment variables in a shell script, and use `source` to load them into the current session:

For example, in a file called `my-env.sh`:

```export HETZNER_DNS_TOKEN=your-hetzner-dns-token```

Then, run the command `source my-env.sh` to load the environment variable into your current session.

Now, simply running the command `./zone_list.py` will automatically pass the `HETZNER_DNS_TOKEN` (or any other environment variables) to the command.


##### **Recommended:** Use `direnv` for easy use across multiple sessions

[Direnv](https://direnv.net/) is a simple and effective program that automatically loads environment variables when you `cd` into a certain directory or any of its subdirectories.

After setting up direnv, navigate to any folder in this project and run this command to enable direnv for this project: `direnv allow`

To automatically add your `HETZNER_DNS_TOKEN` whenever you are in the root folder of this project (or a subdirectory of it), create a `.env` file in the root folder of this project that looks like this:

`HETZNER_DNS_TOKEN=your-hetzner-dns-token`

***Note: Any environment variables saved in `.envrc` will be committed to the repo unless you modify this project's `.gitignore` file. We recommend that you save your secrets in a `.env` file or modify the `.gitignore` to prevent your secrets from ending up in a copy of this repo.***


## Setting parameters

There are two methods of settings parameters when making API calls:
  - Environment variables (required when using these tools from Bash)
  - Python arguments

If using Python, any arguments used when calling a function will override the values of any environment variables.

Please note that the `name` parameter is used in Hetzner's DNS API calls (specifically in `zone_create`), while the `zone_name` parameter is only used in **hetzner-dns-cli**.

Again: **All API calls require a `HETZNER_DNS_TOKEN` parameter to be set.**


## How to Use This Library

**Note:** This library allows indirect lookups to be performed by domain name or other parameters, which will result in multiple requests being issued. To decrease the run time, use zone IDs and record IDs whenever possible.

### In a Bash prompt

Simply execute the file you want to run. For example: `./zone_list.py` (Ensure that you set `HETZNER_DNS_TOKEN` environment variable for every command. Read [this section](#setting-environment-variables) to learn more about setting environment variables.) Data can be added to the command by setting environment variables, e.g. `NAME=your-domain.com ./zone_create.py`.

To get the Python docstring (ie. help file) for a function, set the environment variable `SHOW_HELP` to a truthy value, e.g. `SHOW_HELP=1 ./zone_get.py`

To know whether a script executed successfully or not, run `echo $?` after running a command. If the value of `$?` is `0`, the script executed successfully. If the value of `$?` is `1`, the script exited with an error.

Most errors that occur in the Python code (e.g. if you forget to set an environment variable) will raise an exception and print a stack trace in the console. Other errors will begin with `Error: ` and contain a description of the error.


### In Python

Either add this project's root folder to your Python PATH, or navigate to this project's root folder before running a script like this:

```
from zone_list import zone_list

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

e.g. Running `./zone_list.py` in Bash will list all available DNS zones. (Make sure to pass your `HETZNER_DNS_TOKEN` as an environment variable)


## Converting Results to Human-Readable Output

The default output is nearly impossible for humans to read. Here's how to format it so it looks better:

### In a Bash prompt

This method requires you to have `npm` installed:
  - Install the npm package `json`:
    - `npm i -g json`
  - Pipe the output of a command to `json`:
    - `./zone_list | json`

If you know of a better method (particularly one that doesn't require `npm` to be installed), please [submit a ticket](https://github.com/arcanemachine/hetzner-dns-cli/issues/new).


### In Python code

```
import json
from zone_list import zone_list

# get zone list
dns_zones = zone_list()['zones']

# make it readable
readable_dns_zones = json.dumps(dns_zones, indent=2)

print(readable_dns_zones)
```


## Usage Guide

- [Zones](#zones)
- [zone_list](#zone-create)
- [zone_create](#zone-create)
- [zone_get](#zone-get)
- [zone_delete](#zone-delete)

- [Records](#records)
- [record_list](#record-list)
- [record_create](#record-create)
- [record_get](#record-get)
- [record_delete](#record-delete)

**This section assumes that you have exported the `HETZNER_DNS_TOKEN` environment variable before running any Bash commands. Read [this section](#setting-environment-variables) if you don't know how to do this.)**

#### zone_list

Get list of all zones.

##### In a Bash prompt

`./zone_list.py`

#### In Python

```
from zone_list import zone_list

your_zones = zone_list()

print(your_zones)

```


#### zone_create

Create a new zone.

Required Parameters: `name/zone_name` (`name` and `zone_name` are interchangeable)
Optional Parameters: `ttl`

**NOTE:** `zone_create` and `zone_delete` allow the `name` and `zone_name` parameters (or the `NAME` and `ZONE_NAME` environment variables) to be used interchangeably. Note that the `name` parameter is used in Hetzner's API, but `zone_name` is commonly used in this library, so I allow both to be used to reduce the cognitive burden of having to switch from one to the other.

##### In a Bash prompt

To return all data for the zone: `NAME=your-domain.com ./zone_create.py` or `ZONE_NAME=your-domain.com ./zone_create.py`

To return just the zone ID: `NAME=your-domain.com ID_ONLY=1 ./zone_create.py`

To create a new zone with a custom TTL (default: 86400): `NAME=your-domain.com TTL=57600 ./zone_create.py`

#### In Python

To get all data for the new zone:

```
from zone_create import zone_create

# create a new zone and return all zone data
new_zone = zone_create(hetzner_dns_token='your-token',
                       name='your-domain.com')  # can also use zone_name

# print the name of the new zone
print(new_zone['zone']['name'])  # 'your-domain.com'

```

To return just the ID for the new zone:

```
from zone_create import zone_create

# create a new zone and return just the zone_id
new_zone_id = zone_create(hetzner_dns_token='your-token',
                          zone_name='your-domain.com',  # can also use name
                          id_only=True)

# print the ID of the new zone
print(new_zone_id)

```

To create a new zone with a custom TTL (default: 86400):

```
from zone_create import zone_create

# create a new zone and return all zone data
new_zone = zone_create(hetzner_dns_token='your-token',
                       name='your-domain.com',  # can also use zone_name
                       ttl=57600)

# print the TTL of the new zone
print(new_zone['zone']['ttl'])  # 57600

```


#### zone_get

Get info about an existing zone.

Required Parameters: One of: `zone_id` or `zone_name`
Optional Parameters: `id_only`

##### In a Bash prompt

To return all data for the zone by using the zone ID: `ZONE_ID=your-zone-id ./zone_get.py`

To return all data for the zone by using the zone's domain name: `ZONE_NAME=your-domain.com ./zone_get.py`

To return just the zone ID by using the zone's domain name: `ZONE_NAME=your-domain.com ID_ONLY=1 ./zone_get.py`

#### In Python

To return all data for the zone by using the zone ID:

```
from zone_get import zone_get

zone = zone_get(hetzner_dns_token='your-token',
                zone_id='your-zone-id')

# print the name of the zone
print(zone['zone']['name'])

```


To return all data for the zone by using the zone's domain name:

```
from zone_get import zone_get

zone = zone_get(hetzner_dns_token='your-token',
                zone_name='your-domain.com')

# print the ID of the zone
print(zone['zone']['id'])
```


To return just the zone ID by using the zone's domain name:

```
from zone_get import zone_get

zone_id = zone_get(hetzner_dns_token='your-token',
                   zone_name='your-domain.com',
                   id_only=True)

# print the ID of the zone
print(zone_id)
```


#### zone_update

To update a zone, use `zone_delete` to delete a zone, and then use `zone_create` to create a new one.

There is a `zone_update.py` file in the `unstable` branch, but I was not able to get it to work because the API wouldn't allow any changes. Perhaps I made an mistake in my implementation. However, `zone_delete` + `zone_create` do the job just fine for me, so I just use those.


#### zone_delete

Delete an existing zone.

Zones can be deleted directly using a `zone_id`, or can be done indirectly by using any of the *Optional Parameters* as a lookup.

Successful delete operations will return the string 'OK', and unsuccessful delete operations will raise a `ValueError` exception.

Required Parameters: `zone_id *or* name/zone_name` (`name` and `zone_name` are interchangeable)

**NOTE:** `zone_create` and `zone_delete` allow the `name` and `zone_name` parameters (or the `NAME` and `ZONE_NAME` environment variables) to be used interchangeably. Note that the `name` parameter is used in Hetzner's API, but `zone_name` is commonly used in this library, so I allow both to be used to reduce the cognitive burden of having to switch from one to the other.


### Records

#### record_list

Get list of all records.

Required Parameters: One of: `zone_id` or `zone_name`

##### In a Bash prompt

To return all data for all zones: `./record_list.py`

To return all data for a single zone, by zone ID: `ZONE_ID=your-zone-id ./record_list.py`

To return all data for a single zone, by zone (ie. domain) name: `ZONE_NAME=your-domain.com ./record_list.py`

#### In Python

To return all data for all zones:

```
from record_list import record_list

records = record_list(hetzner_dns_token='your-token')

print(records)
```

To return all data for a single zone, by zone ID:

```
from record_list import record_list

records = record_list(hetzner_dns_token='your-token',
                      zone_id='your-zone-id')

print(records)
```

To return all data for a single zone, by zone (ie. domain) name:

```
from record_list import record_list

records = record_list(hetzner_dns_token='your-token',
                      zone_name='your-domain.com')

print(records)
```


#### record_create

Create a new record.

Required Parameters: `hetzner_dns_token`, `name`, `record_type`, `value`, `zone_id`
Optional Parameters: `zone_name`, `ttl`, `id_only`

To get the ID of the zone you want to create the record in, you can use `zone_name` to do an indirect lookup an obtain the `zone_id`. Note that doing this will result in an additional request being made.

**Note:** Hetzner's DNS API requires a the `type` parameter to specify the type of record (e.g. A, AAAA, CNAME, MX, etc.). Because the word `type` is a reserved keyword in Python, the `record` functions all use the `record_type` parameter instead. When using environment variables, either `TYPE` or `RECORD_TYPE` may be used interchangeably.

##### In a Bash prompt

To create an `A` record for zone ID `your-zone-id` with name `www` and value `1.1.1.1`, and return all record data: `ZONE_ID=your-zone-id TYPE=A NAME=www VALUE=1.1.1.1 ./record_create.py`

To return just the record ID after creating the record: `ZONE_ID=your-zone-id RECORD_TYPE=A NAME=www VALUE=1.1.1.1 ID_ONLY=1 ./record_create.py`

To create a new zone with a custom TTL (default is `86400`) and return all record data: `ZONE_ID=your-zone-id TYPE=A NAME=www VALUE=1.1.1.1 TTL=57600 ./record_create.py`

#### In Python

To create an `A` record for zone ID `your-zone-id` with name `www` and value `1.1.1.1`, and return all record data:

```
from record_create import record_create

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
from record_create import record_create

# create a new record and return all record data
new_record_id = record_create(hetzner_dns_token='your-token',
                              zone_id='your-zone-id',
                              record_type='A',
                              name='www',
                              value='1.1.1.1',
                              id_only=True)

# print the record's ID
print(new_record_id)
```

To create a new zone with a custom TTL (default is `86400`) and return all record data:

```
from record_create import record_create

# create a new record and return all record data
new_record = record_create(hetzner_dns_token='your-token',
                           zone_id='your-zone-id',
                           record_type='A',
                           name='www',
                           value='1.1.1.1',
                           ttl=57600)

# print the record's 'ttl' value
print(new_record['record']['ttl'])  # 57600
```


#### record_get

Get info about an existing record.

Required\* Parameters: One of: `record_id` or `zone_id` or `zone_name`
Optional Parameters: {
  Filters: `record_type`, `name`, `value`, `ttl`,
  Formats: `id_only`
  Options: `first_record_only`, `allow_multiple_records`, `search_all_zones`\*
}

\*If the `search_all_zones` parameter is given a truthy value, then you do not need to include any of the *Required Parameters*, as their purpose is to ensure that records are only returned for a single zone.

**Note:** This function will raise an exception if multiple records are returned, \*unless\* the `first_record_only` \*or\* `allow_multiple_records` parameters are truthy.


##### Options

These parameters can be given truthy values to enable them:

`allow_multiple_records` - If multiple records are returned, return all of them.
`first_record_only` - Return only the first record found. (There is no guarantee of any ordering.)
`search_all_zones` - Allow records to be returned from all zones. No required parameters are needed when using this option.
`id_only` - Returns only the ID of the given record. If this argument and `allow_multiple_records` are both truthy, a list of record IDs will be returned.


##### In a Bash prompt

To return all data for single record via the record's ID: `RECORD_ID=your-record-id ./record_get.py`

To return all MX records for a zone by using a zone ID as a lookup: `ZONE_ID=your-zone-id TYPE=MX ALLOW_MULTIPLE_RECORDS=1 ./record_get.py`

To return a zone's A record with a name of 'www' by using a zone (ie. domain) name as a lookup: `ZONE_NAME=your-domain.com TYPE=A NAME=www ./record_get.py`

To return all record IDs for a zone by using a zone ID as a lookup: `ZONE_ID=your-zone-id ALLOW_MULTIPLE_RECORDS=1 ID_ONLY=1 ./record_get.py`

To return all A records from all zones with a name of '@' (root): `TYPE=A NAME="@" SEARCH_ALL_ZONES=1 ALLOW_MULTIPLE_RECORDS=1 ./record_get.py`

To return the first returned A record with a value of `1.2.3.4` and a TTL of `57600` by using a zone (ie. domain) name as a lookup: `ZONE_NAME=your-domain.com TYPE=A VALUE=1.2.3.4 TTL=57600 FIRST_RECORD_ONLY=1 ./record_get.py`

#### In Python

To return all data for single record via the record's ID:

```
from record_get import record_get

record = record_get(hetzner_dns_token='your-token',
                    record_id='your-record-id')
```

To return all MX records for a zone by using a zone ID as a lookup:

```
from record_get import record_get

records = record_get(hetzner_dns_token='your-token',
                     zone_id='your-zone-id',
                     record_type='MX',
                     allow_multiple_records=True)
```


To return a zone's A record with a name of 'www' by using a zone (ie. domain) name as a lookup:

```
from record_get import record_get

record = record_get(hetzner_dns_token='your-token',
                    zone_id='your-zone-id',
                    record_type='A',
                    name='www')
```

To return all MX records for a zone by using a zone ID as a lookup:

```
from record_get import record_get

records = record_get(hetzner_dns_token='your-token',
                     zone_id='your-zone-id',
                     record_type='MX',
                     allow_multiple_records=True)
```


To return all record IDs for a zone by using a zone ID as a lookup:

```
from record_get import record_get

# this value will contain a list of zone IDs
record_ids = record_get(hetzner_dns_token='your-token',
                        zone_id='your-zone-id',
                        allow_multiple_records=True,
                        id_only=True)
```

To return all record IDs for a zone by using a zone ID as a lookup:

```
from record_get import record_get

# this value will contain a list of zone IDs
record_ids = record_get(hetzner_dns_token='your-token',
                        zone_id='your-zone-id',
                        allow_multiple_records=True,
                        id_only=True)
```

To return all A records from all zones with a name of '@' (root):

```
from record_get import record_get

# this value will contain a list of zone IDs
record_ids = record_get(hetzner_dns_token='your-token',
                        search_all_zones=True,
                        record_type='A',
                        name='@',
                        allow_multiple_records=True)
```

To return the first record with a value of `1.2.3.4` and a TTL of `57600` by using a zone (ie. domain) name as a lookup:

```
from record_get import record_get

# this value will contain a list of zone IDs
record_ids = record_get(hetzner_dns_token='your-token',
                        zone_name='your-domain.com',
                        value='1.2.3.4',
                        ttle=57600,
                        first_record_only=True)
```


#### record_update

As with the `zone` modules, you can use `record_delete` and `record_create` to update a record. This library does not currently have a native `record_update` module.


#### record_delete

Delete an existing zone.

Records can be deleted directly using a `record_id`, or can be done indirectly by using any of the *Optional Parameters* as a lookup.

Successful delete operations will return the string 'OK', and unsuccessful delete operations will raise a `ValueError` exception.

Required\* Parameters: One of: `record_id` or `zone_id` or `zone_name`
Optional Parameters: {
  Filters: `record_type`, `name`, `value`, `ttl`,
  Options: `delete_multiple_records`, `first_record_only`, `search_all_zones`\*
}

\*If the `search_all_zones` parameter is given a truthy value, then you do not need to include any of the *Required Parameters*, as their purpose is to ensure that records are only returned for a single zone.

**Note:** This function will raise an exception if multiple records are returned, \*unless\* the `first_record_only` \*or\* `allow_multiple_records` parameters are truthy.

##### Options

These parameters can be given truthy values to enable them:

`delete_multiple_records` - Delete all matching records, even if there is more than one record returned.
`first_record_only` - Delete only the first record returned. (There is no guarantee of any ordering.)
`search_all_zones` - Allow records to be returned from all zones. None of "required" parameters are needed when using this option.


##### In a Bash prompt

To delete a record by using the record ID: `RECORD_ID='your-record-id' ./record_delete.py`

To delete a zone's A record with a name of 'www' by using a zone (ie. domain) name as a lookup: `ZONE_NAME=your-domain.com TYPE=A NAME=www ./record_delete.py`

To delete all MX records for a zone by using a zone ID as a lookup: `ZONE_ID=your-zone-id TYPE=MX DELETE_MULTIPLE_RECORDS=1 ./record_delete.py`

To delete all A records from all zones with a name of '@' (root): `TYPE=A NAME="@" SEARCH_ALL_ZONES=1 DELETE_MULTIPLE_RECORDS=1 ./record_delete.py`

To delete the first returned A record with a value of `1.2.3.4` and a TTL of `57600` by using a zone (ie. domain) name as a lookup: `ZONE_NAME=your-domain.com TYPE=A VALUE=1.2.3.4 TTL=57600 FIRST_RECORD_ONLY=1 ./record_delete.py`


#### In Python

To delete a record by using the record ID:

```
from record_delete import record_delete

record_delete(hetzner_dns_token='your-token',
              record_id='your-record-id')
```

To delete a zone's A record with a name of 'www' by using a zone (ie. domain) name as a lookup:

```
from record_delete import record_delete

record_delete(hetzner_dns_token='your-token',
              zone_name='your-domain.com',
              record_type='A',
              name='www')
```

To delete all MX records for a zone by using a zone ID as a lookup:

```
from record_delete import record_delete

record_delete(hetzner_dns_token='your-token',
              zone_id='your-zone-id',
              record_type='MX',
              delete_multiple_records=True)
```

To delete all A records from all zones with a name of '@' (root):

```
from record_delete import record_delete

# will raise ValueError return 'OK' if delete operation was successful
record_delete(hetzner_dns_token='your-token',
              record_type='A',
              name='@',
              search_all_zones=True)
```

To delete the first returned A record with a value of `1.2.3.4` and a TTL of `57600` by using a zone (ie. domain) name as a lookup:

```
from record_delete import record_delete

# will raise ValueError return 'OK' if delete operation was successful
record_delete(hetzner_dns_token='your-token',
              zone_name='your-domain.com',
              record_type='A',
              value='1.2.3.4',
              ttl=57600,
              first_record_only=True)
```
