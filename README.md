# Zabbix Proxmox Monitoring Agent

Standard-library-only collectors for Proxmox VE 9 and Zabbix Agent 7.x. Each
command writes exactly one JSON document to stdout. Diagnostics, when enabled
with `--debug`, are written to stderr.

## Local run

```sh
python3 src/proxmox_agent.py api
python3 src/proxmox_agent.py services
```

## Install

Run `sudo agent/install.sh` on the Proxmox host, then import
`template/Template_Proxmox_Host.yaml` into Zabbix 7 and attach it to the host.
The template uses one master item per collector; dependent items can extract
individual values with JSONPath without repeating system calls.

The agent does not run `apt update` and has no pip dependencies. Commands that
are unavailable or fail produce a valid JSON payload with `error: 1` where the
collector cannot provide its data.