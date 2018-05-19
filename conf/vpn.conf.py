[vpn]
# By default we disable VPN support as it requires running utils/rooter.py as
# root next to cuckoo.py (which should run as regular user).
enabled = no

# Comma-separated list of the available VPNs.
vpns = vpn0

[vpn0]
# Name of this VPN. The name is represented by the filepath to the
# configuration file, e.g., cuckoo would represent /etc/openvpn/cuckoo.conf
# Note that you can't assign the names "none" and "internet" as those would
# conflict with the routing section in cuckoo.conf.
name = vpn0

# The description of this VPN which will be displayed in the web interface.
# Can be used to for example describe the country where this VPN ends up.
description = openvpn_tunnel

# The tun device hardcoded for this VPN. Each VPN *must* be configured to use
# a hardcoded/persistent tun device by explicitly adding the line "dev tunX"
# to its configuration (e.g., /etc/openvpn/vpn1.conf) where X in tunX is a
# unique number between 0 and your lucky number of choice.
interface = tun0

# Routing table name/id for this VPN. If table name is used it *must* be
# added to /etc/iproute2/rt_tables as "<id> <name>" line (e.g., "201 tun0").
# ID and name must be unique across the system (refer /etc/iproute2/rt_tables
# for existing names and IDs).
rt_table = tun0

