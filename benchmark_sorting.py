from random import randint
import time
import sys

sys.setrecursionlimit(3550)


def benchmark(func):
    def wrapper(*args):
        start_time = time.time()
        res = func(*args)
        end_time = time.time()
        print("time is: ", end_time - start_time)
        return res
    return wrapper


@benchmark
def sort_bubble(numbers):
    for i in range(len(numbers)):
        for j in range(len(numbers)-1):
            if numbers[j] > numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers


def sort_recursion(numbers):
    global new_nums
    if len(numbers) == 1:
        new_nums.append(numbers[0])
        return new_nums
    else:
        for i in range(len(numbers)-1):
            if numbers[i] < numbers[i+1]:
                numbers[i], numbers[i+1] = numbers[i+1], numbers[i]
        new_nums.append(numbers[-1])
    return sort_recursion(numbers[:-1])


n = 3500
nums = []
new_nums = []
for _ in range(n):
    nums.append(randint(1, 10000))

start = time.time()
sort_recursion(nums)
end = time.time()
print("time is: ", end - start)
sort_bubble(nums)
