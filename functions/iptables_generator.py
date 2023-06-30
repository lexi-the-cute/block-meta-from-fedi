# sudo iptables -A INPUT -s 116.10.0.0/16 -j DROP

from typing import Generator

def generate_iptable_rules(addresses: list[dict]) -> Generator[str, dict, None]:
    # Commands
    sudo: str = "sudo"
    iptables: str = "iptables"

    # Variables
    chain_name: str = "PROTECT_FEDI"
    policy: str = "DROP"  # REJECT tells the server you're dropping them, DROP is more evil in that you drop the connection silently

    # IP Tables Setup
    create_chain: str = f"{sudo} {iptables} -N {chain_name}"
    delete_chain: str = f"{sudo} {iptables} -X {chain_name}"
    empty_chain: str = f"{sudo} {iptables} -F {chain_name}"
    add_chain_to_incoming_packets: str = f"{sudo} {iptables} -I INPUT 1 -j {chain_name}"

    handle_route: str = "{sudo} {iptables} -A {chain_name} -s {address} -j {policy}"

    # Setup Stage
    yield create_chain
    yield add_chain_to_incoming_packets

    # I was going to pipe data directly from one generator to the other, but that made the code far more complex than is needed
    # If the addresses list get's large enough to warrant piping, it may be time to look into another method of handling blocking Meta
    for address in addresses:
        if address is dict and "route" in address:
            yield handle_route.format(sudo=sudo, iptables=iptables, chain_name=chain_name, address=address["route"], policy=policy)