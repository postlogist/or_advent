import os
from ortools.constraint_solver import pywrapcp, routing_enums_pb2
import numpy as np
import matplotlib.pyplot as plt


def parse_instance_file(file_name):
    coordinates = {}
    demands = {}
    time_windows = {}
    stand_times = {}
    dimension = None
    capacity = None
    capacity_vol = None

    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Skip the initial comment section marked by ###
    lines = iter(lines)

    section = None
    for line in lines:
        line = line.strip()
        if line.startswith("DIMENSION"):
            dimension = int(line.split(':')[1].strip())
        elif line.startswith("CAPACITY "):
            capacity = int(line.split(':')[1].strip())
        elif line.startswith("CAPACITY_VOL"):
            capacity_vol = int(line.split(':')[1].strip())
        elif line == "NODE_COORD_SECTION":
            section = "coordinates"
            continue
        elif line == "PICKUP_SECTION":
            section = "pickups"
            continue
        elif line == "DEMAND_SECTION":
            section = "demands"
            continue
        elif line == "TIME_WINDOW_SECTION":
            section = "time_windows"
            continue
        elif line == "STANDTIME_SECTION":
            section = "stand_times"
            continue
        elif line == "DEPOT_SECTION":
            section = "depot"
            continue
        elif line == "EOF":
            break

        if section == "coordinates" and line:
            parts = line.split()
            node_id, x, y = int(parts[0]) - 1, int(parts[1]), int(parts[2])
            coordinates[node_id] = (x, y)
        elif section == "demands" and line:
            parts = line.split()
            node_id, demand = int(parts[0]) - 1, int(parts[1])
            demands[node_id] = demand
        elif section == "time_windows" and line:
            parts = line.split()
            node_id = int(parts[0]) - 1
            begin_hh, begin_mm = map(int, parts[1].split(':'))
            end_hh, end_mm = map(int, parts[2].split(':'))
            time_windows[node_id] = (
                begin_hh * 60 + begin_mm, end_hh * 60 + end_mm)
        elif section == "stand_times" and line:
            parts = line.split()
            node_id, stand_time = int(parts[0]) - 1, int(parts[1])
            stand_times[node_id] = stand_time
        elif section == "depot" and line.isdigit():
            depot = int(line) - 1
    time_windows[0] = (0, 1400)
    stand_times[0] = 0
    return coordinates, demands, time_windows, stand_times, dimension, capacity, capacity_vol


def create_time_matrix(coordinates):
    locations = list(coordinates.values())
    time_matrix = {}
    speed = 1000  # Speed in km/h
    for from_index, from_node in enumerate(locations):
        time_matrix[from_index] = {}
        for to_index, to_node in enumerate(locations):
            if from_index == to_index:
                time_matrix[from_index][to_index] = 0
            else:
                distance = np.linalg.norm(
                    np.array(from_node) - np.array(to_node))   # Distance in km
                time_matrix[from_index][to_index] = int(
                    distance / speed * 60)  # Time in minutes
    return time_matrix


def extract_solution(manager, routing, solution, time_dimension, data):
    total_time = 0
    total_load = 0
    total_demand = 0
    active_vehicles = 0

    for vehicle_id in range(routing.vehicles()):
        index = routing.Start(vehicle_id)
        route_time = 0
        route_load = 0
        route_demand = 0
        route = []

        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data["demands"][node_index]
            load = solution.Value(
                routing.GetDimensionOrDie('Capacity').CumulVar(index))
            time_var = time_dimension.CumulVar(index)
            time = solution.Value(time_var)
            time_window = data['time_windows'][node_index]
            demand = data['demands'][node_index]

            route.append((node_index, time, time_window, demand))
            # route_load = max(route_load, load)
            route_demand += demand

            previous_index = index
            index = solution.Value(routing.NextVar(index))
            if not routing.IsEnd(index):
                route_time += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)

        if route_time > 0:
            active_vehicles += 1
            total_time += route_time
            total_load += route_load
            total_demand += route_demand

            print(f"\nSleigh {vehicle_id}: Load {route_load}")
            for node in route:
                if node[0] == 0:
                    print(f"Santa's depot {node[0]}: Time {node[1]}")
                else:
                    print(f"Child {node[0]}: Time {node[1]} [{
                        node[2][0]}, {node[2][1]}] Demand {node[3]}")

    print("\nSummary:")
    print(f"Active sleighs: {active_vehicles}")
    print(f"Total time: {total_time} minutes")
    print(f"Total load: {total_load}")
    print(f"Total demand: {total_demand}")

    return total_time, total_load, total_demand


