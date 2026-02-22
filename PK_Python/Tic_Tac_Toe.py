def sum(a, b, c):
    return a + b + c

def Tic_Tac_Toe(xState, oState):
    print("Welcome to Tic Tac Toe: ")
    
    zero = 'X' if xState[0] else ('0' if oState[0] else 0)
    one = 'X' if xState[1] else ('0' if oState[1] else 1)
    two = 'X' if xState[2] else ('0' if oState[2] else 2)
    three = 'X' if xState[3] else ('0' if oState[3] else 3)
    four = 'X' if xState[4] else ('0' if oState[4] else 4)
    five = 'X' if xState[5] else ('0' if oState[5] else 5)
    six = 'X' if xState[6] else ('0' if oState[6] else 6)
    seven = 'X' if xState[7] else ('0' if oState[7] else 7)
    eight = 'X' if xState[8] else ('0' if oState[8] else 8)

    print(f" {zero} | {one} | {two} ")
    print(f"---|---|---")
    print(f" {three} | {four} | {five} ")
    print(f"---|---|---")
    print(f" {six} | {seven} | {eight} ")

def checkwin(xState, oState):
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6], [0, 3, 6], [1, 4, 7], [2, 5, 8]]
    for win in wins:
        if sum(xState[win[0]], xState[win[1]], xState[win[2]]) == 3:
            print("X won the match!")
            return 1
        if sum(oState[win[0]], oState[win[1]], oState[win[2]]) == 3:
            print("O won the match!")
            return 0
    return -1

def play_again():
    while True:
        user_input = input("Do you want to play again? (Yes/No): ").strip().lower()
        if user_input == "yes":
            main()  # Restart the game
        elif user_input == "no":
            print("Thanks for playing!")
            break
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")

def main():
    # Initial game state
    xState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    oState = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    turn = 1  # 1 for X, 0 for O

    # Game loop
    while True:
        Tic_Tac_Toe(xState, oState)
        
        if turn == 1:
            print("X's Chance")
            value = int(input("Please enter a value: "))
            if xState[value] or oState[value]:
                print("Invalid move. Try again.")
                continue
            xState[value] = 1
        else:
            print("O's Chance")
            value = int(input("Please enter a value: "))
            if xState[value] or oState[value]:
                print("Invalid move. Try again.")
                continue
            oState[value] = 1
        
        # Check if there is a winner
        cwin = checkwin(xState, oState)
        if cwin != -1:
            print("Match Over!")
            play_again()
            break
        
        # Check if it's a tie
        if all(xState[i] or oState[i] for i in range(9)):
            print("It's a tie!")
            play_again()
            break
        
        turn = 1 - turn  # Switch turns

# Start the game
main()
