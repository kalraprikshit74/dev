import random

def play():
    choices = ["rock", "paper", "scissors"]
    Your_score = 0
    Tommy_score = 0
    while True:
        user_choice = input("Enter your choice (rock, paper, scissors): ").lower()
        if user_choice not in choices:
            print("Invalid choice. Try again.")
            continue

        Tommy_choice = random.choice(choices)
        print(f"You choose: {user_choice}")
        print(f"The Tommy choose: {Tommy_choice}")

        if user_choice == Tommy_choice:
            print("It's a tie!")
        elif (user_choice == "rock" and Tommy_choice == "scissors") or \
             (user_choice == "scissors" and Tommy_choice == "paper") or \
             (user_choice == "paper" and Tommy_choice == "rock"):
            print("You win!")
            Your_score+=1
        else:
            print("You lose!")
            Tommy_score+=1
        print(f"You: {Your_score}")
        print(f"Tommy: {Tommy_score}")
        if Tommy_score==5:
            break
        elif Your_score==5:
            break
    print("Congratulation You Won this!")
    while True:  # Loop to keep asking if the user wants to play again
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            break
        else:
            play()
            break
play()
print("Thanks for playing!")


    
    
