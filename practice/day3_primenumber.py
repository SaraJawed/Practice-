def is_prime(n):
    if n <= 1:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False

    return True
try:
    num = int(input("Enter a number to check if it's prime: "))
    
    if is_prime(num):
        print(f"{num} is a prime number.")
    else:
        print(f"{num} is not a prime number.")

except ValueError:
    print("Invalid input! Please enter a valid integer.")
