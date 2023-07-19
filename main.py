from functions import plaintext_formatter, whois_lookup, iptables_generator, json_formatter, nginx_geo_formatter

import argparse

# Built in boolean parsing does not work as expected, so use this custom parser instead
def parse_boolean_from_string(string: str):
    if string.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif string.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    argParser: argparse.ArgumentParser = argparse.ArgumentParser()
    argParser.add_argument("-f", "--format",
                           default="iptables",
                           const="iptables",
                           nargs="?",
                           type=str,
                           choices=("iptables", "plain", "jsonl", "nginx-geo"),
                           help="Output format of IP address list (default: %(default)s)")

    argParser.add_argument("-p", "--policy",
                           default="DROP",
                           const="DROP",
                           nargs="?",
                           type=str,
                           choices=("DROP", "REJECT", "ACCEPT", "DNAT"),
                           help="iptables policy for handling incoming packets (default: %(default)s)")

    argParser.add_argument("-P", "--protocol",
                           default="tcp",
                           const="tcp",
                           nargs="?",
                           type=str,
                           choices=("tcp", "udp", "sctp", "dccp"),
                           help="iptables protocol type (only valid when policy is DNAT) (default: %(default)s)")

    argParser.add_argument("-d", "--destination",
                           default=":8080",
                           const=":8080",
                           nargs="?",
                           type=str,
                           help="iptables destination route (only valid when policy is DNAT) (default: %(default)s)")

    argParser.add_argument("--handle-firewall",
                           default=True,
                           const=True,
                           nargs="?",
                           type=parse_boolean_from_string,
                           help="iptables handle opening/closing port for you (only valid when policy is DNAT and destination is self) (default: %(default)s)")

    argParser.add_argument("--iptables-path",
                           default="iptables",
                           const="iptables",
                           nargs="?",
                           type=str,
                           help="iptables path (default: %(default)s)")
    
    argParser.add_argument("--ip6tables-path",
                           default="ip6tables",
                           const="ip6tables",
                           nargs="?",
                           type=str,
                           help="ip6tables path (default: %(default)s)")
    
    argParser.add_argument("--sudo-path",
                           default="sudo",
                           const="sudo",
                           nargs="?",
                           type=str,
                           help="sudo path (default: %(default)s)")

    argParser.add_argument("--nginx-geo-input-var",
                           default="http_x_forwarded_for",
                           const="http_x_forwarded_for",
                           nargs="?",
                           type=str,
                           help="The variable Nginx will read to determine one's real ip address (default: %(default)s)")

    args = argParser.parse_args()

    addresses: list[dict] = []

    # Get IP Addresses To Ban
    for address in whois_lookup.get_ips():
        addresses.append(address)

    # Generate IP Table Rules
    if args.format == "iptables":
        # IP Tables Commands
        for rule in iptables_generator.generate_iptable_rules(addresses=addresses, args=args):
            print(rule)
    elif args.format == "plain":
        # Just Plain Addresses
        for address in plaintext_formatter.format_addresses(addresses=addresses, args=args):
            print(address)
    elif args.format == "jsonl":
        # JSON Formatted Addresses
        for address in json_formatter.format_addresses(addresses=addresses, args=args):
            print(address)
    elif args.format == "nginx-geo":
        # Nginx Config Formatted Addresses
        for address in nginx_geo_formatter.format_addresses(addresses=addresses, args=args):
            print(address)
    else:
        print(f"Unknown format: `{args.format}`")