import java.util.*;

public class SearchProgram 
{

    // Node class represents each city
    public static class Node 
    {
        public String id;          // Node name
        public int weight;         // Weight used for threshold searches
        public int x, y;           // Coordinates
        public Map<Node, Integer> neighbors; // Adjacent nodes with edge costs

        // Constructor to initialize a node
        public Node(String id, int weight, int x, int y) 
        {
            this.id = id;
            this.weight = weight;
            this.x = x;
            this.y = y;
            this.neighbors = new HashMap<>();
        }

        // Adds a neighbor with an associated travel cost
        public void addNeighbor(Node neighbor, int cost) 
        {
            neighbors.put(neighbor, cost);
        }
    }

    // Creates a bidirectional edge between two nodes
    public static void addUndirectedEdge(Node a, Node b, int cost) 
    {
        a.addNeighbor(b, cost);
        b.addNeighbor(a, cost);
    }

    // Builds the graph (airports and connections)
    public static Node buildGraph() 
    {
        Node jfk = new Node("JFK", 5, 90, 80);
        Node ord = new Node("ORD", 4, 65, 65);
        Node atl = new Node("ATL", 6, 70, 45);
        Node dfw = new Node("DFW", 3, 45, 40);
        Node den = new Node("DEN", 4, 35, 60);
        Node las = new Node("LAS", 2, 15, 45);
        Node lax = new Node("LAX", 1, 5, 40);

        // Add edges (distances between airports)
        addUndirectedEdge(jfk, ord, 740);
        addUndirectedEdge(jfk, atl, 760);
        addUndirectedEdge(ord, den, 888);
        addUndirectedEdge(ord, dfw, 802);
        addUndirectedEdge(atl, dfw, 731);
        addUndirectedEdge(dfw, den, 641);
        addUndirectedEdge(dfw, las, 1055);
        addUndirectedEdge(den, las, 628);
        addUndirectedEdge(den, lax, 862);
        addUndirectedEdge(las, lax, 236);

        return jfk; // Return starting node
    }

    // Heuristic function
    public static int heuristic(Node a, Node b) 
    {
        int dx = a.x - b.x;
        int dy = a.y - b.y;
        return (int)Math.sqrt(dx * dx + dy * dy);
    }

    // Finds a node in the graph using BFS
    public static Node findNode(Node startNode, String targetId) 
    {
        Set<Node> visited = new HashSet<>();
        Queue<Node> queue = new LinkedList<>();
        queue.add(startNode);
        visited.add(startNode);

        while (!queue.isEmpty()) 
        {
            Node current = queue.poll();

            // If found, return it
            if (current.id.equals(targetId)) 
            {
                return current;
            }

            // Traverse neighbors
            for (Node neighbor : current.neighbors.keySet()) 
            {
                if (!visited.contains(neighbor)) 
                {
                    visited.add(neighbor);
                    queue.add(neighbor);
                }
            }
        }
        return null; // Not found
    }

    // Depth-First Search with cumulative weight threshold
    public static void dfsWithThreshold(Node startNode, int threshold) 
    {
        Set<Node> visited = new HashSet<>();
        Stack<Node> stack = new Stack<>();

        int sum = 0;      // Running total of weights
        boolean hit = false;

        stack.push(startNode);

        while (!stack.isEmpty()) 
        {
            Node current = stack.pop();

            if (visited.contains(current)) 
            {
                continue;
            }

            visited.add(current);
            sum += current.weight;

            System.out.println("Visiting " + current.id + ", cumulative weight = " + sum);

            // Stop if threshold reached
            if (sum >= threshold) 
            {
                System.out.println("Threshold reached at " + current.id + " with total = " + sum);
                hit = true;
                break;
            }

            // Add neighbors in reverse order to maintain DFS order
            List<Node> list = new ArrayList<>(current.neighbors.keySet());
            for (int i = list.size() - 1; i >= 0; i--) 
            {
                if (!visited.contains(list.get(i))) 
                {
                    stack.push(list.get(i));
                }
            }
        }

        if (!hit) 
        {
            System.out.println("Error: threshold not reached. Final = " + sum);
        }
    }

    // Breadth-First Search with cumulative weight threshold
    public static void bfsWithThreshold(Node startNode, int threshold) 
    {
        Set<Node> visited = new HashSet<>();
        Queue<Node> queue = new LinkedList<>();

        int sum = 0;
        boolean hit = false;

        queue.add(startNode);
        visited.add(startNode);

        while (!queue.isEmpty()) 
        {
            Node current = queue.poll();

            sum += current.weight;

            System.out.println("Visiting " + current.id + ", cumulative weight = " + sum);

            // Stop if threshold reached
            if (sum >= threshold) 
            {
                System.out.println("Threshold reached at " + current.id + " with total = " + sum);
                hit = true;
                break;
            }

            // Add neighbors level by level
            for (Node n : current.neighbors.keySet()) 
            {
                if (!visited.contains(n)) 
                {
                    visited.add(n);
                    queue.add(n);
                }
            }
        }

        if (!hit) 
        {
            System.out.println("Error: threshold not reached. Final = " + sum);
        }
    }

