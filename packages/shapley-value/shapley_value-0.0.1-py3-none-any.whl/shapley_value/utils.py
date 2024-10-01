
def combinations(items, r):
    if r == 0:
        yield []
    else:
        for i in range(len(items)):
            for combination in combinations(items[i+1:], r-1):
                yield [items[i]] + combination

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
