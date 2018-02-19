# racktables-api

CLI API for [RackTables](https://www.racktables.org/) database. Written in Python 3.

## Installation

1. Clone the repository.
2. Set database connection requisites in `config.py`.

## Usage

### Get information

```
Help:
/root/bin/racktables-api.py

Get a list of all servers:
/root/bin/racktables-api.py get SERVER

Get CPUs of the server:
/root/bin/racktables-api.py get CPU --server rb139

Get disks:
/root/bin/racktables-api.py get STORAGE --server rb139

Get operating system:
/root/bin/racktables-api.py get OS --server rb139

Status of the server (Active, Broken, In Stock or Suspend):
/root/bin/racktables-api.py get STATUS --server rb139

Get SLA of the server (Managed or Unmanaged):
/root/bin/racktables-api.py get SLA --server rb139

RAM volume:
/root/bin/racktables-api.py get RAM --server rb139

FQDN of the server:
/root/bin/racktables-api.py get FQDN --server rb139
