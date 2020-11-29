#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

/* Parallelized brute-force attempt in C. Still way too slow.
 *
 * My matrix multiplication code is probably pretty naive, which surely would
 * not help things.
 */

#define LEN(X) (sizeof((X)) / sizeof((X)[0]))
#define BUF_LEN (650 * 10000)
int8_t buf[BUF_LEN];
int8_t buf2[BUF_LEN];

static int8_t *do_phases(size_t n);
static void make_pattern(int8_t *pattern, size_t i);

int main(int argc, char **argv)
{
	if (argc < 2)
		return 1;

	char *fname = argv[1];
	FILE *f = fopen(fname, "r");
	char c;
	int i = 0;
	size_t offset = 0;
	while ((c = fgetc(f)) != EOF) {
		if (i < 8) {
			offset *= 10;
			offset += c - '0';
		}
		buf[i++] = c - '0';
		assert(i < BUF_LEN && "overflow");
	}
	fclose(f);

	int8_t *result = do_phases(100);
	for (size_t j = offset; j < 8; j++)
		printf("%d", result[j]);
	putchar('\n');

	return 0;
}

static void make_pattern(int8_t *pattern, size_t i)
{
	static int8_t base[] = {0, 1, 0, -1};
	int first = 1;
	size_t idx = 0;

	for (size_t j = 0; idx < (size_t) BUF_LEN / (i + 1); j += 1) {
		for (size_t k = i; k < i + 1; k += 1) {
			if (first) {
				first = 0;
				continue;
			}
			pattern[idx++] = base[j % LEN(base)];
		}
	}
}

static inline int8_t myabs(int8_t n)
{
	if (n < 0)
		return -n;
	return n;
}

static inline int8_t ones(int64_t n)
{
	return myabs(n) % 10;
}

struct phases_arg {
	pthread_t tid;
	int8_t *input, *out;
	size_t i, j;
};

static void *phases(void *arg)
{
	static __thread int8_t pattern[BUF_LEN];

	struct phases_arg *data = (struct phases_arg *) arg;
	size_t i = data->i,
	       j = data->j;
	int8_t *input = data->input,
	       *out = data->out;

	for (; i < j; i += 1) {
		make_pattern(pattern, i);
		int64_t sum = 0;
		for (size_t j = 0; j < BUF_LEN; j += 1)
			sum += input[j] * pattern[j];
		out[i] = ones(sum);
	}

	pthread_exit(NULL);
}

#define NTHREADS 12

static void do_phase(int8_t *input, int8_t *out)
{
	struct phases_arg threads[NTHREADS];

	size_t rem = BUF_LEN % NTHREADS;
	size_t start = 0;
	for (size_t i = 0; i < NTHREADS; i += 1) {
		threads[i].input = input;
		threads[i].out = out;
		threads[i].i = start;
		threads[i].j = start + (size_t) BUF_LEN / NTHREADS;
		if (i == NTHREADS - 1)
			threads[i].j += rem;
		pthread_create(&threads[i].tid, NULL, phases, &threads[i]);
		start += (size_t) BUF_LEN / NTHREADS;
	}

	for (size_t i = 0; i < NTHREADS; i += 1)
		pthread_join(threads[i].tid, NULL);
}

static int8_t *do_phases(size_t n)
{
	for (size_t i = 0; i < n; i += 1) {
		printf("phase %zu\n", i);
		if (i % 2 == 0)
			do_phase(buf, buf2);
		else
			do_phase(buf2, buf);
	}
	return n % 2 == 0 ? buf : buf2;
}
