# https://book.huihoo.com/iptables-tutorial/c3742.htm
# Tables: raw, mangle, nat, filter
# Chains: PREROUTING, INPUT, OUTPUT, POSTROUTING, FORWARD

from typing import Generator

import argparse

# Determine How To Handle Traffic
def generate_iptable_rules(addresses: list[dict], args: argparse.Namespace) -> Generator[str, dict, None]:
    if args.policy == "DNAT":
        return redirect_traffic(addresses=addresses, args=args)

    return filter_traffic(addresses=addresses, args=args)

# For Redirecting Traffic
def redirect_traffic(addresses: list[dict], args: argparse.Namespace) -> Generator[str, dict, None]:
    # sudo iptables -t nat -A PREROUTING -p tcp -s 10.0.0.224 -j DNAT --to-destination :8080

    # Commands
    sudo: str = args.sudo_path
    iptables: str = args.iptables_path
    ip6tables: str = args.ip6tables_path

    # Variables
    chain_name: str = "PROTECT_FEDI"
    firewall_chain_name: str = "PROTECT_FEDI_FIREWALL"
    policy: str = args.policy
    destination: str = args.destination
    destination_port: str = destination.split(":")[1] if ":" in destination else None
    is_destination_self: bool = True if destination.startswith(":") else False
    protocol: str = args.protocol
    handle_firewall: bool = args.handle_firewall

    # IP Tables Setup
    create_chain: str = f"{sudo} {iptables} -t nat -N {chain_name}"
    delete_chain: str = f"{sudo} {iptables} -t nat -X {chain_name}"
    empty_chain: str = f"{sudo} {iptables} -t nat -F {chain_name}"
    add_chain_to_prerouting_packets: str = f"{sudo} {iptables} -t nat -I PREROUTING 1 -j {chain_name}"
    remove_chain_from_prerouting_packets: str = f"{sudo} {iptables} -t nat -D PREROUTING -j {chain_name}"

    # IP Tables Firewall Setup
    create_chain_firewall: str = f"{sudo} {iptables} -t filter -N {firewall_chain_name}"
    delete_chain_firewall: str = f"{sudo} {iptables} -t filter -X {firewall_chain_name}"
    empty_chain_firewall: str = f"{sudo} {iptables} -t filter -F {firewall_chain_name}"
    add_firewall_chain_to_incoming_packets: str = f"{sudo} {iptables} -t filter -I INPUT 1 -j {firewall_chain_name}"
    remove_firewall_chain_from_incoming_packets: str = f"{sudo} {iptables} -t filter -D INPUT -j {firewall_chain_name}"
    open_port_firewall: str = f"{sudo} {iptables} -t filter -A {firewall_chain_name} -p {protocol} -m {protocol} --dport {destination_port} -j ACCEPT"
    close_port_firewall: str = f"{sudo} {iptables} -t filter -D {firewall_chain_name} -p {protocol} -m {protocol} --dport {destination_port} -j ACCEPT"

    # IPV6 Tables Setup
    create_chain_v6: str = f"{sudo} {ip6tables} -t nat -N {chain_name}"
    delete_chain_v6: str = f"{sudo} {ip6tables} -t nat -X {chain_name}"
    empty_chain_v6: str = f"{sudo} {ip6tables} -t nat -F {chain_name}"
    add_chain_to_prerouting_packets_v6: str = f"{sudo} {ip6tables} -t nat -I PREROUTING 1 -j {chain_name}"
    remove_chain_from_prerouting_packets_v6: str = f"{sudo} {ip6tables} -t nat -D PREROUTING -j {chain_name}"

    # IPV6 Tables Firewall Setup
    create_chain_firewall_v6: str = f"{sudo} {ip6tables} -t filter -N {firewall_chain_name}"
    delete_chain_firewall_v6: str = f"{sudo} {ip6tables} -t filter -X {firewall_chain_name}"
    empty_chain_firewall_v6: str = f"{sudo} {ip6tables} -t filter -F {firewall_chain_name}"
    add_firewall_chain_to_incoming_packets_v6: str = f"{sudo} {ip6tables} -t filter -I INPUT 1 -j {firewall_chain_name}"
    remove_firewall_chain_from_incoming_packets_v6: str = f"{sudo} {ip6tables} -t filter -D INPUT -j {firewall_chain_name}"
    open_port_firewall_v6: str = f"{sudo} {ip6tables} -t filter -A {firewall_chain_name} -p {protocol} -m {protocol} --dport {destination_port} -j ACCEPT"
    close_port_firewall_v6: str = f"{sudo} {ip6tables} -t filter -D {firewall_chain_name} -p {protocol} -m {protocol} --dport {destination_port} -j ACCEPT"

    # Route Strings
    handle_route: str = "{sudo} {iptables} -t nat -A {chain_name} -p {protocol} -m {protocol} -s {address} -j {policy} --to-destination {destination}"
    handle_route_v6: str = "{sudo} {ip6tables} -t nat -A {chain_name} -p {protocol} -m {protocol} -s {address} -j {policy} --to-destination {destination}"

    # Only run this when handling firewall
    if handle_firewall and is_destination_self and destination_port is not None:
        # Open Firewall Stage
        yield close_port_firewall
        yield empty_chain_firewall
        yield remove_firewall_chain_from_incoming_packets
        yield delete_chain_firewall
        yield create_chain_firewall
        yield add_firewall_chain_to_incoming_packets
        yield open_port_firewall

        # Open IPV6 Firewall Stage
        yield close_port_firewall_v6
        yield empty_chain_firewall_v6
        yield remove_firewall_chain_from_incoming_packets_v6
        yield delete_chain_firewall_v6
        yield create_chain_firewall_v6
        yield add_firewall_chain_to_incoming_packets_v6
        yield open_port_firewall_v6

    # Setup Stage
    yield empty_chain
    yield remove_chain_from_prerouting_packets
    yield delete_chain
    yield create_chain
    yield add_chain_to_prerouting_packets

    # Setup IPV6 Stage
    yield empty_chain_v6
    yield remove_chain_from_prerouting_packets_v6
    yield delete_chain_v6
    yield create_chain_v6
    yield add_chain_to_prerouting_packets_v6

    # I was going to pipe data directly from one generator to the other, but that made the code far more complex than is needed
    # If the addresses list get's large enough to warrant piping, it may be time to look into another method of handling blocking Meta
    for address in addresses:
        if type(address) is dict and "route" in address:
            if "ip_version" in address and address["ip_version"] == 6:
                yield handle_route_v6.format(sudo=sudo, ip6tables=ip6tables, chain_name=chain_name, address=address["route"], policy=policy, protocol=protocol, destination=destination)
            else:
                yield handle_route.format(sudo=sudo, iptables=iptables, chain_name=chain_name, address=address["route"], policy=policy, protocol=protocol, destination=destination)

