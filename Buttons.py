import pygame

# Button constants
btn_w, btn_h = 160, 60
btn_color = 'grey'
btn_border_clr = 'black'
btn_border_w = 2
pos_x , pos_y = 320, 240
btn_font_color = 'black'

class BasicButton:
    def __init__(self, x:int = pos_x, y:int = pos_y, button_width:int = btn_w, button_height:int  = btn_h, button_color: str | pygame.Color = btn_color, border: bool = False, border_color: str | pygame.Color = btn_border_clr, border_width:int = btn_border_w, button_font = None, button_text: str = 'None', font_color: str | pygame.Color = btn_font_color):
        self.button_clicked = False
        self.image = pygame.Surface((button_width, button_height))
        self.image.fill(button_color)
        self.rect = self.image.get_rect(center = (x, y))
        if border: 
            pygame.draw.rect(self.image, border_color, self.image.get_rect(), border_width )
        self.button_text_image = button_font.render(button_text, True, font_color)
        self.image.blit(self.button_text_image, self.button_text_image.get_rect(center = (button_width/2, button_height/2)))
        self.clicked = False
    
    def draw(self, screen: pygame.Surface) -> bool:
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_just_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True   
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

class SingleImageButton:
    def __init__(self, xpos: float | int, ypos: float | int, image: str, scale: float | int = 1):
        self.image = pygame.image.load(image).convert()
        if scale != 1:
            self.image = pygame.transform.scale_by(self.image, scale)
        self.rect = self.image.get_rect(center = (xpos, ypos))
        self.clicked = False
    
    def draw(self, screen: pygame.Surface) -> bool:
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_just_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True   
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        #draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action