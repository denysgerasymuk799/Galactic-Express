import pygame
from generate_numbers import get_even, get_lucky, get_ulam
pygame.font.init()
pygame.mixer.init()
pygame.init()


from random import randint, shuffle
import wins


s_channel = pygame.mixer.Channel(1)
m_channel = pygame.mixer.Channel(0)
zip_sound = pygame.mixer.Sound('music/zip_stamp.wav')
wrong_sound = pygame.mixer.Sound('music/mistake.wav')
win_music = pygame.mixer.Sound('music/win_sound.ogg')
main_theme = pygame.mixer.Sound('music/main_theme.wav')
game_over_sound = pygame.mixer.Sound('music/game_over.ogg')


sound_on = True
music_on = True


pygame.display.set_caption('Galactic Express')



font = pygame.font.SysFont('bahnschrift', 28, bold=0)
#stamps = [pygame.image.load('e_icon.png'), pygame.image.load('l_icon.png'), pygame.image.load('u_icon.png'), pygame.image.load('other_icon.png')]
stamps = [pygame.image.load('boxes/e_i.png'),
          pygame.image.load('boxes/l_i.png'),
          pygame.image.load('boxes/u_i.png'),
          pygame.image.load('boxes/other_i.png')]


extra_box_settings = {
    'image': pygame.image.load('boxes\extra_box.png'),
    'w': 195,
    'h': 150,
    't_coords': (40, 94),
    'x_shift': 0,
    'stamp_coords': (105, 5),
}

regular_box_settings = {
    'image': pygame.image.load('boxes/regular_box.png'),
    'w': 241,
    'h': 193,
    't_coords': (40, 137),
    'stamp_coords': (140, 10),
}

d_box_settings = {
    'image': pygame.image.load('boxes/box.png'),
    'w': 241,
    'h': 193,
    't_coords': (45, 144),
    'stamp_coords': (110, 40),
}

u_box_settings = {
    'image': pygame.image.load('boxes/blue_box.png'),
    'w': 241,
    'h': 193,
    't_coords': (40, 140),
    'stamp_coords': (120, 40),
}

background_color = (20, 20, 20)
main_win_color = (0, 0, 0)
    

class Parcel(pygame.sprite.Sprite):
    def __init__(self, number=0, address_class=[0, 0, 0, 1], x=0, y=0, settings=regular_box_settings,
                 font=font, color=background_color):
        self.stamp_location = settings['stamp_coords']

        self.rect = pygame.rect.Rect(x, y, settings['w'], settings['h'])
        
        surface = pygame.surface.Surface((settings['w'], settings['h']))
        surface.fill(color)
        surface.blit(settings['image'], (0, 0))
        address = font.render('# ' + str(number), 0, (0, 0, 0))
        surface.blit(address, settings['t_coords'])
        self.image = surface

        self.true_address = address_class
        self.address = [0, 0, 0, 0]

        self.score = 0
        self.is_stamped = False

        pygame.sprite.Sprite.__init__(self)

    def draw(self, surface):
        surface.blit(self.image, (self.rect.topleft))
    
    def move(self, x=0, y=0):
        self.rect.left += x
        self.rect.top += y

    def stamp(self, stamp_type=0, stamps=stamps):
        
        if self.true_address[stamp_type] is 1 and self.address[stamp_type] is not 1:
            self.address[stamp_type] = 1

            self.score += 1
       
            self.image.blit(stamps[stamp_type], self.stamp_location)
            self.stamp_location = (self.stamp_location[0], self.stamp_location[1]+40)

            if sound_on:
                s_channel.play(zip_sound)
                
            if self.true_address == self.address:
                self.is_stamped = True

        else:
            self.score -= 1

            if sound_on:
                s_channel.play(wrong_sound)
                
                
