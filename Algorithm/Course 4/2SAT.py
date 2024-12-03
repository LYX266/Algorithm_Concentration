import requests
from collections import defaultdict

# Function to fetch and parse data from a URL
def fetch_instance_from_url(url):
    response = requests.get(url)
    response.raise_for_status()  
    data = response.text.strip().splitlines()
    
    n = int(data[0])  
    clauses = []
    for line in data[1:]:
        a, b = map(int, line.split())
        clauses.append((a, b))
    return n, clauses

# Kosaraju's Algorithm for SCC
def kosaraju_scc(graph, reverse_graph, n):
    def dfs1(node):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs1(neighbor)
        finish_stack.append(node)

    def dfs2(node, scc):
        visited[node] = True
        scc.append(node)
        for neighbor in reverse_graph[node]:
            if not visited[neighbor]:
                dfs2(neighbor, scc)

    # First pass: compute finishing times
    visited = [False] * (2 * n + 2)
    finish_stack = []
    for i in range(1, 2 * n + 1):
        if not visited[i]:
            dfs1(i)

    # Second pass: find SCCs
    visited = [False] * (2 * n + 2)
    scc_list = []
    while finish_stack:
        node = finish_stack.pop()
        if not visited[node]:
            scc = []
            dfs2(node, scc)
            scc_list.append(scc)

    return scc_list

# Build the implication graph
def build_graph(n, clauses):
    graph = defaultdict(list)
    reverse_graph = defaultdict(list)
    for a, b in clauses:
        u = 2 * abs(a) - (a < 0)
        v = 2 * abs(b) - (b < 0)
        graph[u ^ 1].append(v)  # ¬a → b
        graph[v ^ 1].append(u)  # ¬b → a
        reverse_graph[v].append(u ^ 1)
        reverse_graph[u].append(v ^ 1)
    return graph, reverse_graph

# Check satisfiability
def is_satisfiable(n, clauses):
    graph, reverse_graph = build_graph(n, clauses)
    sccs = kosaraju_scc(graph, reverse_graph, n)
    node_to_scc = {}
    for i, scc in enumerate(sccs):
        for node in scc:
            node_to_scc[node] = i
    for i in range(1, n + 1):
        if node_to_scc.get(2 * i) == node_to_scc.get(2 * i + 1):
            return False  # x and ¬x are in the same SCC
    return True

def solve_2sat_from_urls(urls):
    result = []
    for url in urls:
        n, clauses = fetch_instance_from_url(url)
        if is_satisfiable(n, clauses):
            result.append('1')
        else:
            result.append('0')
    return ''.join(result)

urls = [
    "https://d3c33hcgiwev3.cloudfront.net/_02c1945398be467219866ee1c3294d2d_2sat1.txt?Expires=1733356800&Signature=abrKkmudPN3~fLwNGoW23~VDFRMbWvRTqEZhazpgGQ0dQDci953vRbtGBl7f4M8AQW48EVCaXXNKDW76j15mh12SbmEtc2Le8OWE~IHp3Tz3cIB8XTuiu4Dt6mHoBbv3qaDxTpLYT61A9q61kre3IdCLU-I-NICikPbIr29B87M_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",
    "https://d3c33hcgiwev3.cloudfront.net/_02c1945398be467219866ee1c3294d2d_2sat2.txt?Expires=1733356800&Signature=dPxihUz1QvkOiog2iHQaQ8KQ-jhzxN8GqgbdHREZiChNyJ9MO42Vxjww~-jZ6LPqHq-8wh4bdAJG4QHclyW4HXfgHE1~rdiMCAba5w9T1b6w5V~fgeCCFCoxGTSmXBJs-n~NWnc5RlfYjR~4aW-0h~WaPxsu5DDgyeD8tKEB~Qk_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",
    "https://d3c33hcgiwev3.cloudfront.net/_02c1945398be467219866ee1c3294d2d_2sat3.txt?Expires=1733356800&Signature=lKncj19kE8wKGei-p88~WoaKZSfbl1deUKJ7fx9YUkZqCw-~rRVOPX4xl6xnSnfWth4I2jYEdROaZZNj~7qqUfHoVvKkAvuuQNZ~dCSvLHQR2YFrwEgbvHZSuHMiNqlTpNFSW~L-Z--LQf2BubnmBXDU4ToEMLNqCyeZ2oJ-YZw_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",
    "https://d3c33hcgiwev3.cloudfront.net/_02c1945398be467219866ee1c3294d2d_2sat4.txt?Expires=1733356800&Signature=N16vId4ESebRKKoi6juAaRr-3QqWrgYEFk8KKApZlkSzsll9bzxFlwxRvKV7oDx2oY8~M7Pnm5E20z7K3fmHu7lq2yaeGCjKHjy4VmO0LOf-5~aijqGcXsCy9UC-1969PZaXkskDqpdGc--NxiH-DE4bnl9f2DnGBAEEJ7fwWeE_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",
    "https://d3c33hcgiwev3.cloudfront.net/_02c1945398be467219866ee1c3294d2d_2sat5.txt?Expires=1733356800&Signature=VnC9jJZd7sN0VvBd7MxalOGVY8mDo2gl~ifNEhefnn67SmyII7fZ~TV0bmzYtBTDecB5N4y9QkMiyIzB3mCZ~OSlbyQZM~NRkTaq70f9QyhhDSWhqvfuCnRvJADmtf3l4QAjnj~Zs42koLWzPBwmeRcMGWl0Xi0KdGHPBKclIzM_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A",
    "https://d3c33hcgiwev3.cloudfront.net/_02c1945398be467219866ee1c3294d2d_2sat6.txt?Expires=1733356800&Signature=bnKJ7YshizjhG4aiYGk-KMyCWoFQ~vKc5kItEt3nAYUUqBGsTI2WMpFKBjP80eMLDbkG-f56A~d7KMGoXtoRbfSJtOA3uTy8wk6opPi4ihv1az0XnYnuYe63Ye~4rbldOfpJvqVnVnxfz9oEUJs3E3bl4Mm3N5VOfZO6bSBjqW4_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A"
]

result = solve_2sat_from_urls(urls)
print(result)  # Output: A 6-bit string
