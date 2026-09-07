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

On the Proxmox host:

```sh
cd /root/zabbix-proxmox
chmod +x agent/install.sh
sudo agent/install.sh
```

The installer copies the agent to `/usr/local/lib/zabbix-proxmox` and the
UserParameters to the include directory used by the installed Zabbix agent.
It also installs root-owned fixed wrapper commands and a restricted sudoers
policy for those wrappers, so the unprivileged Zabbix user can read Proxmox
and hardware data without being granted a general root shell.
Verify the agent before importing the template:

```sh
zabbix_agent2 -t proxmox.api
zabbix_agent2 -t proxmox.journal
zabbix_agent2 -t proxmox.smart
zabbix_agent2 -t proxmox.zfs
zabbix_agent2 -t proxmox.services
```

If the host uses the classic agent, use `zabbix_agentd -t` instead. Import
`template/Template_Proxmox_Host.yaml` into Zabbix 7, attach it to the Proxmox
host, and make sure the host has an active Zabbix agent interface. The
template uses one master item per collector; dependent items extract values
with JSONPath, and SMART disks are discovered automatically.

After attaching the template, check **Monitoring -> Latest data** for the
master items first. Dependent items should populate after their master item
has received its first value.

To remove the installation, delete the copied directory and configuration,
then restart the agent:

```sh
sudo rm -rf /usr/local/lib/zabbix-proxmox
sudo rm -f /etc/zabbix/zabbix_agent2.d/proxmox.conf
sudo rm -f /etc/zabbix/zabbix_agentd.conf.d/proxmox.conf
sudo rm -f /etc/sudoers.d/zabbix-proxmox
sudo systemctl restart zabbix-agent2 || sudo systemctl restart zabbix-agent
```

The agent does not run `apt update` and has no pip dependencies. Commands that
are unavailable or fail produce a valid JSON payload with `error: 1` where the
collector cannot provide its data.