# hetzner-dns-cli

#### *This repo was built using code samples from Hetzner's DNS API docs.*

A collection of tools that make it easy to work with Hetzner's [DNS API](https://dns.hetzner.com/api-docs/).

These tools are made with Python and can be used in Bash or Python.


## Setup

Clone the repo to a folder of your choice: `git clone git@github.com:arcanemachine/hetzner-dns-cli`.

These tools use OS environment variables for setting parameters for API requests.

All API calls will require a `HETZNER_DNS_TOKEN` environment variable to be set.


## Use

### In a bash prompt

Simply execute the file you want to run: e.g. `./zones/zone_list.py`

### In a python module

See section [Modules].

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

e.g. Running `python3 ./zones/zone_list.py` from will list all zones


## Modules

These tools can be imported as python modules, whose primary functions have the same name as the file. For example, this function...:

```
from zones.zone_list import zone_list

zone_list()
```

...will return a dictionary containing the expected values.


## Readable output (pretty-printing)

The default output is nearly impossible for humans to read. Here's how to format it so it looks better:

### In a bash prompt

This method requires you to have `npm` installed:
  - Install the npm package `json`:
    - `npm i -g json`
  - Pipe the output of a command to `json`:
    - `./zones/zone_list | json`

### In Python code

```
import json
from zones.zone_list import zone_list

result = json.dumps(zone_list(), indent=2)

```
