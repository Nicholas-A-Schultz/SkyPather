import math
import heapq
from collections import deque



# Node class (represents a city)
class Node:
    def __init__(self, node_id, weight, x, y):
        self.id = node_id           # City name
        self.weight = weight        # Used for threshold searches (DFS/BFS)
        self.x = x                  # X coordinate (used for heuristic distance)
        self.y = y                  # Y coordinate
        self.neighbors = {}         # Dictionary: {neighbor_node: cost}

    # Add a connection to another node with a travel cost
    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost

    # Required for priority queue comparisons (heapq)
    def __lt__(self, other):
        return self.id < other.id


# Add a bidirectional edge between nodes
def add_undirected_edge(a, b, cost):
    a.add_neighbor(b, cost)
    b.add_neighbor(a, cost)


# Build graph (airports + connections)
def build_graph():
    # Create nodes (city, weight, coordinates)
    jfk = Node("JFK", 5, 90, 80)
    ord_node = Node("ORD", 4, 65, 65)
    atl = Node("ATL", 6, 70, 45)
    dfw = Node("DFW", 3, 45, 40)
    den = Node("DEN", 4, 35, 60)
    las = Node("LAS", 2, 15, 45)
    lax = Node("LAX", 1, 5, 40)

    # Additional nodes (for better testing)
    sea = Node("SEA", 3, 10, 75)
    sfo = Node("SFO", 2, 8, 55)
    phx = Node("PHX", 3, 20, 35)
    iah = Node("IAH", 4, 50, 30)
    mia = Node("MIA", 5, 85, 20)
    bos = Node("BOS", 4, 95, 85)
    clt = Node("CLT", 3, 75, 40)

    # Original edges (flight distances)
    add_undirected_edge(jfk, ord_node, 740)
    add_undirected_edge(jfk, atl, 760)
    add_undirected_edge(ord_node, den, 888)
    add_undirected_edge(ord_node, dfw, 802)
    add_undirected_edge(atl, dfw, 731)
    add_undirected_edge(dfw, den, 641)
    add_undirected_edge(dfw, las, 1055)
    add_undirected_edge(den, las, 628)
    add_undirected_edge(den, lax, 862)
    add_undirected_edge(las, lax, 236)

    # New edges (for better testing)
    add_undirected_edge(lax, sfo, 337)
    add_undirected_edge(sfo, sea, 679)
    add_undirected_edge(sea, den, 1024)
    add_undirected_edge(lax, phx, 370)
    add_undirected_edge(phx, den, 601)
    add_undirected_edge(phx, dfw, 868)
    add_undirected_edge(dfw, iah, 224)
    add_undirected_edge(iah, atl, 689)
    add_undirected_edge(iah, mia, 964)
    add_undirected_edge(atl, clt, 226)
    add_undirected_edge(clt, jfk, 541)
    add_undirected_edge(clt, mia, 650)
    add_undirected_edge(jfk, bos, 187)
    add_undirected_edge(bos, ord_node, 867)

    return jfk  # Return entry point to graph


