from typing import Generator

import json

def format_addresses(addresses: list[dict]) -> Generator[str, dict, None]:
    for address in addresses:
        yield json.dumps(obj=address)