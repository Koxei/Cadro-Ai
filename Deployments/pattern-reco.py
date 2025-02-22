import networkx as nx
import random

# Generate a synthetic transaction graph
def generate_transaction_graph(num_nodes=10, num_edges=15):
    G = nx.DiGraph()
    for i in range(num_nodes):
        G.add_node(i, account_balance=random.uniform(100, 10000))
    
    for _ in range(num_edges):
        sender = random.randint(0, num_nodes - 1)
        receiver = random.randint(0, num_nodes - 1)
        if sender != receiver:
            G.add_edge(sender, receiver, amount=random.uniform(1, 500))
    
    return G

# Detect wash trading cycles using cyclomatic complexity analysis
def detect_wash_trading(graph):
    cycles = list(nx.simple_cycles(graph))
    suspicious_cycles = [cycle for cycle in cycles if len(cycle) > 2]  # Wash trades often involve loops
    
    if suspicious_cycles:
        print("Potential wash trading detected in cycles:")
        for cycle in suspicious_cycles:
            print(cycle)
    else:
        print("No suspicious trading patterns detected.")

# Detect market manipulation based on transaction clustering
def detect_market_manipulation(graph):
    in_degree = dict(graph.in_degree())
    out_degree = dict(graph.out_degree())
    high_activity_nodes = [node for node in graph.nodes if in_degree[node] > 3 and out_degree[node] > 3]
    
    if high_activity_nodes:
        print("Potential market manipulation detected involving nodes:", high_activity_nodes)
    else:
        print("No signs of market manipulation detected.")

# Main execution
def main():
    transaction_graph = generate_transaction_graph()
    detect_wash_trading(transaction_graph)
    detect_market_manipulation(transaction_graph)

if __name__ == "__main__":
    main()
