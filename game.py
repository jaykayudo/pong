from ball import Ball
from paddle import Paddle
import pygame
import random


pygame.init()

class Game:
    def __init__(self):
        self.WINDOW_WIDTH = 1280
        self.WINDOW_HEIGHT = 720
        self.small_font = pygame.font.SysFont("Consolas",30)
        self.large_font = pygame.font.SysFont("Nunito",70)
        self.score_font = pygame.font.SysFont("Comic Sans MS",140)
        self.game_font = pygame.font.SysFont("Poppins",100)
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH,self.WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.paddle_height = 80
        self.paddle_width = 20
        self.ball_width = 20
        self.ball_height = 20
        self.start_state()

        self.player_one = Paddle(self.screen,self.player_one_position[0],
                                 self.player_one_position[1],width=self.paddle_width,
                                 height = self.paddle_height)
        self.player_two = Paddle(self.screen,self.player_two_position[0],
                                 self.player_two_position[1],width=self.paddle_width,
                                 height = self.paddle_height)
        self.ball = Ball(self.screen, self.ball_x,self.ball_y, self.ball_width,self.ball_height)

        self.sounds = {
            'paddle_hit': pygame.mixer.Sound("sounds/paddle_hit.wav"),
            'score': pygame.mixer.Sound("sounds/score.wav"),
            'wall_hit': pygame.mixer.Sound("sounds/wall_hit.wav"),
        }
        self.DT = 30 # delta time a.k.a frames per second (FPS)
        self.clock = pygame.time.Clock()
        self.player_one_score = 0
        self.player_two_score = 0
        self.new_game =True
        self.game_ended = False
        self.lastWinner = None
        
    def start_state(self):
        self.serving_player = random.choice([1,2])
        self.game_play = True
        self.player_one_position = [20,random.randint(0,self.WINDOW_HEIGHT - self.paddle_height)]
        self.player_two_position = [self.WINDOW_WIDTH - self.paddle_width - 20,
                                            random.randint(0,self.WINDOW_HEIGHT - self.paddle_height)]
        self.ball_x = (self.WINDOW_WIDTH/2)-(self.ball_width/2)
        self.ball_y = (self.WINDOW_HEIGHT/2)-(self.ball_height/2)
        self.set_ball_speed_x(self.serving_player)
        self.ball_speed_y = random.choice([5,-5])
        self.paddle_speed = 10
        self.ball_served = False
    def restart_state(self):
        self.player_one_score = 0
        self.player_two_score = 0
        self.game_ended = False
        self.start_state()

    def set_ball_speed_x(self, initial_server):
        if initial_server == 1:
            self.ball_speed_x = 5
        else:
            self.ball_speed_x = -5
        return self.ball_speed_x
        
    def display_background(self):
        self.background = pygame.draw.rect(self.screen,(0,0,0),[0,0, self.WINDOW_WIDTH,self.WINDOW_HEIGHT])
        # pygame.display.update(self.background)
    def display_score(self):
        color = self.ball.generate_color()
        player_one_score_display = self.score_font.render(str(self.player_one_score),1,color)
        player_two_score_display = self.score_font.render(str(self.player_two_score),1,color)
        player_one_score_display_rect = player_one_score_display.get_rect()
        player_two_score_display_rect = player_two_score_display.get_rect()
        player_one_score_display_rect.topright = ((self.WINDOW_WIDTH/2) - (self.WINDOW_WIDTH/2)/2, (self.WINDOW_HEIGHT/2)-100)
        player_two_score_display_rect.topleft = ((self.WINDOW_WIDTH/2) + (self.WINDOW_WIDTH/2)/2, (self.WINDOW_HEIGHT/2)-100)

        self.screen.blit(player_one_score_display,player_one_score_display_rect)
        self.screen.blit(player_two_score_display,player_two_score_display_rect)

    def check_winner(self):
        if self.player_one_score == 10:
            return True, 1
        elif self.player_two_score == 10:
            return True, 2
        else:
            return False

    def display_winner(self):
        color = (255,255,255)
        winner_display = self.game_font.render(f'Player {self.lastWinner} wins',1,color)
        game_restart_display = self.small_font.render(f'Press Enter to restart game',1,color)
        winner_display_rect =  winner_display.get_rect()
        game_restart_display_rect =  game_restart_display.get_rect()
        winner_display_rect.center = self.WINDOW_WIDTH/2, 100
        game_restart_display_rect.center = self.WINDOW_WIDTH/2, 150
        self.screen.blit(winner_display,winner_display_rect)
        self.screen.blit(game_restart_display,game_restart_display_rect)
    def display_serving_player(self):
        color = (255,255,255)
        serving_display = self.large_font.render(f'Player {self.serving_player} to serve',1,color)
        serving_display_rect =  serving_display.get_rect()
        serving_display_rect.center = self.WINDOW_WIDTH/2, 100
        self.screen.blit(serving_display,serving_display_rect)
    
    def display_welcome(self):
        color = self.ball.generate_color()
        welcome_display = self.game_font.render(f"Welcome to Pong",1, color)
        side_text_display = self.small_font.render(f"Press Enter to Start Game",1, color)
        welcome_display_rect =  welcome_display.get_rect()
        side_text_display_rect =  side_text_display.get_rect()
        welcome_display_rect.center = self.WINDOW_WIDTH/2, 100
        side_text_display_rect.center = self.WINDOW_WIDTH/2, 200
        self.screen.blit(welcome_display,welcome_display_rect)
        self.screen.blit(side_text_display,side_text_display_rect)

    def game(self):
        move_y_player_one = 0
        move_y_player_two = 0
        while self.game_play:
            self.display_background()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_play =False
                    pygame.quit()
                    quit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key  == pygame.K_RETURN:
                        if self.game_ended:
                            self.game_ended = False
                            self.restart_state()
                        elif not self.ball_served:
                            self.ball_served = True
                        if self.new_game:
                            self.new_game = False
                    if event.key == pygame.K_ESCAPE:
                        self.game_play = False
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_UP:
                        move_y_player_two -= self.paddle_speed
                    if event.key == pygame.K_DOWN:
                        move_y_player_two += self.paddle_speed
                    if event.key == pygame.K_w:
                        move_y_player_one -= self.paddle_speed
                    if event.key == pygame.K_s:
                        move_y_player_one  += self.paddle_speed
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN or  event.key == pygame.K_UP:
                        move_y_player_two = 0
                    if event.key == pygame.K_w or  event.key == pygame.K_s:
                        move_y_player_one= 0

                        
            if  self.player_one.check_wall_collision(0, self.WINDOW_HEIGHT):
                move_y_player_one = 0
            if  self.player_two.check_wall_collision(0, self.WINDOW_HEIGHT):
                move_y_player_two = 0
            
            self.ball.update_screen()
            self.player_one.update_position(self.player_one.rect_dimension[0], self.player_one.rect_dimension[1] + move_y_player_one)
            self.player_one.update_screen()
            self.player_two.update_position(self.player_two.rect_dimension[0], self.player_two.rect_dimension[1] + move_y_player_two)
            self.player_two.update_screen()

            if self.new_game:
                self.display_welcome()
            elif self.ball_served:
                if self.ball.check_wall_collision(0, self.WINDOW_HEIGHT):
                    self.ball_speed_y *= -1
                    self.sounds['wall_hit'].play()    
                self.ball.update_postion(self.ball.rect_dimension[0] + self.ball_speed_x, 
                                             self.ball.rect_dimension[1] + self.ball_speed_y)
            else:
                self.display_score()
                if not self.game_ended:
                    self.display_serving_player()
                
            if self.ball.check_collision(self.player_one.rect_dimension) or self.ball.check_collision(self.player_two.rect_dimension):
                self.ball_speed_x *= -1
                self.sounds['paddle_hit'].play()
                self.ball_speed_x *= 1.1
                self.ball_speed_y *= 1.1
                self.paddle_speed *= 1.1
            
            x_wall_collision = self.ball.check_wall_x_collision(0, self.WINDOW_WIDTH)
            if x_wall_collision:
                if x_wall_collision[1] == 1:
                    self.start_state()
                    self.set_ball_speed_x(1)
                    self.serving_player = 1
                    self.player_two_score += 1
                else:
                    self.start_state()
                    self.set_ball_speed_x(2)
                    self.serving_player = 2
                    self.player_one_score += 1
                self.sounds["score"].play()
                self.ball.update_postion(self.ball_x,self.ball_y)
            winner_check = self.check_winner()
            if winner_check:
                self.lastWinner = winner_check[1]
                self.game_ended = True
            if self.game_ended:
                self.display_winner()
            

            

            
            pygame.display.flip()
            self.clock.tick(self.DT)




game = Game()
game.game()
            



        