def _get_parcels_types(n_of_parcels=0):
    """Generate information on parcels

    Params:
        n_of_parcels - number, to which generate special numbers

    Attributes:
        even (list): even numbers from 1 to n_of_parcels
        lucky (list): lucky numbers from 1 to n_of_parcels
        ulam  (list): ulam numbers from 1 to n_of_parcels

        parcels_types (list):

        list[i] = [n: number] + [int( n is even ),
                                 int( n is ulam ),
                                 int( n is lucky )

                                + [int(n is even or n is ulam or n is lucky)]

    Returns:
        parcels_types

    """
    
    even = get_even(n_of_parcels)
    lucky = get_lucky(n_of_parcels)
    ulam = get_ulam(n_of_parcels)

    parcels_types = [[i+1, 0, 0, 0] for i in range(n_of_parcels+1)]

    for i in even:
        parcels_types[i-1][1] = 1
    for i in lucky:
        parcels_types[i-1][2] = 1
    for i in ulam:
        if i < n_of_parcels-1:
            parcels_types[i-1][3] = 1
    parcels_types = [i + [1] if sum(i[1:]) is 0 else i + [0] for i in parcels_types]
    return parcels_types

parcels_settings = [extra_box_settings, regular_box_settings, u_box_settings, d_box_settings]


def _make_parcel_group(parcels_types, x=0, y=0, orientation='v', chaos=False, strad=20):
    """Make Parcel objects based on information on parcels

    Params:
        parcels_types (list): information on parcels
        x, y (int): position of group of parcels on screen
        orientation (str): 'v' - vertical or 'h' - horizontal
        chaos (bool): is group randomized (default - group is sorted 1 to number of parcels)
        
    Attributes:
        parcels (list): group of parcels
        parcels_settings (list): global variable, list of details on how parcels look on screen
        weight (int): how many points can be scored on the group
        strad (int): space between boxes

    Returns:
        parcels, weigth

    """
    
    parcels = []
    y = y + strad if orientation is 'v' else y
    x = x - strad if orientation is 'h' else x

    weight = 0

    if chaos:
        shuffle(parcels_types)

    if orientation is 'h':
        for i in range(len(parcels_types)):
            weight += sum(parcels_types[i][1:])
             
            box_settings = parcels_settings[randint(0, len(parcels_settings)-1)]
            
            x -= box_settings['w']
            parcels.append(Parcel(parcels_types[i][0], parcels_types[i][1:], x, y, box_settings))
            x -= strad
            
    elif orientation is 'v':
        for i in range(len(parcels_types)):
            weight += sum(parcels_types[i][1:])
            
            box_settings = parcels_settings[randint(0, len(parcels_settings)-1)]

            y += box_settings['h'] + strad
            parcels.append(Parcel(parcels_types[i][0], parcels_types[i][1:], x, y, box_settings))
            
    
    return parcels, weight


class ParcelGroup():
    def __init__(self, n_of_parcels=100, x=0, y=0,
                 orientation='v', chaos=False, strad=20):

        self.parcels, self.weigth = _make_parcel_group(_get_parcels_types(n_of_parcels),
                                              strad=20, x=x, y=y, orientation=orientation, chaos=chaos)
        self.strad = strad
    
        self.orientation = orientation

    def draw(self, surface):
        for p in self.parcels[:5]:
            p.draw(surface)

    def update(self, win, stamped=[]):
        if self.parcels[0].is_stamped:
            return True
        elif stamped is not []:
            for i in range(4):
                if 1 == stamped[i]:
                     self.parcels[0].stamp(i)
        return False

    def get_first_parcel(self):
        return self.parcels[0]
        

