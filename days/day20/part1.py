from lib.input import fetch

if __name__ == "__main__":
    data = fetch()
    tiles_data = data.strip().split("\n\n")

    tiles = []
    for t in tiles_data:
        idstr, *grid = t.strip().splitlines()
        id_ = int(idstr.split(" ")[1].rstrip(":"))

        gridl = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                if c == "#":
                    gridl[y][x] = 1

        tiles.append((id_, gridl))

    def edges(id_, grid):
        return [
            [grid[0][i] for i in range(len(grid[0]))],
            [grid[-1][i] for i in range(len(grid[0]))],
            [grid[i][0] for i in range(len(grid))],
            [grid[i][-1] for i in range(len(grid))],
        ]

    result = 1

    for id_, grid in tiles:
        nmatched = 0
        for edge in edges(id_, grid):
            for id2, grid2 in tiles:
                if id_ == id2:
                    continue
                for edge2 in edges(id2, grid2):
                    if edge == edge2 or edge == list(reversed(edge2)):
                        nmatched += 1
        if nmatched == 2:
            result *= id_

    print(result)
