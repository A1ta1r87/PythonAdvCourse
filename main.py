from random import randint
import time
import sys


sys.setrecursionlimit(3100)


def benchmark(func):
    def wrapper(*args):
        start = time.time()
        res = func(*args)
        end = time.time()
        print("time is: ", end - start)
        return res
    return wrapper


@benchmark
def sort_bubble(nums):
    flag = True
    while flag:
        flag = False
        for i in range(len(nums) - 1):
            if nums[i] > nums[i + 1]:
                nums[i], nums[i + 1] = nums[i + 1], nums[i]
                flag = True
    print(nums)
    return nums


def sort_recursion(nums):
    global new_nums
    if len(nums) <= 1:
        new_nums.append(nums[0])
        return new_nums
    else:
        min_ind = nums.index(min(nums))
        nums[0], nums[min_ind] = nums[min_ind], nums[0]
        new_nums.append(nums[0])
    return sort_recursion(nums[1:])


n = 3000
nums = []
new_nums = []
for _ in range(n):
    nums.append(randint(1, 1000))
print(nums)
start = time.time()
print(sort_recursion(nums))
end = time.time()
print("time is: ", end - start)
sort_bubble(nums)


