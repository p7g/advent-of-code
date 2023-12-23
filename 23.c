#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

#define SIZE 141
#define GOAL_X (SIZE - 2)
#define GOAL_Y (SIZE - 1)

static char grid[SIZE][SIZE] = {0};
static int seen[SIZE][SIZE] = {0};

static int search(int, int, int);

static int search_one(int x, int y, int ignore_slopes) {
    if (x < 0 || y < 0 || x >= SIZE || y >= SIZE) return -1;
    char c = grid[y][x];
    if (c == '#') return -1;
    if (seen[y][x]) return -1;
    if (x == GOAL_X && y == GOAL_Y) return 1;
    seen[y][x] = 1;
    int result = search(x, y, ignore_slopes);
    seen[y][x] = 0;
    return result;
}

static int search(int x, int y, int ignore_slopes) {
    int longest = -1;
    int length;

    if (grid[y][x] == '.' || ignore_slopes) {
        length = search_one(x + 1, y, ignore_slopes);
        if (length > longest) longest = length;
        length = search_one(x - 1, y, ignore_slopes);
        if (length > longest) longest = length;
        length = search_one(x, y + 1, ignore_slopes);
        if (length > longest) longest = length;
        length = search_one(x, y - 1, ignore_slopes);
        if (length > longest) longest = length;
    } else {
        switch (grid[y][x]) {
        case '>':
            length = search_one(x + 1, y, 0);
            break;
        case '<':
            length = search_one(x - 1, y, 0);
            break;
        case '^':
            length = search_one(x, y - 1, 0);
            break;
        case 'v':
            length = search_one(x, y + 1, 0);
            break;
        default:
            abort();
        }
        if (length > longest) longest = length;
    }

    return longest == -1 ? longest : longest + 1;
}

int main() {
    FILE *f = fopen(".aoc-cache/2023-23.txt", "r");
    for (int y = 0; y < SIZE; y++) {
        for (int x = 0; x < SIZE; x++)
            grid[y][x] = (char) fgetc(f);
        assert(fgetc(f) == '\n');
    }
    assert(fgetc(f) == EOF);
    fclose(f);

    printf("%d\n", search(1, 0, 0) - 1);

    for (int y = 0; y < SIZE; y++)
        for (int x = 0; x < SIZE; x++)
            seen[y][x] = 0;

    printf("%d\n", search(1, 0, 1) - 1);

    return 0;
}
