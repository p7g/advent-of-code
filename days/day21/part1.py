from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines(21)

    foods = []
    for line in data:
        ingredients, allergens = line.rstrip(")").split(" (")
        foods.append(
            (ingredients.split(" "), allergens[len("contains ") :].split(", "))
        )

    possible = {}

    for allergen in set(a for _, as_ in foods for a in as_):
        possible[allergen] = set.intersection(
            *[set(ingrs) for ingrs, as_ in foods if allergen in as_]
        )

    while not all(len(ins) == 1 for ins in possible.values()):
        for a, ins in possible.items():
            if len(ins) == 1:
                ing = list(ins)[0]
                for a2 in possible.keys():
                    if a2 == a:
                        continue
                    try:
                        possible[a2].remove(ing)
                    except KeyError:
                        pass

    have_allergen = set(a for as_ in possible.values() for a in as_)
    all_ingredients = set(i for ins, _ in foods for i in ins)
    without_allergen = all_ingredients - have_allergen

    n = 0
    for ins, _ in foods:
        n += sum(i in without_allergen for i in ins)

    print(n)
