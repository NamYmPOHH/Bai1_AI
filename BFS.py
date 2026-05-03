from collections import deque

def read_input(filename):
    graph = {}
    start = end = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("Start"):
                start = line.split(":")[1].strip()
            elif line.startswith("End"):
                end = line.split(":")[1].strip()
            else:
                u, v = line.split(":")
                graph[u.strip()] = v.strip().split()

    return graph, start, end


def bfs(graph, start, goal, output_file):
    visited = set()
    parent = {}
    Q = []          # List Q: visited order
    L = deque()     # List L: queue

    L.append(start)
    visited.add(start)
    parent[start] = None
    Q.append(start)

    with open(output_file, "w", encoding="utf-8") as out:
        # Header
        out.write(f"{'Expanded':<15}{'Adjacency':<20}{'List Q':<25}{'List L'}\n")
        out.write("-" * 75 + "\n")

        while L:
            u = L.popleft()

            # Goal check
            if u == goal:
                out.write(f"{u:<15}{'Stop':<20}\n")
                break

            adj = graph.get(u, [])

            # Add neighbors
            for v in adj:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    L.append(v)
                    Q.append(v)

            # Print table row
            adj_str = " ".join(adj)
            q_str = " ".join(Q)
            l_str = " ".join(L)

            out.write(f"{u:<15}{adj_str:<20}{q_str:<25}{l_str}\n")

        # Reconstruct path
        path = []
        cur = goal
        while cur:
            path.append(cur)
            cur = parent.get(cur)

        path.reverse()
        out.write("\nPath: " + " -> ".join(path))


def main():
    graph, start, end = read_input("input.txt")
    bfs(graph, start, end, "output.txt")

if __name__ == "__main__":
    main()
