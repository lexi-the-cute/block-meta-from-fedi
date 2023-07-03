from typing import Generator

def format_addresses(addresses: list[dict]) -> Generator[str, dict, None]:
    for address in addresses:
        if "route" in address:
            yield address["route"]