from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines()

    pps = [{}]
    for line in data:
        if line == "":
            pps.append({})
        for attr in line.split(" "):
            if not attr:
                continue
            k, v = attr.split(":")
            pps[-1][k] = v

    n = 0
    for pp in pps:
        for k in ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"):
            if k not in pp:
                break
        else:
            n += 1

    print(n)
