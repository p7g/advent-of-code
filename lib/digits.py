def digits(n):
    digs = []
    while n:
        digs.append(n % 10)
        n //= 10
    digs.reverse()
    return digs


def undigits(digits):
    n, *digits = digits
    for digit in digits:
        n *= 10
        n += digit
    return n
