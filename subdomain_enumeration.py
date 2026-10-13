import secrets
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# PYTHON BASED SUB-DOMAINS ENUMERAITION TOOL
# RUNS with wordlist file of your own choice (given with top 100 most used domains)
# RUN on terminal: Usage: python subdomain_enumeration.py <target_domain> <wordlist_file>

def lookup(host):
    try:
        return set(socket.gethostbyname_ex(host)[2])
    except OSError:
        return set()

def main():
    if len(sys.argv) < 3:
        sys.exit("Usage: python sub_enum.py <target_domain> <wordlist_file>")

    domain, wordlist = sys.argv[1:3]

    try:
        with open(wordlist, encoding="utf-8") as f:
            words = {l.strip() for l in f if l.strip() and not l.startswith("#")}
    except FileNotFoundError:
        sys.exit(f"[-] Wordlist file '{wordlist}' not found.")

    # Wildcard detection: random labels should never resolve
    wildcard = set().union(*(lookup(f"{secrets.token_hex(8)}.{domain}") for _ in range(3)))
    if wildcard:
        print(f"[!] Wildcard DNS detected, filtering IPs: {', '.join(sorted(wildcard))}")

    def check(word):
        host = f"{word}.{domain}"
        ips = lookup(host)
        if ips and not ips <= wildcard:  # resolves, and not just the wildcard IP(s)
            print(f"[+] Discovered: {host} -> {', '.join(sorted(ips))}")
            return host

    print(f"[*] Loaded {len(words)} unique words. Scanning {domain}...\n")
    start = time.time()

    with ThreadPoolExecutor(max_workers=100) as pool:
        found = [r for r in pool.map(check, words) if r]

    print(f"\n[*] Done in {time.time() - start:.2f}s. Active subdomains found: {len(found)}")

if __name__ == "__main__":
    main()