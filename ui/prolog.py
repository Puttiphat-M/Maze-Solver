import subprocess


def run_prolog_query(query):
    prolog_process = subprocess.Popen(
        ['swipl', '-q', '-s', 'a_star.pl'],  # Use 'swipl' and consult the Prolog file
        stdin=subprocess.PIPE,  # Allow Python to write to Prolog's stdin
        stdout=subprocess.PIPE,  # Capture Prolog's stdout
        stderr=subprocess.PIPE,  # Capture Prolog's stderr
        universal_newlines=True,  # Use text mode for communication
    )

    prolog_process.stdin.write(query)
    prolog_process.stdin.flush()

    prolog_output = prolog_process.communicate()[0]
    prolog_process.stdin.close()
    prolog_process.wait()

    # Parse the path from the output
    path = [tuple(map(int, p.split(','))) for p in prolog_output.strip().split()]

    return path


