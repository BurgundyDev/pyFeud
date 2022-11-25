import sys
import time
import pygame
import json
import threading

class Team:
    points = 0
    mistakes = 0
    def __init__(self) -> None:
        self.name = input("Team name?: ")
    
RedTeam = Team()
BlueTeam = Team()

class GameState:
    current_id = 0
    current_question = None
    current_question_text = ""
    in_second_loop = False
    reveal_right = False
    reveal_left = False
    timer_started = False
    in_final_question = False
    correct_answers = 0
    current_team = RedTeam
    prize_pool = 0
    answers_revealed = [False, False, False, False, False, False, False, False, False, False, False, False, False]
    final_answers_one = [0, 0, 0, 0, 0]
    final_answers_two = [0, 0, 0, 0, 0]
    final_started_one = False
    final_started_two = False
    final_complete_one = False
    final_complete_two = False
    final_hidden_one = False
    current_question_answers = 0
    start_time = time.time()
    current_time = time.time()
    over = False
    
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
            game.current_question = question
            game.current_question_text = question["question"]
            print(game.current_id)
            print(game.current_question_text)
            game.current_question_answers = len(question["answers"])
            print(game.current_question_answers)
            
            for x in range(game.current_question_answers):
                game.answers_revealed[x] = False
            
            starting = input("Who starts? ")
            if(starting == "Red" or starting == "red" or starting == RedTeam.name):
                game.current_team = RedTeam
            elif(starting == "Blue" or starting == "blue" or starting == BlueTeam.name):
                game.current_team = BlueTeam
            
            while(game.in_second_loop == False and game.correct_answers < game.current_question_answers):
                answer = int(input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. "))
                if(answer == 0):
                    game.current_team.mistakes += 1
                    print("The current team has " + str(game.current_team.mistakes) + " mistakes")
                    if(game.current_team.mistakes == 3):
                        print("Proceeding to other team.")
                        game.current_team.points -= game.prize_pool
                        game.in_second_loop = True
                elif(answer <= game.current_question_answers):
                    game.prize_pool += (question["answers"][answer-1]["points"] * question["multiplier"])
                    game.current_team.points += (question["answers"][answer-1]["points"] * question["multiplier"])
                    print("The current team has " + str(game.current_team.points) + " points")
                    game.answers_revealed[answer-1] = True
                    game.correct_answers += 1
                    print(game.answers_revealed)
            
            # Second game loop, triggers when the first team get 
            if(game.in_second_loop == True):
                if(game.current_team == RedTeam):
                    game.current_team = BlueTeam
                elif(game.current_team == BlueTeam):
                    game.current_team = RedTeam
                game.current_team.points += game.prize_pool
                unanswered = True
                while(unanswered):
                    answer = int(input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. "))
                    if(answer == 0):
                        game.current_team.mistakes += 1
                        print("The current team has " + str(game.current_team.mistakes) + " mistakes")
                        game.current_team.points -= game.prize_pool
                        unanswered = False
                    elif(answer <= game.current_question_answers):
                        game.prize_pool += (question["answers"][answer-1]["points"] * question["multiplier"])
                        game.current_team.points += (question["answers"][answer-1]["points"] * question["multiplier"])
                        print("The current team has " + str(game.current_team.points) + " points")
                        game.answers_revealed[answer-1] = True
                        game.correct_answers += 1
                        print(game.answers_revealed)
                        unanswered = False
                        
            for x in range(game.current_question_answers):
                if(game.answers_revealed[x] == False):
                    input("Show next answer? ")
                    game.answers_revealed[x] = True
            
            input("Proceed? ")
            # Cleanup
            RedTeam.mistakes = 0
            BlueTeam.mistakes = 0
            game.in_second_loop = False
            game.correct_answers = 0
            game.in_final_question = False
            game.prize_pool = 0
            game.answers_revealed = [False, False, False, False, False, False, False, False, False, False, False, False, False]
            
        if question["question_type"] == "final":
            print("Detected final question.")
            game.current_id = question["question_id"]
            game.current_question = question
            game.current_question_text = question["question"]
            game.in_final_question = True
            print(game.current_id)
            print(game.current_question_text)
            
            if(RedTeam.points > BlueTeam.points):
                game.current_team = RedTeam
            elif(RedTeam.points < BlueTeam.points):
                game.current_team = BlueTeam
                
            input("Start finale? ")
            
            game.start_time = time.time()
            game.current_time = time.time()
            game.final_started_one = True
            iterator = 0
            completed = []
            while(game.current_time - game.start_time < 15 and len(completed) != len(question["questions"])):
                if(iterator not in completed):
                    print(question["questions"][iterator])
                    answer = input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. ")
                    print(answer)
                    if(answer == ''):
                        print("Question passed")
                    else:
                        completed.append(iterator)
                        answer = int(answer)
                        game.final_answers_one[iterator] = answer
                        if(answer != 0):
                            game.current_team.points += (question["answers"][iterator][answer-1]["points"])
                            game.prize_pool += (question["answers"][iterator][answer-1]["points"])
                            print("The current team has " + str(game.current_team.points) + " points")
                iterator += 1
                if(iterator == len(question["questions"])):
                    iterator = 0
                game.current_time = time.time()
            input("Show answers? ")
            game.final_complete_one = True
            input("Hide answers? ")
            game.final_hidden_one = True
            input("Continue? ")
            
            game.start_time = time.time()
            game.current_time = time.time()
            game.final_started_two = True
            iterator = 0
            completed = []
            while(game.current_time - game.start_time < 20 and len(completed) != len(question["questions"])):
                if(iterator not in completed):
                    print(question["questions"][iterator])
                    answer = input("Which answer has been input? Type 0 if there was no answer or the answer was incorrect/repeated. ")
                    print(answer)
                    if(answer == ''):
                        print("Question passed")
                    else:
                        completed.append(iterator)
                        answer = int(answer)
                        game.final_answers_two[iterator] = answer
                        if(answer != 0):
                            game.current_team.points += (question["answers"][iterator][answer-1]["points"])
                            game.prize_pool += (question["answers"][iterator][answer-1]["points"])
                            print("The current team has " + str(game.current_team.points) + " points")
                iterator += 1
                if(iterator == len(question["questions"])):
                    iterator = 0
                game.current_time = time.time()
            
            input("Show answers? ")
            game.final_complete_two = True
            game.final_hidden_one = False
            input("Continue to end screen? ")
                
            if(game.prize_pool < 100):
                print(f"The {game.current_team.name} lost the final round!")
                game.current_team.point -= game.prize_pool
                print(game.current_team.points)
                game.over = True
            else:
                print(f"The {game.current_team.name} won the final round!")
                print(game.current_team.points)
                game.over = True
                

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
    
    if(game.over == True):
        end_name = default_font.render(game.current_team.name, True, (255, 255, 0))
        Window.screen.blit(end_name, ((Window.windowWidth/2 - end_name.get_rect().width/2), 100), end_name.get_rect())
        end_font = pygame.font.Font("dot_matrix/DOTMATRI.TTF", 455)
        end_score = end_font.render(str(game.current_team.points), True, (255, 255, 0))
        Window.screen.blit(end_score, ((Window.windowWidth/2 - end_score.get_rect().width/2), 400), end_score.get_rect())
    elif(game.in_final_question == False):
        text_question = default_font.render(game.current_question_text, True, (255, 255, 0))
        Window.screen.blit(text_question, ((Window.windowWidth/2 - text_question.get_rect().width/2), 100), text_question.get_rect())
        
        text_Red_points = default_font.render(str(RedTeam.points), True, (255, 255, 0))
        text_Red_name = default_font.render(RedTeam.name, True, (255, 255, 0))
        text_Blue_points = default_font.render(str(BlueTeam.points), True, (255, 255, 0))
        text_Blue_name = default_font.render(BlueTeam.name, True, (255, 255, 0))
        Window.screen.blit(text_Red_points, (20, 900), text_Red_points.get_rect())
        Window.screen.blit(text_Blue_points, (Window.windowWidth - 20 - text_Blue_points.get_rect().width, 900), text_Blue_points.get_rect())
        Window.screen.blit(text_Red_name, (20, 840), text_Red_name.get_rect())
        Window.screen.blit(text_Blue_name, (Window.windowWidth - 20 - text_Blue_name.get_rect().width, 840), text_Blue_name.get_rect())
        
        text_sum = default_font.render(str(game.prize_pool), True, (255, 255, 0))
        text_sum_title = default_font.render("TOTAL", True, (255, 255, 0))
        Window.screen.blit(text_sum_title, (Window.windowWidth/2 + text_sum_title.get_rect().width, 860), text_sum_title.get_rect())
        Window.screen.blit(text_sum, (Window.windowWidth/2 + text_sum_title.get_rect().width * 2 + text_sum.get_rect().width, 860), text_sum.get_rect())
        
        for x in range(RedTeam.mistakes):
            mistake_font = pygame.font.Font("dot_matrix/DOTMATRI.TTF", 212)
            mistake = mistake_font.render("X", True, (255, 255, 0))
            Window.screen.blit(mistake, (20, 100 + x * 200), mistake.get_rect())
        
        for x in range(BlueTeam.mistakes):
            mistake_font = pygame.font.Font("dot_matrix/DOTMATRI.TTF", 212)
            mistake = mistake_font.render("X", True, (255, 255, 0))
            Window.screen.blit(mistake, (Window.windowWidth - 20 - mistake.get_rect().width, 100 + x * 200), mistake.get_rect())
        
        for x in range(game.current_question_answers):
            answer_number = default_font.render(str(x+1), True, (255, 255, 0))
            Window.screen.blit(answer_number, (400, 300 + x*60), answer_number.get_rect())
            if(game.answers_revealed[x] == True):
                answer =  default_font.render(game.current_question["answers"][x]["answer"], True, (255, 255, 0))
                Window.screen.blit(answer, (500, 300 + x*60), answer.get_rect())
            else:
                answer =  default_font.render("- - - - -", True, (255, 255, 0))
                Window.screen.blit(answer, (500, 300 + x*60), answer.get_rect())
                
            if(game.answers_revealed[x] == True):
                points =  default_font.render(str(game.current_question["answers"][x]["points"]), True, (255, 255, 0))
                Window.screen.blit(points, (Window.windowWidth/2 + text_sum_title.get_rect().width * 2 + text_sum.get_rect().width, 300 + x*60), points.get_rect())
            else:
                points =  default_font.render("- -", True, (255, 255, 0))
                Window.screen.blit(points, (Window.windowWidth/2 + text_sum_title.get_rect().width * 2 + text_sum.get_rect().width, 300 + x*60), points.get_rect())
    elif(game.in_final_question == True):
        text_question = default_font.render("FINALE", True, (255, 255, 0))
        Window.screen.blit(text_question, ((Window.windowWidth/2 - text_question.get_rect().width/2), 100), text_question.get_rect())
        
        if(game.final_started_one and game.final_complete_one == False):
            timer = default_font.render(str(15 - (game.current_time - game.start_time)), True, (255, 255, 0))
            Window.screen.blit(timer, (200, 800), timer.get_rect())
            
        if(game.final_started_two and game.final_complete_two == False):
            timer = default_font.render(str(15 - (game.current_time - game.start_time)), True, (255, 255, 0))
            Window.screen.blit(timer, (200, 800), timer.get_rect())
        
        if(game.final_complete_two):
            text_sum = default_font.render(str(game.prize_pool), True, (255, 255, 0))
            text_sum_title = default_font.render("TOTAL", True, (255, 255, 0))
            Window.screen.blit(text_sum_title, (Window.windowWidth/2 + text_sum_title.get_rect().width, 860), text_sum_title.get_rect())
            Window.screen.blit(text_sum, (Window.windowWidth/2 + text_sum_title.get_rect().width * 2 + text_sum.get_rect().width, 860), text_sum.get_rect())
        else:
            text_sum = default_font.render("- -", True, (255, 255, 0))
            text_sum_title = default_font.render("TOTAL", True, (255, 255, 0))
            Window.screen.blit(text_sum_title, (Window.windowWidth/2 + text_sum_title.get_rect().width, 860), text_sum_title.get_rect())
            Window.screen.blit(text_sum, (Window.windowWidth/2 + text_sum_title.get_rect().width * 2 + text_sum.get_rect().width, 860), text_sum.get_rect())
        
        for x in range(5):
            if(game.final_complete_one and game.final_hidden_one == False):
                if(game.final_answers_one[x] == 0):
                    answer =  default_font.render("N/A", True, (255, 255, 0))
                    Window.screen.blit(answer, (Window.windowWidth/2 - 600, 300 + x*60), answer.get_rect())
                    points = default_font.render("- -", True, (255, 255, 0))
                    Window.screen.blit(points, (Window.windowWidth/2 - 120, 300 + x*60), points.get_rect())
                else:
                    answer =  default_font.render(game.current_question["answers"][x][game.final_answers_one[x]-1]["answer"], True, (255, 255, 0))
                    Window.screen.blit(answer, (Window.windowWidth/2 - 600, 300 + x*60), answer.get_rect())
                    points = default_font.render(str(game.current_question["answers"][x][game.final_answers_one[x]-1]["points"]), True, (255, 255, 0))
                    Window.screen.blit(points, (Window.windowWidth/2 - 120, 300 + x*60), points.get_rect())
            else:
                answer =  default_font.render("- - - - -", True, (255, 255, 0))
                Window.screen.blit(answer, (Window.windowWidth/2 - 600, 300 + x*60), answer.get_rect())
                points = default_font.render("- -", True, (255, 255, 0))
                Window.screen.blit(points, (Window.windowWidth/2 - 120, 300 + x*60), points.get_rect())
        
        for x in range(5):
            if(game.final_complete_two):
                if(game.final_answers_two[x] == 0):
                    answer =  default_font.render("N/A", True, (255, 255, 0))
                    Window.screen.blit(answer, (Window.windowWidth/2 + 600 - answer.get_rect().width, 300 + x*60), answer.get_rect())
                    points = default_font.render("- -", True, (255, 255, 0))
                    Window.screen.blit(points, (Window.windowWidth/2 + 120 - points.get_rect().width, 300 + x*60), points.get_rect())
                else:
                    answer =  default_font.render(game.current_question["answers"][x][game.final_answers_two[x]-1]["answer"], True, (255, 255, 0))
                    Window.screen.blit(answer, (Window.windowWidth/2 + 600 - answer.get_rect().width, 300 + x*60), answer.get_rect())
                    points = default_font.render(str(game.current_question["answers"][x][game.final_answers_two[x]-1]["points"]), True, (255, 255, 0))
                    Window.screen.blit(points, (Window.windowWidth/2 + 120 - points.get_rect().width, 300 + x*60), points.get_rect())
            else:
                answer =  default_font.render("- - - - -", True, (255, 255, 0))
                Window.screen.blit(answer, (Window.windowWidth/2 + 600 - answer.get_rect().width, 300 + x*60), answer.get_rect())
                points = default_font.render("- -", True, (255, 255, 0))
                Window.screen.blit(points, (Window.windowWidth/2 + 120 - points.get_rect().width, 300 + x*60), points.get_rect())
    pygame.display.flip()