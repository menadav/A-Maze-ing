import sys


def generetor_file_maze(matrix, entry, exit, way, name_file="maze.out"):
    try:
        with open(name_file, 'w') as f:
            for line in matrix:
                line_hex = ""
                for x in line:
                    line_hex += format(x, 'X')
                f.write(line_hex + '\n')
            f.write('\n')
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(f"{way}\n")
    except OSError as e:
        print(f"Error writing output file: {e.strerror}")
        sys.exit(1)
