#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
install_dir=/usr/local/lib/zabbix-proxmox
sudoers_file=/etc/sudoers.d/zabbix-proxmox

if command -v zabbix_agent2 >/dev/null 2>&1; then
	zabbix_dir=/etc/zabbix/zabbix_agent2.d
	zabbix_service=zabbix-agent2
elif command -v zabbix_agentd >/dev/null 2>&1; then
	zabbix_dir=/etc/zabbix/zabbix_agentd.conf.d
	zabbix_service=zabbix-agent
else
	printf '%s\n' "Neither zabbix_agent2 nor zabbix_agentd was found" >&2
	exit 1
fi

mkdir -p "$install_dir/src" "$install_dir/bin" "$zabbix_dir"
cp -R "$project_dir/src/." "$install_dir/src/"
install -m 0755 "$project_dir"/agent/bin/proxmox-* "$install_dir/bin/"
install -m 0644 "$project_dir/agent/proxmox.conf" "$zabbix_dir/proxmox.conf"
sed -i 's/\r$//' "$zabbix_dir/proxmox.conf"
for wrapper in "$install_dir"/bin/proxmox-*; do
	sed -i 's/\r$//' "$wrapper"
done
rm -f "$sudoers_file"
install -m 0440 "$project_dir/agent/zabbix-proxmox.sudoers" "$sudoers_file"
sed -i 's/\r$//' "$sudoers_file"
visudo -cf "$sudoers_file"
systemctl restart "$zabbix_service"
printf '%s\n' "Installed Zabbix Proxmox agent to $install_dir"