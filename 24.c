#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

int alu(int w[14])
{
	long long x, y, z;

	z = w[0] + 6;
	z = z * 26 + w[1] + 12;
	z = z * 26 + w[2] + 5;
	z = z * 26 + w[3] + 10;
	x = (w[3] - 6) != w[4];
	y = 25 * x + 1;
	z = (z / 26 * y) + (w[4] + 7) * x;
	z = z * 26 + w[5];
	z = z * 26 + w[6] + 4;
	x = w[6] != w[7];
	y = 25 * x + 1;
	z = (z / 26 * y) + (w[7] + 12) * x;
	z = z * 26 + w[8] + 14;
	x = (w[8] + 7) != w[9];
	y = 25 * x + 1;
	z = (z / 26 * y) + (w[9] + 13) * x;
	x = ((z % 26) - 8) != w[10];
	y = 25 * x + 1;
	z = (z / 26 * y) + (w[10] + 10) * x;
	x = ((z % 26) - 4) != w[11];
	y = 25 * x + 1;
	z = (z / 26 * y) + (w[11] + 11) * x;
	x = ((z % 26) - 15) != w[12];
	y = 25 * x + 1;
	z = (z / 26 * y) + (w[12] + 9) * x;
	x = ((z % 26) - 8) != w[13];
	y = 25 * x + 1;
	z = (z / 26 * y) + (w[13] + 9) * x;

	if (!z) {
		for (int i = 0; i < 14; i++) {
			assert(w[i] < 10);
			assert(w[i] > 0);
			printf("%d", w[i]);
		}
		putchar('\n');
	}
	return !z;
}

int main()
{
	int w[14];

#define RUN(NEXT) ANY(0) ANY(1) ANY(2) RANGE(3, 7, 10) { DERIVED(4, 3, -6) ANY(5) ANY(6) { DERIVED(7, 6,) RANGE(8, 1, 3) { DERIVED(9, 8, +7) ANY(10) ANY(11) ANY(12) ANY(13) if (alu(w)) goto NEXT; } } }
#define DERIVED(N, FROM, DIFF) w[N] = w[FROM] DIFF;

#define ANY(N) for (w[N] = 9; w[N] > 0; w[N]--)
#define RANGE(N, MIN, STOP) for (w[N] = STOP - 1; w[N] >= MIN; w[N]--)
	RUN(next)
#undef ANY
#undef RANGE

next:
#define ANY(N) for (w[N] = 1; w[N] < 10; w[N]++)
#define RANGE(N, MIN, STOP) for (w[N] = MIN; w[N] < STOP; w[N]++)
	RUN(done)

done:
	return 0;
}
