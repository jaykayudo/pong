import pygame

class Paddle:
    def __init__(self, screen, posx, posy, color = (255,255,255),width = 30, height = 70):
        self.posx = posx
        self.posy = posy
        self.width  = width
        self.height = height
        self.screen = screen
        self.color = color
        self.rect_dimension = pygame.Rect(self.posx,self.posy,self.width, self.height)
        
    def update_screen(self):
        self.paddle = pygame.draw.rect(self.screen,self.color,self.rect_dimension)
        # self.screen.blit(self.paddle,self.rect_dimension)
    def update_position(self,x,y):
        self.rect_dimension.topleft = (x,y)
        
    def check_wall_collision(self,wall_top, wall_bottom):
        
        if self.rect_dimension[1] <= wall_top:
            self.update_position(self.rect_dimension[0], self.rect_dimension[1] + 5)
            return True
        
        elif self.rect_dimension[1] + self.height >= wall_bottom:
            self.update_position(self.rect_dimension[0], self.rect_dimension[1] - 5)
            return True
        return False
        