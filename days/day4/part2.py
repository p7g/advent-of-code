import re
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
            if len(pp["byr"]) != 4 or not (1920 <= int(pp["byr"]) <= 2002):
                continue
            if len(pp["iyr"]) != 4 or not (2010 <= int(pp["iyr"]) <= 2020):
                continue
            if len(pp["eyr"]) != 4 or not (2020 <= int(pp["eyr"]) <= 2030):
                continue
            if match := re.fullmatch(r"(\d+)cm", pp["hgt"]):
                if not (150 <= int(match[1]) <= 193):
                    continue
            elif match := re.fullmatch(r"(\d+)in", pp["hgt"]):
                if not (59 <= int(match[1]) <= 76):
                    continue
            else:
                continue
            if not re.fullmatch(r"#[0-9a-f]{6}", pp["hcl"]):
                continue
            if pp["ecl"] not in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"):
                continue
            if not re.fullmatch(r"\d{9}", pp["pid"]):
                continue
            n += 1

    print(n)
