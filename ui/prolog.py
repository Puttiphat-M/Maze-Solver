from pyswip import Prolog

# Initialize Prolog engine
prolog = Prolog()

# Load Prolog code
prolog.consult('aStar.pl')


def convert_walls_to_prolog(walls):
    for cell, directions in walls.items():
        for direction, value in directions.items():
            prolog.assertz(f'wall({cell[0]}, {cell[1]}, {direction}, {value})')
            # print(f'wall({cell[0]}, {cell[1]}, {direction}, {value})')


def retract_all_walls(walls):
    for cell, directions in walls.items():
        for direction, value in directions.items():
            prolog.retract(f'wall({cell[0]}, {cell[1]}, {direction}, {value})')


def convert_grid_to_prolog(grid):
    for cell in grid:
        prolog.assertz(f'cell({cell[0]}, {cell[1]})')
        # print(f'cell({cell[0]}, {cell[1]})')


def find_shortest_path(start_position, end_position):
    # Call the find_shortest_path/4 predicate in Prolog
    query = f'find_shortest_path({start_position}, {end_position}, Path, Cost).'
    results = list(prolog.query(query))

    # Process the results
    if results:
        # Extract the path as a list of tuples
        shortest_path = list(results[0]['Path'])
        cost = results[0]['Cost']
        return shortest_path, cost
    else:
        return None, None


# Example data
# walls = {
#     (1, 1): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (1, 2): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (1, 3): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (1, 4): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (1, 5): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (2, 1): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (2, 2): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (2, 3): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (2, 4): {'e': 1, 'w': 0, 'n': 0, 's': 0},
#     (2, 5): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (3, 1): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (3, 2): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (3, 3): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (3, 4): {'e': 0, 'w': 1, 'n': 0, 's': 0},
#     (3, 5): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (4, 1): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (4, 2): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (4, 3): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (4, 4): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (4, 5): {'e': 0, 'w': 0, 'n': 0, 's': 0},
#     (5, 1): {'e': 0, 'w': 0, 'n': 0, 's': 0}
# }
# grid = [cell for cell in walls.keys()]
#
# # Convert walls to Prolog predicates
# convert_walls_to_prolog(walls)
#
# # Convert cells to Prolog predicates
# convert_grid_to_prolog(grid)
#
# # Example start and end positions
# start_position = (1, 4)
# end_position = (4, 4)
#
# # Find the shortest path
# query = f'a_star({start_position}, {end_position}, Path, Cost)'
# result = list(prolog.query(query))
#
# # Print the result
# if result:
#     path = result[0]['Path']
#     cost = result[0]['Cost']
#     print(f'Shortest path: {path}')
#     print(f'Cost: {cost}')
# else:
#     print('No path found')
