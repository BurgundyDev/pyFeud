import time
import pygame
import json
import threading

class Team:
    points = 0
    mistakes = 0
    
RedTeam = Team()
BlueTeam = Team()

class GameState:
    current_id = 0
    current_question = ""
    in_second_loop = False
    reveal_all = False
    reveal_right = False
    reveal_left = False
    timer_started = False
    in_final_question = False
    correct_answers = 0
    current_team = RedTeam
    
game = GameState()

with open("questions.json", "r") as read_file:
    data = json.load(read_file)

def gameLoop():
    for question in data:
        if question["question_type"] == "basic":
            print("Detected basic question.")
            game.current_id = question["question_id"]
            game.current_question = question["question"]
            print(game.current_id)
            print(game.current_question)
            
            starting = input("Who starts? ")
            if(starting == "Red"):
                game.current_team = RedTeam
            elif(starting == "Blue"):
                game.current_team = BlueTeam
            
            while(game.in_second_loop == False and game.correct_answers < 5):
                answer = int(input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. "))
                if(answer == 0):
                    game.current_team.mistakes += 1
                    print("The current team has " + str(game.current_team.mistakes) + " mistakes")
                    if(game.current_team.mistakes == 3):
                        print("Proceeding to other team.")
                        game.in_second_loop = True
                else:
                    game.current_team.points += (question["answers"][answer-1]["points"] * question["multiplier"])
                    print("The current team has " + str(game.current_team.points) + " points")
                    game.correct_answers += 1
            
            # Second game loop, triggers when the first team get 
            if(game.in_second_loop == True):
                if(game.current_team == RedTeam):
                    game.current_team = BlueTeam
                elif(game.current_team == BlueTeam):
                    game.current_team = RedTeam
                while(game.current_team.mistakes < 1 and game.correct_answers < 5):
                    answer = int(input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. "))
                    if(answer == 0):
                        game.current_team.mistakes += 1
                        print("The current team has " + str(game.current_team.mistakes) + " mistakes")
                    else:
                        game.current_team.points += (question["answers"][answer-1]["points"] * question["multiplier"])
                        print("The current team has " + str(game.current_team.points) + " points")
                        game.correct_answers += 1
            game.reveal_all = True
            
            input("Proceed? ")
            # Cleanup
            RedTeam.mistakes = 0
            BlueTeam.mistakes = 0
            game.in_second_loop = 0
            game.correct_answers = 0
            game.reveal_all = False
            
        if question["question_type"] == "final":
            print("Detected final question.")
            game.current_id = question["question_id"]
            game.current_question = question["question"]
            game.in_final_question = True
            print(game.current_id)
            print(game.current_question)
            
            starting = input("Who starts? ")
            if(starting == "Red"):
                game.current_team = RedTeam
            elif(starting == "Blue"):
                game.current_team = BlueTeam
            
            starttime = time.time()
            currtime = time.time()
            iterator = 0
            while(currtime - starttime < 15 and iterator < len(question["questions"])):
                print(question["questions"][iterator])
                answer = int(input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. "))
                if(answer != 0):
                    game.current_team.points += (question["answers"][iterator][answer-1]["points"])
                    print("The current team has " + str(game.current_team.points) + " points")
                iterator += 1
                currtime = time.time()
            
            input("Continue? ")
            
            if(game.current_team == RedTeam):
                game.current_team = BlueTeam
            elif(game.current_team == BlueTeam):
                game.current_team = RedTeam
            
            starttime = time.time()
            currtime = time.time()
            iterator = 0
            while(currtime - starttime < 15 and iterator < len(question["questions"])):
                print(question["questions"][iterator])
                answer = int(input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. "))
                if(answer != 0):
                    game.current_team.points += (question["answers"][iterator][answer-1]["points"])
                    print("The current team has " + str(game.current_team.points) + " points")
                iterator += 1
                currtime = time.time()
gameLoop()