# hetzner-dns-cli

#### *This repo was built using code samples from Hetzner's DNS API docs.*

This library makes it easier to work with Hetzner's [DNS API](https://dns.hetzner.com/api-docs/).

These tools are made with Python and are designed to be used in Bash or Python.

All examples in this README assume you are in the root directory of this project when running commands.

## Setup

Clone the repo to a folder of your choice: `git clone https://github.com/arcanemachine/hetzner-dns-cli`.

Now, simply navigate to the folder and run the command you want to use.

Example (from project root folder): ` HETZNER_DNS_TOKEN=your-hetzner-dns-token ./zones/zone_list.py`

(Note: To prevent sensitive data from being saved in your Bash history, ensure that this command begins with a space, or set the [environment variable somewhere else](#setting-environment-variables)

**All API calls require a `HETZNER_DNS_TOKEN` parameter to be set.**


## Setting environment variables in Bash

If you already know about Bash environment variables, you can safely skip this section. If you don't, you should read this section to avoid leaking your DNS token in your bash history



### Setting environment variables

#### For a single command

To set an environment variable for a single command, just enter the key-value pair before the command you want to run.

Example: `HETZNER_DNS_TOKEN=your-hetzner-dns-token ./zones/zone_list.py` **(WARNING: This command will be saved to your Bash history! Continue reading to learn how to avoid this)**

To avoid saving the item to your bash history, begin the command with a space:

Example: ` HETZNER_DNS_TOKEN=your-hetzner-dns-token ./zones/zone_list.py` (Make sure there is a space at the beginning!)

Please note that this method of setting environment variables is cumbersome and error-prone. Continue reading to learn better and easier ways of setting environment variables.


#### For the current session

You can set environment variables in a shell script, and use `source` to load them into the current session:

For example, in a file called `my-env.sh`:

```
export HETZNER_DNS_TOKEN=your-hetzner-dns-token
```

Then, run the command `source my-env.sh` to load the environment variable into your current session.

Now, simply running the command `./zones/zone_list.py` will automatically pass the `HETZNER_DNS_TOKEN` (or any other environment variables) to the command.


##### Recommended: Use `direnv` for easy use across multiple sessions

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

Again: **All API calls require a `HETZNER_DNS_TOKEN` parameter to be set.**


## Using these tools

### In a Bash prompt

Simply execute the file you want to run:

Example: `./zones/zone_list.py`

(Ensure that the `HETZNER_DNS_TOKEN` environment variable has been set. Read [this section](#setting-environment-variables) if you don't know how to do this.)


### In Python

Either add this project's root folder to your Python PATH, or navigate to this project's root folder before running a script like this:

```
from zones.zone_list import zone_list

# THIS EXAMPLE WILL NOT WORK IF YOU HAVEN'T CREATED ANY HETZNER DNS ZONES

# get zone list
dns_zones = zone_list()['zones']

# parse ID from first zone
your_zone_id = dns_zones[0]['id']

print(your_zone_id)
```


## Structure

These tools are seperated by feature into folders/modules:
  - zones
  - records

Each feature/module can perform the following actions
  - list
  - create
  - get
  - update
  - destroy

e.g. Running `./zones/zone_list.py` in Bash will list all available DNS zones.


## Getting human-readable output (pretty-printing)

The default output is nearly impossible for humans to read. Here's how to format it so it looks better:

### In a Bash prompt

This method requires you to have `npm` installed:
  - Install the npm package `json`:
    - `npm i -g json`
  - Pipe the output of a command to `json`:
    - `./zones/zone_list | json`

If you know of a simpler method, please submit a ticket.


### In Python code

```
import json
from zones.zone_list import zone_list

# get zone list
dns_zones = zone_list()['zones']

# make it readable
readable_dns_zones = json.dumps(dns_zones, indent=2)

print(readable_dns_zones)

```



## Helpful Features

This section highlights some features that have been included with this library.

**This section assumes that you have saved the `HETZNER_DNS_TOKEN` environment variable before running the commands. Read [this section](#setting-environment-variables) if you don't know how to do this.)**

### Get zone by domain name

#### In a Bash prompt

##### Get data for the entire zone

`NAME=your-domain.com ./zones/zone_get.py`

##### Get zone ID only

`NAME=your-domain.com ID_ONLY=1 ./zones/zone_get.py`


### In Python

##### Get data for the entire zone

```
from zones.zone_get import zone_get

zone = zone_get(name='your-domain.com')

print(zone)

```

##### Get zone ID only

```
from zones.zone_get import zone_get

zone_id = zone_get(name='your-domain.com', id_only=True)

print(zone_id)

```


## Modules

These tools can be imported as python modules, whose primary functions have the same name as the file. For example, this function...:

```
from zones.zone_list import zone_list

zone_list()
```

...will return a dictionary containing the expected values.



