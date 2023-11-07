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


def find_shortest_path(start_position, end_position, walls, grid):
    convert_walls_to_prolog(walls)
    convert_grid_to_prolog(grid)

    query = f'find_shortest_path({start_position}, {end_position}, Path, Cost).'
    results = list(prolog.query(query))

    retract_all_walls(walls)
    # Process the results
    if results:
        # Extract the path as a list of tuples
        shortest_path = list(results[0]['Path'])
        cost = results[0]['Cost']
        return shortest_path, cost
    else:
        return None, None
