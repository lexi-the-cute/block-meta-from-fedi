import whois

def lookup_records(query: str, host: str, flags: int = 0, many_results: bool = True, quiet: bool = True) -> str:
    # whois -h whois.radb.net -- '-i origin AS32934' | grep ^route
    client: whois.NICClient = whois.NICClient()

    response: bytes = client.whois(query=query, hostname=host, flags=flags, many_results=many_results, quiet=quiet)

    return response

def lookup_ips(query: str, host: str, flags: int = 0, many_results: bool = True, quiet: bool = True):
    response = lookup_records(query=query, host=host, flags=flags, many_results=many_results, quiet=quiet)

    for line in response.splitlines():
        if line.startswith("route:"):
            route: str = ":".join(line.split(":")[2:]).strip()

            yield {
                "ip_version": 4,
                "route": route
            }
        elif line.startswith("route6:"):
            route: str = ":".join(line.split(":")[2:]).strip()

            yield {
                "ip_version": 6,
                "route": route
            }

if __name__ == "__main__":
    query: str = "-i origin AS32934"
    host: str = "whois.radb.net"

    for ip in lookup_ips(query=query, host=host):
        print(ip)