def main():

    os.chdir('Day24')  # Change to the appropriate folder
    file_name = 'instance_clean.txt'
    # file_name = 'instance_tiny.txt'

    # Parse input data
    coordinates, demands, time_windows, stand_times, dimension, capacity, capacity_vol = parse_instance_file(
        file_name)

    # Define data model
    data = {}
    data['time_matrix'] = create_time_matrix(coordinates)
    data['demands'] = list(demands.values())
    data['time_windows'] = list(time_windows.values())
    data['stand_times'] = list(stand_times.values())
    # Example: 10 vehicles with given capacity
    data['vehicle_capacities'] = [capacity] * 60
    data['num_vehicles'] = len(data['vehicle_capacities'])
    data['depot'] = 0

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(
        len(data['time_matrix']), data['num_vehicles'], data['depot'])

    routing_parameters = pywrapcp.DefaultRoutingModelParameters()
    routing_parameters.solver_parameters.trace_propagation = True
    routing_parameters.solver_parameters.trace_search = True

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)  # , routing_parameters

    # Create and register a transit callback

    def time_callback(from_index, to_index):
        # Returns the travel time between the two nodes
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['time_matrix'][from_node][to_node] + data['stand_times'][from_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Capacity constraint

    def demand_callback(from_index):
        # Returns the demand of the node
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # Null capacity slack
        data['vehicle_capacities'],  # Vehicle maximum capacities
        True,  # Start cumul to zero
        'Capacity')

    # Add Time Window constraint
    routing.AddDimension(
        transit_callback_index,
        600,  # Allow waiting time
        1440,  # Maximum time per vehicle
        False,  # Don't force start cumul to zero
        'Time')

    time_dimension = routing.GetDimensionOrDie('Time')
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data["depot"]
    for vehicle_id in range(data["num_vehicles"]):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data["time_windows"][depot_idx][0], data["time_windows"][depot_idx][1]
        )
    for i in range(data["num_vehicles"]):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i))
        )
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # Setting search heuristic to Tabu Search
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH)
    # search_parameters.local_search_metaheuristic = (
    #    routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.log_search = True

    search_parameters.time_limit.seconds = 300

    # Setting search heuristic to Greedy Algorithm
    # search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    # search_parameters.first_solution_strategy = (
    #    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # search_parameters.time_limit.seconds = 30

    # Solve the problem
    print("Starting the solver...")
    solution = routing.SolveWithParameters(search_parameters)

    solver_statuses = {
        0:	'ROUTING_NOT_SOLVED: Problem not solved yet.',
        1:	'ROUTING_SUCCESS: Problem solved successfully.',
        2: 'ROUTING_PARTIAL_SUCCESS_LOCAL_OPTIMUM_NOT_REACHED: Problem solved successfully after calling RoutingModel.Solve(), except that a local optimum has not been reached. Leaving more time would allow improving the solution.',
        3:	'ROUTING_FAIL: No solution found to the problem.',
        4:	'ROUTING_FAIL_TIMEOUT: Time limit reached before finding a solution.',
        5:	'ROUTING_INVALID: Model, model parameters, or flags are not valid.',
        6: 'ROUTING_INFEASIBLE: Problem proven to be infeasible.'
    }
    print("Solver status: ", routing.status(),
          solver_statuses.get(routing.status()))

    # Print solution and visualize
    if solution:
        print("Solution found! Printing solution...")
        total_time, total_load, total_demand = extract_solution(
            manager, routing, solution, time_dimension, data)
    else:
        print("No solution found!")


if __name__ == '__main__':
    main()
