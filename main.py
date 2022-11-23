import sys
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
    prize_pool = 0
    
game = GameState()

class WindowProperties:
    windowSize = width, height = 1920, 1080
    windowWidth = windowSize[0]
    windowHeight = windowSize[1]
    
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(self.windowSize)

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
                        game.current_team.points -= game.prize_pool
                        game.in_second_loop = True
                else:
                    game.prize_pool += (question["answers"][answer-1]["points"] * question["multiplier"])
                    game.current_team.points += (question["answers"][answer-1]["points"] * question["multiplier"])
                    print("The current team has " + str(game.current_team.points) + " points")
                    game.correct_answers += 1
            
            # Second game loop, triggers when the first team get 
            if(game.in_second_loop == True):
                if(game.current_team == RedTeam):
                    game.current_team = BlueTeam
                elif(game.current_team == BlueTeam):
                    game.current_team = RedTeam
                game.current_team.points += game.prize_pool
                while(game.current_team.mistakes < 1 and game.correct_answers < 5):
                    answer = int(input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. "))
                    if(answer == 0):
                        game.current_team.mistakes += 1
                        print("The current team has " + str(game.current_team.mistakes) + " mistakes")
                        game.current_team.points -= game.prize_pool
                        if(game.current_team == RedTeam):
                            game.current_team = BlueTeam
                        elif(game.current_team == BlueTeam):
                            game.current_team = RedTeam
                        game.current_team.points += game.prize_pool
                    else:
                        game.prize_pool += (question["answers"][answer-1]["points"] * question["multiplier"])
                        game.current_team.points += (question["answers"][answer-1]["points"] * question["multiplier"])
                        print("The current team has " + str(game.current_team.points) + " points")
                        game.correct_answers += 1
            game.reveal_all = True
            
            input("Proceed? ")
            # Cleanup
            RedTeam.mistakes = 0
            BlueTeam.mistakes = 0
            game.in_second_loop = False
            game.correct_answers = 0
            game.reveal_all = False
            game.in_final_question = False
            game.prize_pool = 0
            
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
                
threading.Thread(target=gameLoop, daemon=True).start()

pygame.init()
pygame.font.init()

Window = WindowProperties()

default_font = pygame.font.Font("dot_matrix/DOTMATRI.TTF", 48)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
                
    Window.screen.fill((0, 0, 0))
    
    if(game.in_final_question == False):
        text_question = default_font.render(game.current_question, True, (255, 255, 0))
        Window.screen.blit(text_question, ((Window.windowWidth/2 - text_question.get_rect().width/2), 100), text_question.get_rect())
        
        text_Red_points = default_font.render(str(RedTeam.points), True, (255, 255, 0))
        text_Blue_points = default_font.render(str(BlueTeam.points), True, (255, 255, 0))
        Window.screen.blit(text_Red_points, (20, 900), text_Red_points.get_rect())
        Window.screen.blit(text_Blue_points, (Window.windowWidth - 20 - text_Blue_points.get_rect().width, 900), text_Blue_points.get_rect())
        
        text_sum = default_font.render(str(game.prize_pool), True, (255, 255, 0))
        text_sum_title = default_font.render("TOTAL", True, (255, 255, 0))
        Window.screen.blit(text_sum_title, (Window.windowWidth/2 + text_sum_title.get_rect().width, 720), text_sum_title.get_rect())
        Window.screen.blit(text_sum, (Window.windowWidth/2 + text_sum_title.get_rect().width * 2 + text_sum.get_rect().width, 720), text_sum.get_rect())
    
    pygame.display.flip()