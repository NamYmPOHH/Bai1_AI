from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


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
    Q = []          # List Q
    L = deque()     # Queue

    L.append(start)
    visited.add(start)
    parent[start] = None
    Q.append(start)

    with open(output_file, "w", encoding="utf-8") as out:
        out.write(f"{'Expanded':<15}{'Adjacency':<20}{'List Q':<25}{'List L'}\n")
        out.write("-" * 75 + "\n")

        while L:
            u = L.popleft()

            if u == goal:
                out.write(f"{u:<15}{'Stop':<20}\n")
                break

            adj = graph.get(u, [])

            for v in adj:
                if v not in visited:
                    visited.add(v)
                    parent[v] = u
                    L.append(v)
                    Q.append(v)

            out.write(
                f"{u:<15}"
                f"{' '.join(adj):<20}"
                f"{' '.join(Q):<25}"
                f"{' '.join(L)}\n"
            )

    # Truy vết đường đi BFS
    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()

    with open(output_file, "a", encoding="utf-8") as out:
        out.write("\nPath: " + " -> ".join(path))

    return path


def draw_graph(graph, bfs_path):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()

    for u in graph:
        for v in graph[u]:
            G.add_edge(u, v)

    # Tự động tính toán vị trí để không bị lỗi với input mới
    pos = nx.spring_layout(G, seed=42)
    try:
        from networkx.drawing.nx_pydot import graphviz_layout
        pos = graphviz_layout(G, prog='dot')
    except ImportError:
        # Tự viết một layout dạng cây nếu không có graphviz
        start_node = bfs_path[0] if bfs_path else list(G.nodes)[0]
        try:
            distances = nx.single_source_shortest_path_length(G, start_node)
        except Exception:
            distances = {start_node: 0}
            
        max_dist = max(distances.values()) if distances else 0
        layers = {}
        for n in G.nodes:
            layers[n] = distances.get(n, max_dist + 1)
            
        layer_nodes = {}
        for n, layer in layers.items():
            layer_nodes.setdefault(layer, []).append(n)
            
        pos = {}
        for layer, nodes in layer_nodes.items():
            width = len(nodes)
            for i, n in enumerate(nodes):
                pos[n] = ((i - width / 2.0 + 0.5) * 4, -layer * 3)

    plt.figure(figsize=(10, 7))

    # Vẽ node
    nx.draw_networkx_nodes(
        G, pos,
        node_size=1800,
        node_color='white',
        edgecolors='black',
        linewidths=1.5
    )

    # Vẽ nhãn
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_weight='bold'
    )

    # 1️⃣ Vẽ TẤT CẢ cạnh (màu đen, CÓ mũi tên)
    nx.draw_networkx_edges(
        G, pos,
        edge_color='black',
        width=1.5,
        arrows=True,
        arrowstyle='-|>',
        arrowsize=18,
        node_size=1800,
        connectionstyle='arc3'
    )

    # 2️⃣ Vẽ cạnh BFS (màu đỏ, mũi tên to hơn)
    bfs_edges = [(bfs_path[i], bfs_path[i + 1])
                 for i in range(len(bfs_path) - 1)]

    nx.draw_networkx_edges(
        G, pos,
        edgelist=bfs_edges,
        edge_color='red',
        width=4,
        arrows=True,
        arrowstyle='-|>',
        arrowsize=25,
        node_size=1800,
        connectionstyle='arc3'
    )

    title = f"BFS Graph"
    if bfs_path:
        title += f" ({bfs_path[0]} → {bfs_path[-1]})"
    plt.title(title, fontsize=14)
    plt.axis('off')
    plt.show()



def main():
    graph, start, end = read_input("input.txt")
    bfs_path = bfs(graph, start, end, "output.txt")
    draw_graph(graph, bfs_path)


if __name__ == "__main__":
    main()
