print("STONE-PAPER-SCISSOR")
print("Rules: Stone beats Scissor ,Scissor beats Paper, Paper beats Stone")
list = ["stone","paper","scissor"]
user_score = 0
computer_score = 0
while True:
 us = input("Enter your choice from the list: ")
 import random
 co = random.choice(list)
 print("Computer choice is:",co)
 print(us,"x",co)
 if us == "stone" and co == "scissor" or us== "paper" and co=="stone" or us=="scissor" and co=="paper":
    print("User win")
    user_score += 1
    print(user_score)
 elif co == "stone" and us == "scissor" or co == "paper" and us =="stone" or co =="scissor" and us =="paper":
    print("Computer win")
    computer_score += 1
    print(computer_score)
 elif us==co:
    print("It's draw, play again")
