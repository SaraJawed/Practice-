print("Welcome to Guess the Number!")
print("Player 1: Choose a secret number (don’t show Player 2).")
secret_number = int(input("Enter the secret number: "))

print("\n" * 10) 
print("Player 2: Try to guess the number!")

while True:
    guess = int(input("Enter your guess: "))

    if guess == secret_number:
        print("Congratulations! You guessed it right.")
        break

    elif guess < secret_number:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")
