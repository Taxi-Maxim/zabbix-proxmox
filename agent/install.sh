#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
install_dir=/usr/local/lib/zabbix-proxmox
zabbix_dir=/etc/zabbix/zabbix_agent2.d

mkdir -p "$install_dir/src" "$zabbix_dir"
cp -R "$project_dir/src/." "$install_dir/src/"
install -m 0644 "$project_dir/agent/proxmox.conf" "$zabbix_dir/proxmox.conf"
systemctl restart zabbix-agent2 2>/dev/null || systemctl restart zabbix-agent
printf '%s\n' "Installed Zabbix Proxmox agent to $install_dir"