class ParcelWindow():
    def __init__(self, w=400, h=400, n_of_parcels=100, x=0, y=0,
                 orientation='v', w_x=0, w_y=0, color=(0, 0, 0), chaos=False, strad=20):

        y = 0 if orientation is 'v' else y
        x = w if orientation is 'h' else x

        self.parcels = ParcelGroup(n_of_parcels, x=x, y=y,
                                   orientation=orientation, chaos=chaos, strad=strad)
       
        self.surface = pygame.Surface((w, h))
        self.coords = (w_x, w_y)
        self.color = color
        
        self.orientation = orientation

        self.max_score = self.parcels.weigth
        self.score = 0

    def proceed(self, win):
        first_parcel = self.parcels.get_first_parcel()
        scored = first_parcel.score
        
        if self.orientation is 'v':
            dx, dy = 0, first_parcel.rect.top - first_parcel.rect.bottom - self.parcels.strad
            for i in range(-dy//20):
                self.draw(win)
                for p in self.parcels.parcels:
                    p.move(0, -20)
                dy += 20
                   
                pygame.display.update()
                pygame.time.delay(5)

        elif self.orientation is 'h':
            dx, dy = (first_parcel.rect.right - first_parcel.rect.left + self.parcels.strad), 0

            for p in self.parcels.parcels[5:]:
                p.move(dx, dy)
                
            for i in range(dx//30):
                self.draw(win)
                for p in self.parcels.parcels[:5]:
                    p.move(+30, 0)
                dx -= 30
                    
                pygame.display.update()
                pygame.time.delay(10)
                
        for p in self.parcels.parcels[:5]:
                p.move(dx, dy)
                
        self.parcels.parcels = self.parcels.parcels[1:]

        self.score += scored
                
    def handle_events(self, win):
        keys = pygame.key.get_pressed()
        pygame.event.pump()
        stamped = [keys[pygame.K_e], keys[pygame.K_l], keys[pygame.K_u], keys[pygame.K_x]]
        
        is_stamped = self.parcels.update(win, stamped)
        if is_stamped:
            scored = self.proceed(win)
             
    def draw(self, win):
        self.surface.fill(self.color)
        self.parcels.draw(self.surface)
        win.blit(self.surface, self.coords)

    def update(self, win):
        self.handle_events(win)
        self.draw(win)

username = 'Steve'
win_width = 900
win_height = 500


class MenuWin():
    def __init__(self, w=win_width-500, h=win_height-200):
        self.surface = pygame.Surface((w, h))
        #self.surface.fill((255, 255, 255))
        self.coords=(250, 100)

        level_images = [[pygame.image.load('buttons\p'+str(i)+'.png'),
                        pygame.image.load('buttons\o'+str(i)+'.png')] for i in range(4)]

        buttons = []
        
        x = (w-300)//2
        for i in range(4):
            y=50+i*50
            plain_img = level_images[i][0]
            over_img = level_images[i][1]
            
            button = wins.Button(supersurf=self.surface,
                                 plain_img=plain_img, over_img=over_img,
                                 x=x, y=y,
                                 absolute_x=self.coords[0],
                                 absolute_y=self.coords[1])
            buttons.append(button)
            
        self.buttons = buttons
            
    def update(self, win):
        self.surface.fill((255, 255, 255))

        selected = []
        for b in self.buttons:
            pressed = b.update()
            selected.append(pressed)
            
        win.blit(self.surface, self.coords)
        return selected

class SettingsBar():
    def __init__(self, w=win_width, h=60):
        self.surface = pygame.Surface((w, h))
        self.surface.fill((255, 255, 255))
        self.coords=(0, 0)

        music_on_button = wins.Button(supersurf=self.surface,
                                      plain_img=pygame.image.load('buttons\mo.png'),
                                      over_img=pygame.image.load('buttons\mo_o.png'),
                                      x=win_width-50, y=5,
                                      absolute_x=0, absolute_y=0)
         
        music_off_button = wins.Button(supersurf=self.surface,
                                       plain_img=pygame.image.load('buttons\mf.png'),
                                       over_img=pygame.image.load('buttons\mf_o.png'),
                                       x=win_width-50, y=5,
                                       absolute_x=0, absolute_y=0)
        
        menu_on_button = wins.Button(supersurf=self.surface,
                                     plain_img=pygame.image.load('buttons/pb.png'),
                                     over_img=pygame.image.load('buttons/rb_o.png'),
                                     x=10, y=5,
                                     absolute_x=0, absolute_y=0)

        menu_off_button = wins.Button(supersurf=self.surface,
                                      plain_img=pygame.image.load('buttons/rb.png'),
                                      over_img=pygame.image.load('buttons/pb_o.png'),
                                      x=10, y=5,
                                      absolute_x=0, absolute_y=0)

        self.buttons = {
            'music_on': music_on_button,
            'music_off': music_off_button,
            'menu_on': menu_on_button,
            'menu_off': menu_off_button}

        self.music_on = True
        self.menu_on = True

    def update(self, win):
        self.surface.fill((0, 0, 0))

        if self.music_on:
            pressed = self.buttons['music_on'].update()
            if pressed:
                self.music_on = False
                m_channel.stop()
        else:
            pressed = self.buttons['music_off'].update()
            if pressed:
                self.music_on = True
                m_channel.play(main_theme)

                

        out = False
        if self.menu_on:
            pressed = self.buttons['menu_on'].update()
            if pressed:
                out = True
                self.menu_on = False
                
        else:
            pressed = self.buttons['menu_off'].update()
            if pressed:
                out = True
                self.menu_on = True
                
              
        win.blit(self.surface, self.coords)
        
        return out

def basic_handle():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        

from time import time


class Game():
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load('space.jpg'), (win_width, win_height))
        self.main_win = pygame.display.set_mode((win_width, win_height))

        tutorial_win = ParcelWindow(w=win_width, h=win_height-200, n_of_parcels=7, strad=20, x=0, y=50,
                                orientation='h', w_x=0, w_y=100, color=background_color)
        
        beginner_win =  ParcelWindow(w=win_width, h=win_height-200, n_of_parcels=100, strad=20, x=0, y=50,
                                orientation='h', w_x=0, w_y=100, color=background_color)
        
        pro_win =  ParcelWindow(w=win_width, h=win_height-200, n_of_parcels=150, strad=20, x=0, y=50,
                                orientation='h', w_x=0, w_y=100, color=background_color)
        
        win_9 =  ParcelWindow(w=win_width, h=win_height-200, n_of_parcels=500, strad=20, x=0, y=50,
                                orientation='h', w_x=0, w_y=100, color=background_color,  chaos=True)

        self.menu = MenuWin()
        self.settings_bar = SettingsBar()

        self.levels = [tutorial_win, beginner_win, pro_win, win_9]
        self.scores = [0, 0, 0, 0]

        self.loose = pygame.image.load('loose.png')
        self.win = pygame.image.load('win.png')
        
        self.begin()
        
    def begin(self):
        self.introduction()
        
        m_channel.play(main_theme)
        self.main_win.blit(self.background, (0, 0))

        self.run_menu()

    def run_menu(self):
        self.main_win.blit(self.background, (0, 0))
        while True:
            level_selected = self.menu.update(self.main_win)
            if any(level_selected):
                   self.run_game(level_selected.index(True))
                   
            basic_handle()
                   

            self.settings_bar.update(self.main_win)
            
            pygame.display.update()
            pygame.event.pump()
            pygame.time.delay(200)

    def run_game(self, program_index):
        self.main_win.blit(self.background, (0, 0))
        program =  self.levels[program_index]
        while not self.settings_bar.update(self.main_win) and len(program.parcels.parcels) > 0:
            basic_handle()
            
            program.update(self.main_win)

            pygame.display.update()
            pygame.event.pump()
            pygame.time.delay(200)

        if len(program.parcels.parcels) == 0:
            self.scores[program_index] = program.score/program.max_score > 0.8
            
            if self.scores[program_index]:
                self.you_win()
                if all([self.scores]):
                    epilogue()
                    pygame.quit()
                    exit()
                
            else:
                self.you_loose()
                self.__init__()

        self.run_menu()

    def you_loose(self):
        self.main_win.blit(self.loose, (0, 0))
        pygame.display.update()

        m_channel.play(game_over_sound)

        pressed = False
        while not pressed:
            pygame.time.delay(50)

            pressed = pygame.key.get_pressed()[pygame.K_SPACE]
            basic_handle()
        return
    
    def you_win(self):
        self.main_win.blit(self.win, (0, 0))
        pygame.display.update()

        pressed = False
        while not pressed:
            pygame.time.delay(50)
        
            pressed = pygame.key.get_pressed()[pygame.K_SPACE]
            basic_handle()
        return

    def introduction(self):
        frames = [pygame.image.load('scenario/p'+str(i)+'.png') for i in range(9)]
        
        for i in frames:
            start = time()

            self.main_win.blit(i, ((win_width-i.get_width())//2, (win_height-i.get_height())//2))
            pygame.display.update()

            pressed = False
            while time()-start < 5 and not pressed:
                pygame.time.delay(5)
                pygame.event.pump()
                pressed = pygame.key.get_pressed()[pygame.K_SPACE]
                basic_handle()
                
            if pressed:
                break
        
    def epilogue(self):
        frames = [pygame.image.load('scenario/p'+str(i)+'.png') for i in range(3)]

        m_channel.play(win_music, 0)
        
        for i in frames:
            start = time()

            self.main_win.blit(i, ((win_width-i.get_width())//2, (win_height-i.get_height())//2))
            pygame.display.update()
            
            while time()-start > 5:
                pygame.time.delay(5)
                pygame.event.pump()
                basic_handle()

        return

    
Game()