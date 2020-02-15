import time
import random

def countingSort(arr, exp1):
    n = len(arr)
    output = [0] * (n)
    count = [0] * (10)

    for i in range(0, n):
        index = (arr[i] // exp1)
        count[(index) % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = (arr[i] // exp1)
        output[count[(index) % 10] - 1] = arr[i]
        count[(index) % 10] -= 1
        i -= 1

    for i in range(0, len(arr)):
        arr[i] = output[i]


def radixSort(arr):
    max1 = max(arr)
    exp = 1
    while max1 / exp > 0:
        countingSort(arr, exp)
        exp *= 10


def partition(array, start, end):
    pivot = array[start]
    low = start + 1
    high = end

    while True:
        while low <= high and array[high] >= pivot:
            high = high - 1
        while low <= high and array[low] <= pivot:
            low = low + 1
        if low <= high:
            array[low], array[high] = array[high], array[low]
        else:
            break

    array[start], array[high] = array[high], array[start]

    return high


def quick_sort(array, start=0, end=None):
    if end is None:
        end = len(array) - 1

    if start >= end:
        return

    p = partition(array, start, end)
    quick_sort(array, start, p-1)
    quick_sort(array, p+1, end)


def divide_sort(arr):
    if len(arr) <= 1:
        return arr
    if len(arr) == 2:
        return arr if arr[0] < arr[1] else arr[::-1]

    original = []
    for i in arr:
        original.append(i)

    _sorted = []

    while any(i is not None for i in arr):
        _ = min([i for i in arr if i is not None])

        for j in range(len(arr)):
            arr[j] = arr[j] // (_ + 2) if arr[j] is not None else None
        z = [j for j in range(len(arr)) if arr[j] == 0]
        for j in z:
            arr[j] = None

        _sorted += divide_sort([original[j] for j in z])

    return _sorted


def elapsed():
    arr = list(range(90, 100))
    random.shuffle(arr)
    y = arr
    start = time.time()
    quick_sort(arr)
    end = time.time()
    print(end - start)
    arr = y
    start = time.time()
    radixSort(arr)
    end = time.time()
    print(end - start)
    arr = y
    start = time.time()
    divide_sort(arr)
    end = time.time()
    print(end - start)


elapsed()
