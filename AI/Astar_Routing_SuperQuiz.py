#Rhys Jennings
#25/08/2020
#A* Routing Program to find the shortest path between a starting node and a goal node from a grid input. 


from search import *
import math
import heapq

class RoutingGraph(Graph):
    """Routing Graph"""
    
    def __init__(self, text_representation):
        self.graph = []
        text_representation = text_representation.strip()
        
        self.goal_nodes = []
        for i in text_representation.splitlines():
            row = []
            for j in i.strip():
                row.append(j)
            self.graph.append(row)
    
    
        self.directions = [('N', -1, 0),('E',  0, 1),('S',  1, 0),('W',  0, -1)] 

        
    
    def starting_nodes(self):
        self.start_nodes = []
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                node = self.graph[i][j]
                if node == 'S':
                    self.start_nodes.append((i, j, math.inf))
                elif node.isdigit() == True:
                    self.start_nodes.append((i, j, int(node)))
                elif node == 'G':
                    self.goal_nodes.append((i, j))
        return self.start_nodes
    
    def is_goal(self, node):
            """Returns true if the given node is a goal state, false otherwise."""
            
            row, column, fuel = node
            if self.graph[row][column] == 'G':
                return True
            else:
                return False
            
    def outgoing_arcs(self, tail_node):
            """Given a node it returns a sequence of arcs (Arc objects)
            which correspond to the actions that can be taken in that
            state (node)."""    
            arcs = []
            
            row, column, fuel = tail_node
                      
            for i in self.directions:
                direction, row_move, column_move = i
                potential_move = self.graph[row + row_move][column + column_move]
                if potential_move != '-' and potential_move != '|' and potential_move != 'X' and fuel != 0:
                    arcs.append(Arc(tail_node, (row + row_move, column + column_move, fuel-1), direction, 5))
            
            if fuel <= 8 and self.graph[row][column] == 'F':
                arcs.append(Arc(tail_node, (row , column, 9), 'Fuel up', 15))  
            return arcs
        
        
    def estimated_cost_to_goal(self, node):
        """Return the estimated cost to a goal node from the given
        state. This function is usually implemented when there is a
        single goal state. The function is used as a heuristic in
        search. The implementation should make sure that the heuristic
        meets the required criteria for heuristics."""
        i, j, fuel = node
        lowest_goal = math.inf
        
        for goal in self.goal_nodes:
            goal_i, goal_j = goal
            guess_distance = float(abs(i - goal_i) + abs(j - goal_j))
            if guess_distance <= lowest_goal:
                lowest_goal = guess_distance 
        return lowest_goal * 5
            
class AStarFrontier(Frontier):

    def __init__(self, map_graph):
        self.map_graph = map_graph
        self.container = []
        self.paths = set()
        self.count = 0
        self.expanded = set()

    def add(self, path):
        if path[-1].head not in self.paths:
            self.paths.add(path[-1].head)
            cost = 0 
            for i in path: 
                cost += i.cost
            h = self.map_graph.estimated_cost_to_goal(path[-1].head) + cost
            heapq.heappush(self.container, ([h, self.count], path))
                       
            self.count += 1


    def __iter__(self):
        """We don't need a separate iterator object. Just return self. You
        don't need to change this method."""
        return self    

    def __next__(self):
        if len(self.container) > 0:
                
            
            expand = heapq.heappop(self.container)[1]
            self.expanded.add(expand[-1].head)
            return expand
        else:
            raise StopIteration
            

def print_map(map_graph, frontier, solution):
    new_graph = map_graph.graph
    if solution is not None:
        for i in solution[1:-1]:
            tail, head, action, cost = i
            row, column, fuel = head
            new_graph[row][column] = '*'
        
            
    for i in frontier.expanded:
        if i is not None:
            row, column, fuel = i
                
            if new_graph[row][column] == ' ':
                new_graph[row][column] = '.'
            
    for i in new_graph:
        print("".join(i))   
    
            
    
def main():
    """main stuss"""
    
    
    map_str = """\
    +----------------+
    |                |
    |                |
    |                |
    |                |
    |                |
    |                |
    |        S       |
    |                |
    |                |
    |     G          |
    |                |
    |                |
    |                |
    +----------------+
    """
    
    map_graph = RoutingGraph(map_str)
    frontier = AStarFrontier(map_graph)
    solution = next(generic_search(map_graph, frontier), None)
    print_map(map_graph, frontier, solution)
                
if __name__ == "__main__":
    main()