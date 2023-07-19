from typing import Generator

import argparse

def format_addresses(addresses: list[dict], args: argparse.Namespace) -> Generator[str, dict, None]:
    # Variables
    input_var_name: str = args.nginx_geo_input_var
    output_var_name: str = "meta_ip_address"

    header: str = f"geo ${input_var_name} ${output_var_name} \u007b"
    footer: str = "\n    default 0;\n}"
    
    yield header
    for address in addresses:
        if "route" in address:
            yield f"    {address['route']} 1;"

    yield footer