# For Filtering Traffic
def filter_traffic(addresses: list[dict], args: argparse.Namespace) -> Generator[str, dict, None]:
    # Commands
    sudo: str = args.sudo_path
    iptables: str = args.iptables_path
    ip6tables: str = args.ip6tables_path

    # Variables
    chain_name: str = "PROTECT_FEDI"
    policy: str = args.policy  # REJECT tells the server you're dropping them, DROP is more evil in that you drop the connection silently

    # IP Tables Setup
    create_chain: str = f"{sudo} {iptables} -t filter -N {chain_name}"
    delete_chain: str = f"{sudo} {iptables} -t filter -X {chain_name}"
    empty_chain: str = f"{sudo} {iptables} -t filter -F {chain_name}"
    add_chain_to_incoming_packets: str = f"{sudo} {iptables} -t filter -I INPUT 1 -j {chain_name}"
    remove_chain_from_incoming_packets: str = f"{sudo} {iptables} -t filter -D INPUT -j {chain_name}"

    # IPV6 Tables Setup
    create_chain_v6: str = f"{sudo} {ip6tables} -t filter -N {chain_name}"
    delete_chain_v6: str = f"{sudo} {ip6tables} -t filter -X {chain_name}"
    empty_chain_v6: str = f"{sudo} {ip6tables} -t filter -F {chain_name}"
    add_chain_to_incoming_packets_v6: str = f"{sudo} {ip6tables} -t filter -I INPUT 1 -j {chain_name}"
    remove_chain_from_incoming_packets_v6: str = f"{sudo} {ip6tables} -t filter -D INPUT -j {chain_name}"

    # Route Strings
    handle_route: str = "{sudo} {iptables} -t filter -A {chain_name} -s {address} -j {policy}"
    handle_route_v6: str = "{sudo} {ip6tables} -t filter -A {chain_name} -s {address} -j {policy}"

    # Setup Stage
    yield empty_chain
    yield remove_chain_from_incoming_packets
    yield delete_chain
    yield create_chain
    yield add_chain_to_incoming_packets

    # Setup IPV6 Stage
    yield empty_chain_v6
    yield remove_chain_from_incoming_packets_v6
    yield delete_chain_v6
    yield create_chain_v6
    yield add_chain_to_incoming_packets_v6

    # I was going to pipe data directly from one generator to the other, but that made the code far more complex than is needed
    # If the addresses list get's large enough to warrant piping, it may be time to look into another method of handling blocking Meta
    for address in addresses:
        if type(address) is dict and "route" in address:
            if "ip_version" in address and address["ip_version"] == 6:
                yield handle_route_v6.format(sudo=sudo, ip6tables=ip6tables, chain_name=chain_name, address=address["route"], policy=policy)
            else:
                yield handle_route.format(sudo=sudo, iptables=iptables, chain_name=chain_name, address=address["route"], policy=policy)