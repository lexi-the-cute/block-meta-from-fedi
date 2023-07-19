# sudo iptables -A INPUT -s 116.10.0.0/16 -j DROP

from typing import Generator

import argparse

def generate_iptable_rules(addresses: list[dict], args: argparse.Namespace) -> Generator[str, dict, None]:
    # Commands
    sudo: str = "sudo"
    iptables: str = "iptables"
    ip6tables: str = "ip6tables"

    # Variables
    chain_name: str = "PROTECT_FEDI"
    policy: str = args.policy  # REJECT tells the server you're dropping them, DROP is more evil in that you drop the connection silently

    # IP Tables Setup
    create_chain: str = f"{sudo} {iptables} -N {chain_name}"
    delete_chain: str = f"{sudo} {iptables} -X {chain_name}"
    empty_chain: str = f"{sudo} {iptables} -F {chain_name}"
    add_chain_to_incoming_packets: str = f"{sudo} {iptables} -I INPUT 1 -j {chain_name}"

    # IPV6 Tables Setup
    create_chain_v6: str = f"{sudo} {ip6tables} -N {chain_name}"
    delete_chain_v6: str = f"{sudo} {ip6tables} -X {chain_name}"
    empty_chain_v6: str = f"{sudo} {ip6tables} -F {chain_name}"
    add_chain_to_incoming_packets_v6: str = f"{sudo} {ip6tables} -I INPUT 1 -j {chain_name}"

    # Route Strings
    handle_route: str = "{sudo} {iptables} -A {chain_name} -s {address} -j {policy}"
    handle_route_v6: str = "{sudo} {ip6tables} -A {chain_name} -s {address} -j {policy}"

    # Setup Stage
    yield create_chain
    yield add_chain_to_incoming_packets

    # Setup IPV6 Stage
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