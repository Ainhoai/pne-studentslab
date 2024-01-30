def fibon(n):
    n1, n2, count = 0, 1, 0
    while count < n:
        nth = n1 + n2
        n1, n2 = n2, nth
        count += 1
    print(f"{n}th Fibonacci term: ", n1)

fibon(5)
fibon(10)
fibon(15)

