from functions import whois_lookup, iptables_generator

if __name__ == "__main__":
    addresses: list[dict] = []

    # Get IP Addresses To Ban
    for address in whois_lookup.get_ips():
        addresses.append(address)

    # Generate IP Table Rules
    for rule in iptables_generator.generate_iptable_rules(addresses=addresses):
        print(rule)