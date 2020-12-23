#include <assert.h>
#include <stdio.h>

#define NNODES 1000001

struct node {
	struct node *next;
	int label;
};

static struct node nodes[NNODES];

int main(void)
{
	const char data[] = "643719258";
	int bottom_lookups[10];

	for (int i = 1; i <= sizeof(data); i += 1)
		nodes[i].label = data[i - 1] - '0';

	for (int i = 1; i < NNODES; i += 1) {
		nodes[i].next = i == NNODES - 1 ? &nodes[1] : &nodes[i + 1];
		if (i > 9)
			nodes[i].label = i;
		else
			bottom_lookups[nodes[i].label] = i;
	}

	assert(nodes[NNODES - 1].label == 1000000);
	assert(bottom_lookups[6] == 1);

	struct node *current = &nodes[1];

	for (int i = 0; i < 10000000; i += 1) {
		struct node *a = current->next,
					*b = current->next->next,
					*c = current->next->next->next;
		current->next = c->next;

		int dest = current->label;
		do {
			dest -= 1;
			if (dest < 1)
				dest = 1000000;
		} while (dest == a->label || dest == b->label || dest == c->label);

		struct node *dest_node = dest < 10
			? &nodes[bottom_lookups[dest]]
			: &nodes[dest];
		struct node *end_node = dest_node->next;
		dest_node->next = a;
		a->next = b;
		b->next = c;
		c->next = end_node;

		current = current->next;
	}

	struct node *one = &nodes[bottom_lookups[1]];
	printf("%ld\n", (long) one->next->label * (long) one->next->next->label);

	return 0;
}
