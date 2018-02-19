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
/root/bin/racktables-api.py get CPU --server srv001

Get disks:
/root/bin/racktables-api.py get STORAGE --server srv001

Get operating system:
/root/bin/racktables-api.py get OS --server srv001

Status of the server (Active, Broken, In Stock or Suspend):
/root/bin/racktables-api.py get STATUS --server srv001

Get SLA of the server (Managed or Unmanaged):
/root/bin/racktables-api.py get SLA --server srv001

RAM volume:
/root/bin/racktables-api.py get RAM --server srv001

FQDN of the server:
/root/bin/racktables-api.py get FQDN --server srv001
```

### Modifying information

Before modifying information you must get list of all available values for given parameter:

```
/root/bin/racktables-api.py get CPU     - get all available processor models
/root/bin/racktables-api.py get STORAGE - disks
/root/bin/racktables-api.py get OS      - operating systems
/root/bin/racktables-api.py get STATUS  - statuses of servers
/root/bin/racktables-api.py get SLA     - available types of SLA
```

Then set a desired value:

```
Add/delete a processor:
/root/bin/racktables-api.py add/del CPU --server srv001 --value "Intel Xeon E5645"

Add/delete a disk:
/root/bin/racktables-api.py add/del STORAGE --server srv001 --value "SSD ST480HM000"

Change an operating system:
/root/bin/racktables-api.py set OS --server srv001 --value "Debian 8 (jessie)"

Change a server status:
/root/bin/racktables-api.py set STATUS --server srv001 --value "Active"

Change a server SLA:
/root/bin/racktables-api.py set SLA --server srv001 --value "Managed"

Change a RAM volume (in MB):
/root/bin/racktables-api.py set RAM --server srv001 --value 48245

Set a server FQDN:
/root/bin/racktables-api.py set FQDN -s srv001 -v srv001.example.com
```

### Exit codes

0 - successful execution;
20 - incorrect number of arguments or their unacceptable combination;
30 - MySQL connaction error;
40 - MySQL query error.
