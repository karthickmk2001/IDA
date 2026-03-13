#Graph representation
gr = {
    'S': [('A', 2), ('B', 5)],
    'A': [('C', 4), ('D', 7)],
    'B': [('D', 3), ('E', 6)],
    'C': [('G', 5)],
    'D': [('G', 2)],
    'E': [('G', 4)],
    'G': []
}

# Heuristic values
h = {
    'S': 7,
    'A': 6,
    'B': 4,
    'C': 4,
    'D': 2,
    'E': 3,
    'G': 0
}

goal = 'G'


def ida_star(start):                  #IDA* algorithm implementation
    threshold = h[start]              #Initial threshold is the heuristic value of the start node
    path = [start]                    #Path to keep track of the current path being explored
    while True:                           #Loop until a solution is found or all paths are explored
        temp = search(path, 0, threshold) #Search function to explore the paths, returns "FOUND" if goal is reached, or the minimum f-value if not
        if temp == "FOUND":               #Check if the goal was found
            return path
        if temp == float('inf'):          #If the minimum f-value is infinity, it means all paths have been explored and no solution was found
            return None
        threshold = temp             #Update the threshold to the minimum f-value for the next iteration

def search(path, g, threshold):         #Recursive search function for IDA*
    node = path[-1]                     #Get the current node (last node in the path)
    f = g + h[node]
    if f > threshold:                   #If the f-value exceeds the current threshold, return the f-value to update the threshold for the next iteration
        return f
    if node == goal:                    #If the current node is the goal, return "FOUND" to indicate that a solution has been found
        return "FOUND"
    minimum = float('inf')              #Initialize minimum f-value to infinity, this will be used to find the minimum f-value among the neighbors

    for (nearby, cost) in gr[node]:  #Iterate through the neighbors of the current node
        if nearby not in path:       #Check if the neighbor is not already in the current path to avoid cycles
            path.append(nearby)      #Add the neighbor to the current path
            temp = search(path, g + cost, threshold)   #Recursively call the search function for the neighbor, updating the g-value with the cost to reach the neighbor
            if temp == "FOUND":                   #If the goal was found in the recursive call, return "FOUND" to propagate the success up the call stack
                return "FOUND"
            if temp < minimum:            #If the f-value returned from the recursive call is less than the current minimum, update the minimum f-value
                minimum = temp             #Update the minimum f-value to the smallest f-value returned from the neighbors
            path.pop()                     #Remove the neighbor from the current path to backtrack and explore other paths
    return minimum
result = ida_star('S')                      #Call the IDA* algorithm with the start node 'S' and store the result (the path found) in the variable "result"

if result:                                 #If a path was found, print the path and calculate the total cost of the path
    print("The lowest path from Start node to Goal node:", result)           #Print the path found by the IDA* algorithm
    cost = 0 
    for i in range(len(result) - 1):       #Iterate through the path to calculate the total cost by summing the costs of the edges between consecutive nodes in the path
        for (nearby, c) in gr[result[i]]:  #Iterate through the neighbors of the current node in the path to find the cost of the edge to the next node in the path
            if nearby == result[i + 1]:    #If the neighbor matches the next node in the path, add the cost of that edge to the total cost
                cost += c                  #Add the cost of the edge to the total cost

    print("The Lowest cost from Start node to Goal node:", cost)             #Print the total cost of the path found by the IDA* algorithm

else:
    print("No path found")                 #If no path was found, print a message indicating that no path exists from the start node to the goal node