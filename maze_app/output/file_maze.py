import sys


def generetor_file_maze(
    matrix: list[list[int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
    way: str,
    name_file: str,
) -> None:
    """Save the maze matrix, entry, exit, and solution to a file.

    Args:
        matrix: Maze grid encoded as integers.
        entry: Entry coordinate (row, col).
        exit: Exit coordinate (row, col).
        way: Solution path as a string.
        name_file: Output filename.

    Raises:
        SystemExit: If the file cannot be written.
    """
    try:
        with open(name_file, 'w') as f:
            for line in matrix:
                line_hex = "".join(format(x, 'X') for x in line)
                f.write(line_hex + '\n')
            f.write('\n')
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(f"{way}\n")
    except OSError as e:
        sys.stderr.write(f"Error writing output file: {e.strerror}")
        sys.exit(1)
