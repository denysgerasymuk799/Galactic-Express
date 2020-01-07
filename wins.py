import pygame
pygame.init()


class Button():
    def __init__(self,
                 x=0, y=0,
                 plain_img=pygame.Surface((20,20)),
                 over_img=pygame.Surface((20, 20)),
                 supersurf=None,
                 absolute_x=0, absolute_y=0):

        self.plain_surface = plain_img
        self.over_surface = over_img

        self.image = plain_img

        width = plain_img.get_width()
        height = plain_img.get_height()
       
        self.rect = pygame.Rect((x, y, width, height))

        self.supersurf = supersurf

        self.center = (x+width//2, y+height//2)

        self.min_x = absolute_x + x
        self.max_x = absolute_x + x + width
        self.min_y = absolute_y + y
        self.max_y = absolute_y + y + height
        
    def check_pressed(self):
        m_x, m_y = pygame.mouse.get_pos()
        if self.min_x < m_x < self.max_x:
            if self.min_y < m_y < self.max_y:
                return True, pygame.mouse.get_pressed()[0]
        return False, False
        
    def draw(self):
        self.supersurf.blit(self.image, self.rect)

    def update(self):
        pressed = self.work()
        self.draw()
        return pressed
        
    def work(self):
        over, pressed = self.check_pressed()
        if over:
            self.set_image(self.over_surface)
            if pressed:
                return True
        else:
            self.set_image(self.plain_surface)
        return False

    def set_image(self, image):
        self.image = image
        #self.rect = image.get_rect()
        #self.rect.center = self.center

