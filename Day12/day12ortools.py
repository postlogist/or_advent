# Code to solve TSP with Google OR Tools
import os
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# Create the data


def create_data_model(filename):
    """
    Reads TSP instance data from a file and returns a data dictionary
    with the distance matrix, number of vehicles and depot index.
    """
    data = {}
    dimension = None
    distance_matrix = []

    # Read the entire file
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Strip whitespace from each line
    lines = [line.strip() for line in lines if line.strip()]

    # Find the DIMENSION and EDGE_WEIGHT_SECTION indices
    dimension_line = next(
        (l for l in lines if l.startswith('DIMENSION')), None)
    if dimension_line:
        # Format: DIMENSION: <number>
        parts = dimension_line.split(':')
        dimension = int(parts[1].strip())

    # Locate the start of the EDGE_WEIGHT_SECTION
    # The line "EDGE_WEIGHT_SECTION" marks where matrix lines start.
    start_index = None
    for i, line in enumerate(lines):
        if line.startswith('EDGE_WEIGHT_SECTION'):
            start_index = i + 1
            break

    if dimension is None or start_index is None:
        raise ValueError(
            "Could not find DIMENSION or EDGE_WEIGHT_SECTION in the file.")

    # Now read exactly 'dimension' lines of matrix data
    # Note: The FULL_MATRIX format should contain exactly dimension lines,
    # each with dimension distances.
    # However, sometimes the matrix may span multiple lines due to formatting.
    # We'll need to accumulate numbers until we have dimension^2 numbers.

    matrix_numbers = []
    for line in lines[start_index:]:
        # Split by whitespace to get numbers
        parts = line.split()
        # Convert to int
        nums = [int(x) for x in parts]
        matrix_numbers.extend(nums)
        # Break if we have enough numbers
        if len(matrix_numbers) >= dimension * dimension:
            break

    # Construct the matrix
    if len(matrix_numbers) < dimension * dimension:
        raise ValueError(
            "Not enough distance entries found for a full matrix.")

    # Slice the flat list into a square matrix
    distance_matrix = [
        matrix_numbers[i*dimension:(i+1)*dimension] for i in range(dimension)]

    data["distance_matrix"] = distance_matrix
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


os.chdir('Day12')

# Create the routing model
data = create_data_model("instance.txt")
manager = pywrapcp.RoutingIndexManager(
    len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
)
routing = pywrapcp.RoutingModel(manager)

# Create the distance callback


def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data["distance_matrix"][from_node][to_node]


transit_callback_index = routing.RegisterTransitCallback(distance_callback)


# Set the cost of travel
routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# Set search parameters
search_parameters = pywrapcp.DefaultRoutingSearchParameters()

# Option 1: Greedy, 2763 miles
# search_parameters.first_solution_strategy = (
#     routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
# )

# Option 2: Local Search, 30 sec: 2752 # GUIDED_LOCAL_SEARCH #2729 SIMULATED_ANNEALING #2727 TABU_SEARCH
search_parameters.local_search_metaheuristic = (
    routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)
search_parameters.time_limit.seconds = 600
search_parameters.log_search = True

"""
AUTOMATIC	Lets the solver select the metaheuristic.
GREEDY_DESCENT	Accepts improving(cost-reducing) local search neighbors until a local minimum is reached.
GUIDED_LOCAL_SEARCH	Uses guided local search to escape local minima. (cf. Guided Local Search) this is generally the most efficient metaheuristic for vehicle routing.
SIMULATED_ANNEALING	Uses simulated annealing to escape local minima(cf. Simulated Annealing).
TABU_SEARCH	Uses tabu search to escape local minima(cf. Tabu Search).
GENERIC_TABU_SEARCH	Uses tabu search on the objective value of solution to escape local minima.
"""

# Add the solution printer


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index) + 1} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(
            previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index) + 1}\n"
    print(plan_output)
    plan_output += f"Route distance: {route_distance}km\n"


# Solve and print the solution
solution = routing.SolveWithParameters(search_parameters)
if solution:
    print_solution(manager, routing, solution)

# Save routes to a list or array


def get_routes(solution, routing, manager):
    """Get vehicle routes from a solution and store them in an array."""
    # Get vehicle routes and store them in a two dimensional array whose
    # i,j entry is the jth location visited by vehicle i along its route.
    routes = []
    for route_nbr in range(routing.vehicles()):
        index = routing.Start(route_nbr)
        route = [manager.IndexToNode(index)]
        while not routing.IsEnd(index):
            index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))
        routes.append(route)
    return routes
