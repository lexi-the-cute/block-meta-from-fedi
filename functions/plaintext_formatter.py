from typing import Generator

import argparse

def format_addresses(addresses: list[dict], args: argparse.Namespace) -> Generator[str, dict, None]:
    for address in addresses:
        if "route" in address:
            yield address["route"]