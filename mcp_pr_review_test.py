import random

def guess_the_number() -> None:
    """A short interactive game to guess a hidden number."""
    print("🤖 Welcome to the Guessing Game!")
    secret_number = random.randint(1, 20)
    attempts = 0

    while True:
        # 1. Safely handle user input that isn't a number
        try:
            user_guess = int(input("Guess a number between 1 and 20: "))
        except ValueError:
            print("❌ Invalid input! Please enter a whole number.")
            continue

        attempts += 1

        # 2. Check the guess using explicit conditional logic
        if user_guess < secret_number:
            print("📈 Too low! Try again.")
        elif user_guess > secret_number:
            print("📉 Too high! Try again.")
        else:
            print(f"🎉 Correct! You found it in {attempts} attempts.")
            break

if __name__ == "__main__":
    guess_the_number()
