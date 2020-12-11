from lib.input import fetch_int_lines

if __name__ == "__main__":
    data = fetch_int_lines()
    data.sort()
    data.append(data[-1] + 3)
    data.insert(0, 0)

    npaths = [None, None, 1, 3, 6, 12]
    streak = 0
    n = 1
    for i in range(1, len(data)):
        if data[i] - data[i - 1] == 3:
            if streak > 1:
                n += n * npaths[streak]
            streak = 0
        else:
            streak += 1

    print(n)