    // Greedy Best-First Search (uses only heuristic)
    public static void greedyBestFirstSearch(Node start, Node goal) 
    {
        // Priority based only on heuristic distance
        PriorityQueue<Node> pq =
                new PriorityQueue<>((a, b) -> heuristic(a, goal) - heuristic(b, goal));

        Set<Node> visited = new HashSet<>();
        Map<Node, Node> parent = new HashMap<>();

        pq.add(start);
        parent.put(start, null);

        while (!pq.isEmpty()) 
        {
            Node current = pq.poll();

            if (visited.contains(current)) 
            {
                continue;
            }

            visited.add(current);

            // Goal reached → reconstruct path
            if (current == goal) 
            {
                List<String> path = new ArrayList<>();
                int cost = 0;

                Node temp = current;
                while (temp != null) 
                {
                    path.add(0, temp.id);
                    Node prev = parent.get(temp);

                    if (prev != null) 
                    {
                        cost += prev.neighbors.get(temp);
                    }

                    temp = prev;
                }

                System.out.println("Path: " + path);
                System.out.println("Cost: " + cost);
                return;
            }

            // Expand neighbors
            for (Node n : current.neighbors.keySet()) 
            {
                if (!visited.contains(n) && !parent.containsKey(n)) 
                {
                    parent.put(n, current);
                    pq.add(n);
                }
            }
        }

        System.out.println("Goal not found");
    }

    // A* Search
    public static void aStarSearch(Node start, Node goal) 
    {
        Map<Node, Integer> g = new HashMap<>(); // Cost from start
        Map<Node, Node> parent = new HashMap<>();
        Set<Node> visited = new HashSet<>();

        // Priority based on f(n) = g(n) + h(n)
        PriorityQueue<Node> pq =
                new PriorityQueue<>((a, b) ->
                        (g.get(a) + heuristic(a, goal)) - (g.get(b) + heuristic(b, goal)));

        g.put(start, 0);
        parent.put(start, null);
        pq.add(start);

        while (!pq.isEmpty()) 
        {
            Node current = pq.poll();

            if (visited.contains(current)) 
            {
                continue;
            }

            visited.add(current);

            // Goal reached → reconstruct path
            if (current == goal) 
            {
                List<String> path = new ArrayList<>();
                Node temp = current;

                while (temp != null) 
                {
                    path.add(0, temp.id);
                    temp = parent.get(temp);
                }

                System.out.println("Path: " + path);
                System.out.println("Cost: " + g.get(current));
                return;
            }

            // Relax edges
            for (Node n : current.neighbors.keySet()) 
            {
                int newCost = g.get(current) + current.neighbors.get(n);

                if (!g.containsKey(n) || newCost < g.get(n)) 
                {
                    g.put(n, newCost);
                    parent.put(n, current);
                    pq.add(n);
                }
            }
        }

        System.out.println("Goal not found");
    }

    // Main driver program with user interaction
    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);
        Node graph = buildGraph();

        while (true) 
        {
            System.out.println("\nNodes: JFK, ORD, ATL, DFW, DEN, LAS, LAX");
            System.out.println("Choose a search method:");
            System.out.println("1 DFS with Threshold");
            System.out.println("2 BFS with Threshold");
            System.out.println("3 Greedy Best-First Search");
            System.out.println("4 A* Search");
            System.out.println("5 Exit");
            System.out.print("Enter choice (1-5): ");

            int choice = sc.nextInt();
            sc.nextLine();

            if (choice == 5) 
            {
                System.out.println("Exiting program.");
                break;
            }

            // Threshold-based searches
            if (choice == 1 || choice == 2) 
            {
                System.out.print("Enter start node: ");
                Node start = findNode(graph, sc.nextLine());

                if (start == null) 
                {
                    System.out.println("Invalid start node.");
                    continue;
                }

                System.out.print("Enter threshold: ");
                int threshold = sc.nextInt();

                if (choice == 1) 
                {
                    dfsWithThreshold(start, threshold);
                } 
                else 
                {
                    bfsWithThreshold(start, threshold);
                }

            } 
            // Pathfinding searches
            else if (choice == 3 || choice == 4) 
            {
                System.out.print("Enter start node: ");
                Node start = findNode(graph, sc.nextLine());

                if (start == null) 
                {
                    System.out.println("Invalid start node.");
                    continue;
                }

                System.out.print("Enter goal node: ");
                Node goal = findNode(graph, sc.nextLine());

                if (goal == null) 
                {
                    System.out.println("Invalid goal node.");
                    continue;
                }

                if (choice == 3) 
                {
                    greedyBestFirstSearch(start, goal);
                } 
                else 
                {
                    aStarSearch(start, goal);
                }

            } 
            else 
            {
                System.out.println("Invalid choice. Try again.");
            }
        }

        sc.close();
    }
}