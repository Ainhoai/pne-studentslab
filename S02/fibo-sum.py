def fibosum(n):
    n1, n2, count, sum = 0, 1, 0, 0
    while count < n:
        nth = n1 + n2
        n1, n2 = n2, nth
        sum += n1
        count += 1
    print(f"The sum of the first {n} terms of the Fionacci sequence: ", sum)
fibosum(5)
fibosum(10)



