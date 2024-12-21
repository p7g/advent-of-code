#include <assert.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

#define W 141

static inline int grid_idx(int x, int y) {
	// +1 because of the newlines
	return y * (W + 1) + x;
}

static inline int idx(int x, int y) {
	return y * W + x;
}

struct pt {
	int x, y;
};

static inline int ptidx(struct pt pt) {
	return idx(pt.x, pt.y);
}

static void compute_shortest_path_lengths(char *grid, unsigned *dist, struct pt src);

int main(void) {
	FILE *f = fopen(".aoc-cache/2024-20.txt", "r");
	fseek(f, 0, SEEK_END);
	long sz = ftell(f);
	rewind(f);

	char *input = malloc(sz + 1);
	assert(sz == fread(input, sizeof input[0], sz, f));
	input[sz] = 0;
	fclose(f);

	struct pt start;
	struct pt end;

	for (int y = 0; y < W; y += 1) {
		for (int x = 0; x < W; x += 1) {
			if (input[grid_idx(x, y)] == 'S') {
				start = (struct pt){x, y};
			} else if (input[grid_idx(x, y)] == 'E') {
				end = (struct pt){x, y};
			}
		}
	}

	static unsigned dist_from_start[W * W] = {INT_MAX};
	static unsigned dist_from_end[W * W] = {INT_MAX};

	compute_shortest_path_lengths(input, dist_from_start, start);
	compute_shortest_path_lengths(input, dist_from_end, end);

	int base_time = dist_from_start[ptidx(end)];

	int s = 0;
	int s2 = 0;
	for (int y = 0; y < W; y += 1) {
		for (int x = 0; x < W; x += 1) {
			if (input[grid_idx(x, y)] == '#')
				continue;

			for (int y2 = 0; y2 < W; y2 += 1) {
				for (int x2 = 0; x2 < W; x2 += 1) {
					if (input[grid_idx(x2, y2)] == '#')
						continue;

					int d = abs(x2 - x) + abs(y2 - y);
					if (d > 20)
						continue;

					int total = dist_from_start[idx(x, y)]
						+ d
						+ dist_from_end[idx(x2, y2)];
					if (total >= base_time)
						continue;

					int saved_time = base_time - total;
					if (saved_time >= 100) {
						s += d == 2;
						s2 += 1;
					}
				}
			}
		}
	}

	printf("%d\n", s);
	printf("%d\n", s2);

	return 0;
}

struct heapentry {
	int priority;
	struct pt pt;
};

struct heap {
	int size;
	struct heapentry entries[W * W];
};

static void heapinit(struct heap *heap);
static void heappush(struct heap *heap, struct pt pt, int priority);
static int heapempty(struct heap const *heap);
static struct pt heappop(struct heap *heap);
static void heapdecpriority(struct heap *heap, struct pt pt, int priority);

static void compute_shortest_path_lengths(char *grid, unsigned *dist, struct pt src) {
	static struct pt prev[W * W];
	static struct heap Q;

	heapinit(&Q);
	dist[ptidx(src)] = 0;
	heappush(&Q, src, 0);

	for (int y = 0; y < W; y += 1) {
		for (int x = 0; x < W; x += 1) {
			if (x == src.x && y == src.y)
				continue;
			prev[idx(x, y)] = (struct pt) {-1, -1};
			dist[idx(x, y)] = INT_MAX;
			heappush(&Q, (struct pt){x, y}, INT_MAX);
		}
	}

	while (!heapempty(&Q)) {
		struct pt u = heappop(&Q);

#define FOR_NBR(x, y) do { \
	if (x < 0 || x >= W || y < 0 || y >= W) break; \
	if (grid[grid_idx(x, y)] == '#') break; \
	int alt = dist[ptidx(u)] + 1; \
	if (alt < dist[idx(x, y)]) { \
		prev[idx(x, y)] = u; \
		dist[idx(x, y)] = alt; \
		heapdecpriority(&Q, (struct pt) {x, y}, alt); \
	} \
} while(0)

		FOR_NBR(u.x - 1, u.y);
		FOR_NBR(u.x, u.y - 1);
		FOR_NBR(u.x + 1, u.y);
		FOR_NBR(u.x, u.y + 1);

#undef FOR_NBR
	}
}

static void heapinit(struct heap *heap) {
	heap->size = 0;
}

static void heap_siftdown(struct heap *heap, int startpos, int pos);
static void heap_siftup(struct heap *heap, int pos);

// ported from cpython heapq
static void heappush(struct heap *heap, struct pt pt, int priority) {
	heap->entries[heap->size++] = (struct heapentry) {
		.priority = priority,
		.pt = pt,
	};
	heap_siftdown(heap, 0, heap->size - 1);
}

static int heapempty(struct heap const *heap) {
	return heap->size == 0;
}

static struct pt heappop(struct heap *heap) {
	assert(heap->size > 0);
	struct heapentry entry = heap->entries[--heap->size];
	if (!heap->size)
		return entry.pt;
	struct pt returnitem = heap->entries[0].pt;
	heap->entries[0] = entry;
	heap_siftup(heap, 0);
	return returnitem;
}

static void heapdecpriority(struct heap *heap, struct pt pt, int priority) {
	int i = 0;
	for (; i < heap->size; i += 1) {
		struct pt *pt2 = &heap->entries[i].pt;
		if (pt2->x == pt.x && pt2->y == pt.y)
			break;
	}
	if (i == heap->size)
		return;

	heap->entries[i].priority = priority;
	heap_siftdown(heap, 0, i);
}

static void heap_siftdown(struct heap *heap, int startpos, int pos) {
	struct heapentry newitem = heap->entries[pos];
	while (pos > startpos) {
		int parentpos = (pos - 1) >> 1;
		struct heapentry parent = heap->entries[parentpos];
		if (newitem.priority < parent.priority) {
			heap->entries[pos] = parent;
			pos = parentpos;
			continue;
		}
		break;
	}
	heap->entries[pos] = newitem;
}

static void heap_siftup(struct heap *heap, int pos) {
	int endpos = heap->size;
	int startpos = pos;
	struct heapentry newitem = heap->entries[pos];
	int childpos = 2 * pos + 1;
	while (childpos < endpos) {
		int rightpos = childpos + 1;
		if (rightpos < endpos
				&& heap->entries[childpos].priority >= heap->entries[rightpos].priority) {
			childpos = rightpos;
		}
		heap->entries[pos] = heap->entries[childpos];
		pos = childpos;
		childpos = 2 * pos + 1;
	}
	heap->entries[pos] = newitem;
	heap_siftdown(heap, startpos, pos);
}
