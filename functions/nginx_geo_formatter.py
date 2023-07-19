from typing import Generator

import argparse

def format_addresses(addresses: list[dict], args: argparse.Namespace) -> Generator[str, dict, None]:
    # Variables
    var_name: str = "meta_ip_address"

    header: str = f"geo ${var_name} \u007b"
    footer: str = "\n    default 1;\n}"
    
    yield header
    for address in addresses:
        if "route" in address:
            yield f"    {address['route']};"

    yield footer