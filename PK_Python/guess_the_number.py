import random

def play_again():
    while True:
        user_choice = input("Do you want to play again? Type 'yes' or 'no': ").lower()
        if user_choice == 'yes':
            number_game()
            break
        elif user_choice == 'no':
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please type 'yes' or 'no'.")

def number_game():
    attempts = 0
    guess_number = random.randint(1, 100)
    print("Guess the number between 1 and 100. Type 'q' to quit.")

    while True:
        user_input = input("Enter your guess: ")

        # Handle quitting the game
        if user_input.lower() == 'q':
            print(f"The correct number was {guess_number}.")
            break

        try:
            user_input = int(user_input)

            if user_input == guess_number:
                print(f"Congratulations! You guessed the number {guess_number} correctly in {attempts + 1} attempts.")
                play_again()
                break
            elif user_input > guess_number:
                print("Too high! Guess again.")
            else:
                print("Too low! Guess again.")
            
            attempts += 1

            # Provide a nearby hint after 5 attempts
            if attempts == 5:
                hint_low = max(1, guess_number - 10)  
                hint_high = min(100, guess_number + 10)  
                print(f"Your attempts have reached 5. Here's a hint: The number is between {hint_low} and {hint_high}.")

            # End the game after 10 attempts
            if attempts == 10:
                print("You've reached the maximum attempts! Game over.")
                print(f"The correct number was {guess_number}.")
                play_again()
                break
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

# Start the game
number_game()
