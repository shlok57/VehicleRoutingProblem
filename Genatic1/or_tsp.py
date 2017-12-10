# Copyright 2010-2014 Google
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Traveling Salesman Sample.

   This is a sample using the routing library python wrapper to solve a
   Traveling Salesman Problem.
   The description of the problem can be found here:
   http://en.wikipedia.org/wiki/Travelling_salesman_problem.
   The optimization engine uses local search to improve solutions, first
   solutions being generated using a cheapest addition heuristic.
   Optionally one can randomly forbid a set of random connections between nodes
   (forbidden arcs).
"""



import random
from ortools.constraint_solver import pywrapcp
# You need to import routing_enums_pb2 after pywrapcp!
from ortools.constraint_solver import routing_enums_pb2

# Cost/distance functions.


def Distance(i, j):
  """Sample function."""
  # Put your distance code here.
  return i + j

def TSP():
  # Create routing model
  if 3 > 0:
    # TSP of size args.tsp_size
    # Second argument = 1 to build a single tour (it's a TSP).
    # Nodes are indexed from 0 to parser_tsp_size - 1, by default the start of
    # the route is node 0.
    routing = pywrapcp.RoutingModel(3, 1, 0)

    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    # Setting first solution heuristic (cheapest addition).
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    routing.SetArcCostEvaluatorOfAllVehicles(Distance)
    # Forbid node connections (randomly).
    rand = random.Random()
    rand.seed(0)
    forbidden_connections = 0
    
    assignment = routing.Solve()
    if assignment:
      # Solution cost.
      print(assignment.ObjectiveValue())
      # Inspect solution.
      # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1
      route_number = 0
      node = routing.Start(route_number)
      route = ''
      while not routing.IsEnd(node):
        route += str(node) + ' -> '
        node = assignment.Value(routing.NextVar(node))
      route += '0'
      print(route)
    else:
      print('No solution found.')
  else:
    print('Specify an instance greater than 0.')

if __name__ == '__main__':
  TSP()
