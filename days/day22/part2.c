#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

struct qnode {
	struct qnode *next;
	int value;
};

struct q {
	struct qnode *head, *tail;
	int size;
};

static struct q *q_new(void);
static void q_free(struct q *q);
static struct q *q_copy(const struct q *q, int until);
static void q_put(struct q *q, int value);
static int q_take(struct q *q);
static unsigned q_hash(struct q *q);

struct set {
	int size, used;
	unsigned *buckets;
};

static struct set *set_new(void);
static void set_free(struct set *set);
static void set_add(struct set *set, unsigned hash);
static int set_has(struct set *set, unsigned hash);

static struct q *make_deck(char *p);

static struct q *game(struct q *p1, struct q *p2)
{
	struct set *past_states;
	struct q *w, *w2, *p12, *p22;
	unsigned snapshot;
	int a, b, c;

	past_states = set_new();
	for (;;) {
		snapshot = 31 * q_hash(p1) + q_hash(p2);
		if (set_has(past_states, snapshot)) {
			w = p1;
			break;
		}
		set_add(past_states, snapshot);

		a = q_take(p1);
		b = q_take(p2);

		if (p1->size >= a && p2->size >= b) {
			p12 = q_copy(p1, a);
			p22 = q_copy(p2, b);
			w2 = game(p12, p22);
			if (w2 == p12) {
				w = p1;
				c = a;
			} else {
				w = p2;
				c = b;
			}
			q_free(p12);
			q_free(p22);
		} else if (a > b) {
			w = p1;
			c = a;
		} else {
			w = p2;
			c = b;
		}

		q_put(w, c);
		q_put(w, b == c ? a : b);

		if (!p1->size) {
			w = p2;
			break;
		} else if (!p2->size) {
			w = p1;
			break;
		}
	}

	set_free(past_states);
	return w;
}

int main(void)
{
	FILE *f;
	char *buf, *s1, *s2;
	int buflen, c, i, score;
	struct q *p1, *p2, *winner;

	f = fopen("input.txt", "rb");
	if (!f) {
		perror(NULL);
		return 1;
	}
	buf = malloc(sizeof(char) * (buflen = 4096));
	i = 0;

	while (EOF != (c = fgetc(f))) {
		buf[i++] = c;
		if (i == buflen)
			buf = realloc(buf, sizeof(char) * (buflen *= 2));
	}
	buf = realloc(buf, sizeof(char) * (buflen = i + 1));
	buf[i] = 0;

	s1 = s2 = NULL;
	for (i = 0; i < buflen - 1; i += 1) {
		if (buf[i] != '\n' || buf[i + 1] != '\n')
			continue;
		buf[i] = 0;
		s1 = buf;
		s2 = buf + i + 2;
		break;
	}

	if (!s1 || !s2)
		abort();

	p1 = make_deck(s1);
	p2 = make_deck(s2);
	free(buf);

	winner = game(p1, p2);
	if (winner == p1)
		q_free(p2);
	else
		q_free(p1);

	score = 0;
	for (i = winner->size; i > 0; i -= 1)
		score += q_take(winner) * i;
	q_free(winner);

	printf("%d\n", score);
	return 0;
}

static struct q *q_new(void)
{
	struct q *q;

	q = malloc(sizeof(struct q));
	q->head = q->tail = NULL;
	q->size = 0;

	return q;
}

static void q_free(struct q *q)
{
	struct qnode *a, *b;

	a = q->head;
	while (a) {
		b = a;
		a = a->next;
		free(b);
	}

	free(q);
}

static struct q *q_copy(const struct q *q, int until)
{
	struct q *new;
	struct qnode *p;
	int i;

	new = q_new();
	for (i = 0, p = q->head; i < until && p; i += 1, p = p->next)
		q_put(new, p->value);

	return new;
}

static void q_put(struct q *q, int value)
{
	struct qnode *new;

	new = malloc(sizeof(struct qnode));
	new->value = value;
	new->next = NULL;
	if (q->tail)
		q->tail->next = new;
	if (!q->head)
		q->head = new;
	q->tail = new;
	q->size += 1;
}

static int q_take(struct q *q)
{
	struct qnode *tmp;
	int val;

	assert(q->head);
	tmp = q->head;
	q->head = tmp->next;
	if (q->tail == tmp)
		q->tail = NULL;
	val = tmp->value;
	free(tmp);
	q->size -= 1;

	return val;
}

static unsigned q_hash(struct q *q)
{
	struct qnode *n;
	unsigned hash;

	hash = 1;
	n = q->head;
	while (n) {
		hash = 31 * hash + n->value;
		n = n->next;
	}

	return hash;
}

static struct set *set_new(void)
{
	struct set *set;

	set = malloc(sizeof(struct set));
	set->size = 4096;
	set->used = 0;
	set->buckets = calloc(set->size, sizeof(unsigned));

	return set;
}

static void set_free(struct set *set)
{
	free(set->buckets);
	free(set);
}

static void set_grow(struct set *set)
{
	int old_size, i;
	unsigned *old_buckets, hash;

	old_size = set->size;
	old_buckets = set->buckets;
	set->used = 0;
	set->size *= 2;
	set->buckets = calloc(set->size, sizeof(unsigned));

	for (i = 0; i < old_size; i += 1) {
		if ((hash = old_buckets[i]))
			set_add(set, hash);
	}

	free(old_buckets);
}

static void set_add(struct set *set, unsigned hash)
{
	int i;
	unsigned h;

	if (set->used / set->size > 0.3)
		set_grow(set);

	h = hash % set->size;
	for (i = 0; i < set->size - h; i += 1) {
		if (set->buckets[h + i]) {
			if (set->buckets[h + i] == hash)
				break;
			continue;
		}
		set->buckets[h + i] = hash;
		set->used += 1;
		break;
	}
}

static int set_has(struct set *set, unsigned hash)
{
	int i;
	unsigned h;

	h = hash % set->size;
	for (i = 0; i < set->size - h; i += 1) {
		if (set->buckets[h + i] == hash)
			return 1;
		if (!set->buckets[h + i])
			break;
	}
	return 0;
}

static struct q *make_deck(char *p)
{
	struct q *q;

	q = q_new();
	while (*++p != '\n');
	while (*p++ == '\n' && *p)
		q_put(q, (int) strtol(p, &p, 10));

	return q;
}
