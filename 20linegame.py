# a simple game
def game():
    print("Welcome to the game! You are in a dark cave")
    choice = input("Do you want to go left or right? ")
    if choice == "left":
        print("You are in a room with a table and a chair")
        choice = input("Do you want to sit down or stand up? ")
        if choice == "sit down":
            print("You are sitting down")
            print("You need to find the magic stone")
        else:
            print("You are standing up")
            print("You need to find the magic stone")
    else:
        print("You are in a room with a table and a chair")
        choice = input("Do you want to sit down or stand up? ")
        if choice == "sit down":
            print("You are sitting down")
            print("You need to find the magic stone")
        else:
            print("You are standing up")
            print("You did it! You are a wizard!")
    print("Game over")
    
game()








