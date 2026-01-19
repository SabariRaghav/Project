import random

number_to_guess=random.randint(1,100)
while True:
    try:
        guess=int(input("Enter a number from 1 to 100:"))
        if guess < number_to_guess:
            print("Too low")
        elif guess > number_to_guess:
            print("Too high")
        else:
            print("You guessed Correctly")
            break
    except ValueError:
        print("Enter a valid number")
