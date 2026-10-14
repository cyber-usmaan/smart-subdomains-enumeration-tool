# smart-subdomains-enumeration-tool
# sub_enum.py

A fast, dependency-free Python tool that discovers subdomains of a target domain by brute-forcing names from a wordlist and checking which ones resolve in DNS.

> **Legal notice:** Only use this against domains you own or have explicit permission to test.

## Features

- **Fast concurrent scanning** using a pool of 100 threads
- **Wildcard DNS detection** that filters out false positives when a domain resolves every name
- **Multi-IP results**: shows every IP a subdomain resolves to
- **Wordlist cleanup**: ignores blank lines and `#` comments, and removes duplicates
- **Zero dependencies**: standard library only (Python 3.6+)
- **Scan summary**: reports total time and number of subdomains found

## Usage

```bash
python sub_enum.py <target_domain> <wordlist_file>
```

Example:

```bash
python sub_enum.py example.com subdomains.txt
```

Wordlist format (one word per line):

```
# common names
www
mail
dev
api
```

Sample output:

```
[!] Wildcard DNS detected, filtering IPs: 203.0.113.10
[*] Loaded 4 unique words. Scanning example.com...

[+] Discovered: www.example.com -> 93.184.216.34
[+] Discovered: api.example.com -> 198.51.100.7

[*] Done in 1.42s. Active subdomains found: 2
```

## How it works

1. **Load the wordlist.** Lines are stripped, and empty lines and comments are dropped. A set removes duplicate entries.
2. **Detect wildcard DNS.** The tool resolves three random labels (e.g. `a3f9c1d2e4b56780.example.com`) that cannot legitimately exist. Any IPs returned are recorded as wildcard IPs.
3. **Resolve in parallel.** Each `word.domain` is looked up with `socket.gethostbyname_ex` across a thread pool. DNS lookups are I/O-bound, so threads give a large speedup.
4. **Filter and report.** A subdomain counts as discovered only if it resolves *and* its IPs are not entirely a subset of the wildcard IPs.