# Heuristic function (Euclidean distance)
# Used in Greedy + A*
def heuristic(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    return int(math.sqrt(dx * dx + dy * dy))


# Find a node by name using BFS traversal
def find_node(start_node, target_id):
    target_id = target_id.strip().upper()

    visited = set()
    queue = deque([start_node])
    visited.add(start_node)

    while queue:
        current = queue.popleft()

        # Return node if found
        if current.id == target_id:
            return current

        # Traverse neighbors
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return None  # Not found


# DFS with cumulative weight threshold
def dfs_with_threshold(start_node, threshold):
    visited = set()
    stack = [start_node]

    total_weight = 0
    hit = False

    while stack:
        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        total_weight += current.weight

        print(f"Visiting {current.id}, cumulative weight = {total_weight}")

        # Stop if threshold reached
        if total_weight >= threshold:
            print(f"Threshold reached at {current.id} with total = {total_weight}")
            hit = True
            break

        # Add neighbors in reverse order 
        neighbors_list = list(current.neighbors.keys())
        for neighbor in reversed(neighbors_list):
            if neighbor not in visited:
                stack.append(neighbor)

    if not hit:
        print(f"Error: threshold not reached. Final = {total_weight}")


# BFS with cumulative weight threshold
def bfs_with_threshold(start_node, threshold):
    visited = set()
    queue = deque([start_node])
    visited.add(start_node)

    total_weight = 0
    hit = False

    while queue:
        current = queue.popleft()
        total_weight += current.weight

        print(f"Visiting {current.id}, cumulative weight = {total_weight}")

        # Stop if threshold reached
        if total_weight >= threshold:
            print(f"Threshold reached at {current.id} with total = {total_weight}")
            hit = True
            break

        # Explore neighbors level-by-level
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    if not hit:
        print(f"Error: threshold not reached. Final = {total_weight}")


# Greedy Best-First Search
# Uses ONLY heuristic
def greedy_best_first_search(start, goal):
    pq = []
    heapq.heappush(pq, (heuristic(start, goal), start))

    visited = set()
    parent = {start: None}

    while pq:
        _, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        # Goal reached → reconstruct path
        if current == goal:
            path = []
            cost = 0
            temp = current

            while temp:
                path.insert(0, temp.id)
                prev = parent[temp]

                if prev:
                    cost += prev.neighbors[temp]

                temp = prev

            print("Path:", " -> ".join(path))
            print("Cost:", cost)
            return

        # Add neighbors to priority queue
        for neighbor in current.neighbors:
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current
                heapq.heappush(pq, (heuristic(neighbor, goal), neighbor))

    print("Goal not found")


# A* Search (optimal pathfinding)
# Uses g(n) + h(n)
def a_star_search(start, goal):
    g_cost = {start: 0}        # Distance from start
    parent = {start: None}
    visited = set()

    pq = []
    heapq.heappush(pq, (g_cost[start] + heuristic(start, goal), start))

    while pq:
        _, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        # Goal reached → reconstruct path
        if current == goal:
            path = []
            temp = current

            while temp:
                path.insert(0, temp.id)
                temp = parent[temp]

            print("Path:", " -> ".join(path))
            print("Cost:", g_cost[current])
            return

        # Relax edges
        for neighbor, edge_cost in current.neighbors.items():
            new_cost = g_cost[current] + edge_cost

            # Update if better path found
            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                parent[neighbor] = current
                f_cost = new_cost + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_cost, neighbor))

    print("Goal not found")


# Main program loop (user interaction)
def main():
    graph = build_graph()

    while True:
        print("\nNodes: JFK, ORD, ATL, DFW, DEN, LAS, LAX, SEA, SFO, PHX, IAH, MIA, BOS, CLT")
        print("Choose a search method:")
        print("1 DFS with Threshold")
        print("2 BFS with Threshold")
        print("3 Greedy Best-First Search")
        print("4 A* Search")
        print("5 Exit")

        choice = input("Enter choice (1-5): ").strip()

        if not choice.isdigit():
            print("Invalid choice.")
            continue

        choice = int(choice)

        if choice == 5:
            print("Exiting program.")
            break

        # Threshold-based searches
        if choice in (1, 2):
            start = find_node(graph, input("Enter start node: "))

            if not start:
                print("Invalid start node.")
                continue

            threshold = int(input("Enter threshold: "))

            if choice == 1:
                dfs_with_threshold(start, threshold)
            else:
                bfs_with_threshold(start, threshold)

        # Pathfinding searches
        elif choice in (3, 4):
            start = find_node(graph, input("Enter start node: "))
            goal = find_node(graph, input("Enter goal node: "))

            if not start or not goal:
                print("Invalid node(s).")
                continue

            if choice == 3:
                greedy_best_first_search(start, goal)
            else:
                a_star_search(start, goal)

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()