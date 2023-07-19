from typing import Generator

import json
import argparse

def format_addresses(addresses: list[dict], args: argparse.Namespace) -> Generator[str, dict, None]:
    for address in addresses:
        yield json.dumps(obj=address)