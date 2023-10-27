import subprocess


def run_prolog_query(query):
    prolog_process = subprocess.Popen(
        ['swipl', '-q', '-s', 'aStar.pl'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    prolog_process.stdin.write(query)
    prolog_process.stdin.flush()

    prolog_output = prolog_process.communicate()[0]
    prolog_process.stdin.close()
    prolog_process.wait()

    return prolog_output


if __name__ == '__main__':
    grid = [(i, j) for i in range(0, 7) for j in range(0, 7)]
    walls = {cell: {'E': 0, 'W': 0, 'N': 0, 'S': 0} for cell in grid}
    # Query to run A* algorithm with parameters
    prolog_query = f"a_star({grid}, {(1, 1)}, {(3, 3)}, {walls}, Path).\n"

    # Run the Prolog query
    output = run_prolog_query(prolog_query)

    print(output)
