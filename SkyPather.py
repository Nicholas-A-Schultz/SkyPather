import heapq
import matplotlib.pyplot as plt
import weatherapi as wx
import points as pts


# Build graph by calling points.py functions directly

def build_graph():
    print("Fetching weather info from AviationWeather.gov...")
    wx.populateWindData()
    print("Fetched.")

    fixes = pts.readFixesFromFile("fixes.txt")
    pts.readAirportsFromFile("airports.txt", fixes)
    return fixes


# Weather-aware heuristic using imported weather + points data

def heuristic(current, goal, altitude=3000):
    base_distance = current.distanceTo(goal) * 60

    mid_lat = (current.latitude + goal.latitude) / 2
    mid_lon = (current.longitude + goal.longitude) / 2

    try:
        direction, speed, _ = wx.getWindData(mid_lat, mid_lon, altitude)
        wind = pts.windAsComplex(direction, speed)

        intended_x = goal.longitude - current.longitude
        intended_y = goal.latitude - current.latitude
        intended = complex(intended_x, intended_y)

        return abs(intended - wind) * 60
    except Exception:
        return base_distance


# Find a node by input using points.py directly

def find_node(fixes, input):
    return pts.findFixByCode(fixes, input.strip().upper())


# Greedy Best-First Search

def greedy_best_first_search(start, goal, altitude=3000):
    pq = []
    heapq.heappush(pq, (heuristic(start, goal, altitude), start))

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
                path.insert(0, temp.code)
                prev = parent[temp]
                if prev:
                    cost += prev.distanceTo(temp) * 60
                temp = prev

            print("Path:", " -> ".join(path))
            print("Cost:", round(cost, 2))
            return path

        # Add neighbors to priority queue
        for neighbor in current.neighbors:
            if neighbor not in visited and neighbor not in parent:
                parent[neighbor] = current
                heapq.heappush(pq, (heuristic(neighbor, goal, altitude), neighbor))

    print("Goal not found")


# A* Search

def a_star_search(start, goal, altitude=3000):
    g_cost = {start: 0}     # Distance from start
    parent = {start: None}
    visited = set()

    pq = []
    heapq.heappush(pq, (heuristic(start, goal, altitude), start))

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
                path.insert(0, temp.code)
                temp = parent[temp]

            print("Path:", " -> ".join(path))
            print("Cost:", round(g_cost[current], 2))
            return path

        # Relax edges
        for neighbor in current.neighbors:
            edge_cost = current.distanceTo(neighbor) * 60
            new_cost = g_cost[current] + edge_cost

             # Update if better path found
            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost
                parent[neighbor] = current
                f_cost = new_cost + heuristic(neighbor, goal, altitude)
                heapq.heappush(pq, (f_cost, neighbor))

    print("Goal not found")


# Main program loop

def main():
    fixes = build_graph()
    fig, ax = plt.subplots()

    # Plot the Florida map
    img = plt.imread("florida.png")
    ax.imshow(img)
    # Plot all the fixes
    pts.plotFixesToGraph(fixes,ax)

    while True:
        print("\nAvailable nodes:")
        print(", ".join(sorted(fix.code for fix in fixes)))
        print("Choose a search method:")
        print("1 Greedy Best-First Search")
        print("2 A* Search")
        print("3 Exit")

        choice = input("Enter choice (1-3): ").strip()

        if not choice.isdigit():
            print("Invalid choice.")
            continue

        choice = int(choice)

        if choice == 3:
            print("Exiting program.")
            break

        # Pathfinding searches
        if choice in (1, 2):
            start = find_node(fixes, input("Enter start node: "))
            goal = find_node(fixes, input("Enter goal node: "))

            if not start or not goal:
                print("Invalid node(s).")
                continue

            if choice == 1:
                path = greedy_best_first_search(start, goal)
                pathFixes = pts.fixListFromCodeList(fixes, path)
                
            else:
                path = a_star_search(start, goal)
        else:
            print("Invalid choice.")




if __name__ == "__main__":
    main()
