import random
from playsound import playsound

def play_sound(correct=True):
    # if correct:
    #     playsound('correct.mp3')
    # else:
    #     playsound('wrong.mp3')
    pass

def start_game():
    print("Welcome to Prikshit's game!")
    print("This game was specially made for Vansh.")
    print("This game was made on 22 November 2024 by Prikshit.")
    # This is just a fun game for kids
    # We are just warming up

    # name = input("Enter your name: ")
    print("Hello, Vansh!")
    # Taking an integer input
    # age = int(input("Enter your age: "))
    # print("You are " + str(age) + " years old.")

    print("Choose a level of difficulty:")
    print("1. Easy (Single digit x Single digit)")
    print("2. Medium (Two digit x Single digit)")
    print("3. Hard (Two digit x Two digit)")

    level = input("Select the level (1 for Easy, 2 for Medium, 3 for Hard): ")

    if level == "1":
        play_game(1)  # Easy level
    elif level == "2":
        play_game(2)  # Medium level
    elif level == "3":
        play_game(3)  # Hard level
    else:
        print("Invalid choice. Please try again.")
        start_game()

def play_game(level):
    score = 0
    question_count = 0
    lives = 5

    while lives > 0:
        if level == 1:
            # Easy: Single-digit x Single-digit
            num1 = random.randint(1, 9)
            num2 = random.randint(1, 9)
        elif level == 2:
            # Medium: Two-digit x Single-digit
            num1 = random.randint(10, 99)
            num2 = random.randint(1, 9)
        elif level == 3:
            # Hard: Two-digit x Two-digit
            num1 = random.randint(10, 99)
            num2 = random.randint(10, 99)

        correct_answer = num1 * num2

        print(f"Question {question_count + 1}: What is {num1} x {num2}? (Lives left: {lives})")
        answer = input("Your answer (or type 'quit' to stop): ")

        if answer.lower() == 'quit':
            break  # Exit the loop to stop the game

        if answer.isdigit() and int(answer) == correct_answer:
            print("Correct!")
            play_sound(correct=True)  # Play correct answer sound
            score += 1
        else:
            print(f"Oops! The correct answer was {correct_answer}.")
            play_sound(correct=False)  # Play incorrect answer sound
            lives -= 1  # Deduct a life for an incorrect answer

        question_count += 1

    print(f"\nGame over! Your final score: {score} out of {question_count}.")
    play_again()

def play_again():
    choice = input("Do you want to play again? (yes/no): ").lower()
    if choice == "yes":
        start_game()
    elif choice == "no":
        print("Thanks for playing!")
    else:
        print("Invalid choice. Exiting the game.")

# Start the game
start_game()
