import pygame
import random

class Ball:
    def __init__(self,screen,posx, posy, width = 50, height = 50):
        self.posx = posx
        self.posy = posy
        self.width  = width
        self.height = height
        self.screen = screen
        self.rect_dimension = pygame.Rect(self.posx,self.posy,self.width, self.height)
        self.color = self.generate_color()
       

    def generate_color(self):
        return (random.randint(10,255),random.randint(10,255), random.randint(10,255))
    
    def check_collision(self,rect):
        if self.rect_dimension.colliderect(rect):
            return True
        return False
    def update_screen(self):
        self.ball = pygame.draw.rect(self.screen,self.color,self.rect_dimension)
    def update_postion(self,x,y):
        self.rect_dimension.topleft = (x,y)
    def check_wall_collision(self,wall_top, wall_bottom):
        if self.rect_dimension[1] <= wall_top:
            return True
        elif self.rect_dimension[1] + self.height >= wall_bottom:
            return True
        return False
    
    def check_wall_x_collision(self,wall_left, wall_right):
        if self.rect_dimension[0] <= wall_left:
            return (True,1)
        elif self.rect_dimension[0] + self.width >= wall_right:
            return (True,2)
        return False
