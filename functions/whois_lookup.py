import whois

from typing import Generator

# https://developers.facebook.com/docs/sharing/webmasters/crawler/
# whois -h whois.radb.net -- '-i origin AS32934' | grep ^route
# The results are in the format of address:mask

def lookup_records(query: str, host: str, flags: int = 0, many_results: bool = True, quiet: bool = True) -> str:
    client: whois.NICClient = whois.NICClient()

    response: bytes = client.whois(query=query, hostname=host, flags=flags, many_results=many_results, quiet=quiet)

    return response

def lookup_ips(query: str, host: str, flags: int = 0, many_results: bool = True, quiet: bool = True) -> Generator[dict, None, None]:
    response = lookup_records(query=query, host=host, flags=flags, many_results=many_results, quiet=quiet)

    for line in response.splitlines():
        if line.startswith("route:"):
            route: str = ":".join(line.split(":")[1:]).strip()

            yield {
                "ip_version": 4,
                "route": route
            }
        elif line.startswith("route6:"):
            route: str = ":".join(line.split(":")[1:]).strip()

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
        if ip is dict and "route" in ip:
            print(ip["route"])
        else:
            print(ip)