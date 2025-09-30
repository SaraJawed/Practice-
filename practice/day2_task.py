print("First 20 Fibonacci numbers:")

a = 0   # first number
b = 1   # second number

for i in range(20):   # loop runs 20 times
    print(a, end=" ")   # print current number
    next_num = a + b    # calculate next number
    a = b               # shift a to the next
    b = next_num        # shift b to the next
