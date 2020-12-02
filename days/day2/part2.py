from lib.input import fetch_lines

if __name__ == "__main__":
    data = fetch_lines(2)

    num = 0
    for line in data:
        policy, pw = map(str.strip, line.split(":"))
        times, c = policy.split(" ")
        min, max = map(int, times.split("-"))
        max -= 1
        min -= 1
        if (pw[min] == c) ^ (pw[max] == c):
            num += 1

    print(num)
