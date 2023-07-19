import re
import logging

logger = logging.getLogger(__name__)

try:
    import whois
except ImportError as e:
    logger.error("You need to install the python-whois module. Install PIP (https://bootstrap.pypa.io/get-pip.py) and then 'pip3 install python-whois'")
    raise e

from typing import Generator

# https://developers.facebook.com/docs/sharing/webmasters/crawler/
# whois -h whois.radb.net -- '-i origin AS32934' | grep ^route
# The results are in the format of address:mask

route_pattern: re.Pattern = re.compile(pattern='([^a-z0-9./:])+')
def sanitize_routes(route: str):
    return re.sub(pattern=route_pattern, repl="", string=route.lower())

def lookup_records(query: str, host: str, flags: int = 0, many_results: bool = True, quiet: bool = True) -> str:
    client: whois.NICClient = whois.NICClient()

    response: bytes = client.whois(query=query, hostname=host, flags=flags, many_results=many_results, quiet=quiet)

    return response

def lookup_ips(query: str, host: str, flags: int = 0, many_results: bool = True, quiet: bool = True) -> Generator[dict, None, None]:
    response = lookup_records(query=query, host=host, flags=flags, many_results=many_results, quiet=quiet)

    # Deduplicating Routes
    routes: list = []
    for line in response.splitlines():
        if line.startswith("route:"):
            route: str = sanitize_routes(":".join(line.split(":")[1:]).strip())

            if route in routes:
                continue

            routes.append(route)
            yield {
                "ip_version": 4,
                "route": route
            }
        elif line.startswith("route6:"):
            route: str = sanitize_routes(":".join(line.split(":")[1:]).strip())

            if route in routes:
                continue

            routes.append(route)
            yield {
                "ip_version": 6,
                "route": route
            }

def get_ips():
    query: str = "-i origin AS32934"
    host: str = "whois.radb.net"

    return lookup_ips(query=query, host=host)

if __name__ == "__main__":
    for ip in get_ips():
        if type(ip) is dict and "route" in ip:
            print(ip["route"])
        else:
            print(ip)