import math

a_start, a_end, b_start, b_end, c_start, c_end = [int(input()) for _ in range(6)]

for a in range(a_start, a_end + 1):
    for b in range(b_start, b_end + 1):
        for c in range(c_start, c_end + 1):
            D = (b ** 2) - (4 * a * c)
            try:
                if D < 0:
                    continue
                elif D == 0:
                    x = round(-b / (2 * a), 2)
                    print(f'{a} {b} {c} Yes {x}')
                else:
                    x1 = round((-b + math.sqrt(D)) / (2 * a), 2)
                    x2 = round((-b - math.sqrt(D)) / (2 * a), 2)
                    print(f'{a} {b} {c} Yes {x1} {x2}')
            except ZeroDivisionError:
                continue
