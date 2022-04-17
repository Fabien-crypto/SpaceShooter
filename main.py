import pygame
from pygame import mixer
from random import randint
import sys
from PIL import Image, ImageFilter
from pygame.math import Vector2
import os


#Initialisation du jeu#
pygame.init()
pygame.font.init()

# Nom de la fenêtre #
pygame.display.set_caption("SpaceShoot")

#Définition de la police d'écriture #
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/menu/font.ttf", size)

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('green')

#On créer deux variables qui sont soit vrai soit fausses et qui sont utilisées dans la fonction session() pour indiquer au joueur si la session n'existe pas ou si elle existe déjà
existe_deja = 0
existe_pas = 0

#Icone jeu#
icon = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
pygame.display.set_icon(icon)

#Background des boutons#
buttonimg = pygame.image.load("assets/menu/button.png")
buttonimg = pygame.transform.scale(buttonimg,(150,50))
screen = pygame.display.set_mode((400, 600))

#On créer un fichier initialisation.txt avant que la fonction session() soit lancée pour que le jeu ne crash pas en indiquant que le fichier nom_session.txt n'existe pas car nom_session n'a pas été définit
with open("initialisation.txt","w") as init :
    init.write("0\n0\n0\n0\n0\n0\n")
    init.close()
nom_session = "initialisation"

# Fonction permettant de lire les données sauvegardées dans un fichier
def saveread(score):
    with open(nom_session+'.txt',"r") as fichier:
        list = fichier.readlines()
        fichier.close()
    if score == "bestscore":
        return list[0].replace("\n","")
    elif score == "volume":
        return list[2].replace("\n","")
    elif score == "position":
        return list[3].replace("\n","")
    elif score == "volume2":
        return list[4].replace("\n","")
    elif score == "position2":
        return list[5]
    else:
        return list[1].replace("\n","")

# Fonction permettant de sauvegarder les données tels que le volume du jeu, le meilleur score, le score dans un fichier
def save(score,vol,pos,vol2,pos2):
    bestscore = saveread("bestscore")
    fichier = open(nom_session+'.txt',"w+")
    if score > int(bestscore):
        fichier.write(str(score)+"\n"+str(score)+"\n"+str(vol)+"\n"+str(pos)+"\n"+str(vol2)+"\n"+str(pos2))
        fichier.close()
    elif score == -1:
        fichier.write(str(0)+"\n"+str(0)+"\n"+str(vol)+"\n"+str(pos)+"\n"+str(vol2)+"\n"+str(pos2))
        fichier.close()
    else:
        fichier.write(bestscore+"\n"+str(score)+"\n"+str(vol)+"\n"+str(pos)+"\n"+str(vol2)+"\n"+str(pos2))
        fichier.close()

# Fonction de connexion et d'inscription du joueur
def session(nom):
    BG = pygame.image.load("assets/menu/Background.png")
    global nom_session, existe_deja, existe_pas
    MENU_TEXT = get_font(23).render("SpaceShooter", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
    input_box1 = InputBox(100, 220, 200, 32)
    input_box2 = InputBox(100, 350, 200, 32)
    input_boxes = [input_box1, input_box2]
    done = False
    INSCRIPTION_TEXT = get_font(12).render("S'inscrire", True, "white")
    INSCRIPTION_RECT = INSCRIPTION_TEXT.get_rect(center=(200, 190))
    CONNEXION_TEXT = get_font(12).render("Se connecter", True, "white")
    CONNEXION_RECT = CONNEXION_TEXT.get_rect(center=(200, 320))
    try :
        os.remove(nom+'.txt')
    except OSError:
        pass

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            input_box1.handle_event_1(event)
            input_box2.handle_event_2(event)


        screen.blit(BG, (0, 0))
        screen.blit(INSCRIPTION_TEXT, INSCRIPTION_RECT)
        screen.blit(CONNEXION_TEXT,CONNEXION_RECT)
        screen.blit(MENU_TEXT,MENU_RECT)
        for box in input_boxes:
            box.draw(screen)
        
        if existe_deja == 1 :
            EXISTE_DEJA_TEXT = get_font(10).render("* Ce nom est déjà pris", True, "red")
            EXISTE_DEJA_RECT = EXISTE_DEJA_TEXT.get_rect(center=(200, 150))
            screen.blit(EXISTE_DEJA_TEXT, EXISTE_DEJA_RECT)
        if existe_pas == 1 :
            EXISTE_PAS_TEXT = get_font(10).render("* Ce nom n'existe pas", True, "red")
            EXISTE_PAS_RECT = EXISTE_PAS_TEXT.get_rect(center=(200, 410))
            screen.blit(EXISTE_PAS_TEXT, EXISTE_PAS_RECT)

        pygame.display.flip()

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = get_font(12).render(text, True, self.color)
        self.active = False

    # fonction du champ de texte d'inscription 
    def handle_event_1(self, event):
        global existe_deja,nom_session
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    nom_session = str(self.text).lower()
                    try:
                        with open(nom_session+'.txt', 'r') as f:
                            existe_deja = 1
                    except FileNotFoundError as e:
                        with open(nom_session+'.txt', 'w+') as f:
                            f.write("0\n0\n0.5\n250\n0.5\n250\n")
                            f.close()
                        os.remove("initialisation.txt")
                        main_menu()
                    except IOError as e:
                        with open(nom_session+'.txt', 'w+') as f:
                            f.write("0\n0\n0.5\n250\n0.5\n250\n")
                            f.close()
                        os.remove("initialisation.txt")
                        main_menu()
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text)<16:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = get_font(12).render(self.text, True, self.color)
    # Fonction du champ de texte de connexion
    def handle_event_2(self, event):
        global existe_pas,nom_session
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    nom_session = str(self.text).lower()
                    # On teste d'ouvrir un fichier comprenant le nom qu'a rentré l'utilisateur pour se connecter#

                    # S'il y arrive alors le fichier existe bien, il rentre dans le jeu
                    try:
                        with open(nom_session+'.txt', 'r') as f:
                            os.remove("initialisation.txt")
                            main_menu()

                    #Sinon on affiche un texte pour indiquer au joueur que cette session n'existe pas
                    except FileNotFoundError as e:
                        existe_pas = 1
                    except IOError as e:
                        existe_pas =1
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text)<16:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = get_font(12).render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)  

# On créer une classe bouton qu'on utilise dans les différents menus
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# On créer une classe explosion qui affiche une animation d'explosion lorsqu'un monstre est tué
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"assets/explosion/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (40, 40))
            if size == 2:
                img = pygame.transform.scale(img, (60, 60))
            if size == 3:
                img = pygame.transform.scale(img, (180, 180))
            #add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    # Fonction permettant de changer les images pour créer l'animation d'explosion
    def update(self):
        explosion_speed = 3
        #update explosion animation
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        #if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

    #classe mouvement du laser #
    def move(self, time):
        self.rect.y += self.velocity * time
        if self.rect.y >  screen.get_height():
            self.remove()

#Classe du monstre#s
class Monster(pygame.sprite.Sprite):
    def __init__(self, game):
        global soundObj 
        super().__init__()
        self.game = game
        soundObj = pygame.mixer.Sound('sounds/ennemy_explosion.aiff')
        soundObj.set_volume(float(saveread("volume2")))
        self.health = 1000
        self.max_health = 1000
        self.attack = 10
        self.all_laser = pygame.sprite.Group()
        self.image = pygame.image.load("assets/vaisseaux/ennemies/enemy-01/nomove_1.png")
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.delay = 90
        self.pos = Vector2(randint(15,360),-10)
        self.velocity = 90

    #On eneleve de la vie au monstre et on verifie s'il lui en reste. S'il lui en reste pas on affiche l'animation d'explosion avec le son d'explosion, on incremente le score du joueur et fait apparaitre une pièce
    def damage(self, amount) :            
        self.health -= amount
        if self.health <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            soundObj.play()
            coin = Coin(self,self.rect.centerx, self.rect.centery, 1)
            self.game.all_coin.add(coin)
            self.game.explosion_group.add(explosion)
            self.game.all_monsters.remove(self)
            self.game.player.score += 5

    #On Fait avancer les monstres en fonction de leur vitesse définit et si le monstre dépasse l'écran on le détruit pour ne pas ralentir le jeu
    def forward(self, time, velocity):
        self.pos += Vector2(0,velocity) * time
        self.rect.center = self.pos
        if self.game.check_collision(self,self.game.all_players) :
            self.game.player.damage(self.attack)
            self.game.all_monsters.remove(self)
        if self.rect.y > 590 :
            self.game.all_monsters.remove(self)
            self.game.player.damage(self.attack)

    # Fonction utilisée dans les vagues pour rajouter de la difficulté en diminuant le delai de spawn et en augmentant ainsi le nbr de monstres par vagues.
    def velocityUp(self, x) :
        self.velocity += x

    # Fonction qui arrete le déplacement des monstres
    def freeze(self):
        self.rect.center = self.pos
    # Fonction utilisée dans les vagues pour rajouter de la difficulté en augmentant la vie des monstres
    def HealthUp(self, x) :
        self.max_health += x
        self.health += x
        

#classe projectile de notre vaisseau #
class Projectile(pygame.sprite.Sprite) :
    # Définir le constructeur de cette classe #
    def __init__(self, player):
        super().__init__()
        soundObj = pygame.mixer.Sound('sounds/player_shoot.wav')
        soundObj.set_volume(float(saveread("volume2")))
        soundObj.play()
        self.velocity = 450
        self.player = player
        self.image = pygame.image.load('assets/missiles/PlayProjectile.png')
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + (player.rect.width)/2 - self.image.get_width()/2
        self.rect.y = player.rect.y

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self,time):
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters) :
            self.remove()
            monster.damage(self.player.attack)
        if self.rect.y < -10 :
            self.remove()
        self.rect.y -= self.velocity * time

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 100
        self.max_health = 100
        self.attack = 500
        self.velocity = 440
        self.score = 0
        self.money = 0
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
        self.rect = self.image.get_rect()
        self.rect.x = 160
        self.rect.y = 500
        self.shoot_delay = 250
        self.last_shoot =  pygame.time.get_ticks()
        self.clock = pygame.time.get_ticks()

    def damage(self, amount) :
        self.health -= amount

    def update_health_bar(self,surface):
        bar_color = (35, 188, 27)
        bar_position = [self.rect.x -10, self.rect.y + self.rect.height, self.health, 5]
        back_bar_color = (212, 63, 23)
        back_bar_position = [self.rect.x -10, self.rect.y + self.rect.height, self.max_health, 5]
        pygame.draw.rect(surface, back_bar_color, back_bar_position,0,3) #dessin barre de vie rouge #
        pygame.draw.rect(surface, bar_color, bar_position,0,3) #dessin barre de vie verte#

    def launch_projectile(self):
        #Création nouvelle instance du projectile et intervalle de temps#
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.all_projectiles.add(Projectile(self))
            self.last_shoot = now

    def HealthUp(self, x) :
        self.health += x
        self.max_health += x

    def ShootUp(self, x) :
        self.shoot_delay -= x

    def move_right(self, time):
        self.rect.x += self.velocity * time
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/right.png')
        self.image = pygame.transform.scale(self.image, (80, 80))
    def move_left(self, time):
        self.rect.x -= self.velocity * time
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/left.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_up(self, time):
        self.rect.y -= self.velocity * time
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def move_down(self, time):
        self.rect.y += self.velocity * time
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))
    def no_move(self):
        self.image = pygame.image.load('assets/vaisseaux/player/ship 01/nomove.png')
        self.image = pygame.transform.scale(self.image, (80,80))


class Coin(pygame.sprite.Sprite):
    def __init__(self,player, x, y, size):
        super().__init__()
        global sound_coin
        self.value = 1
        self.player = player
        sound_coin = pygame.mixer.Sound('sounds/coin.wav')
        sound_coin.set_volume(float(saveread("volume2")))
        self.images = []
        for num in range(1, 9):
            img = pygame.image.load(f"assets/coin/coin_0{num}.png")
            img = pygame.transform.scale(img,(25,25))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.pos = Vector2(x,y)
        self.counter = 0

    def update(self):
        flip_speed = 10
        #update explosion animation
        self.counter += 1
        if self.counter >= flip_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.counter >= flip_speed and self.index >= len(self.images) -1:
            self.counter = 0
            self.index = 0
            self.image = self.images[self.index]

    def remove(self):
        self.player.game.all_coin.remove(self)

    def forward(self, time, velocity):
        if pygame.sprite.spritecollide(self, self.player.game.all_players, False, pygame.sprite.collide_mask) :
            self.player.game.player.money += self.value
            sound_coin.play()
            self.remove()
        else :
            self.pos += Vector2(0,velocity) * time
            self.rect.center = self.pos

    def freeze(self):
        self.rect.center = self.pos

class Game:
    def __init__(self):
        #Génère notre joueur#
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.explosion_group = pygame.sprite.Group()
        self.all_monsters = pygame.sprite.Group()
        self.monster  = Monster(self)
        self.coin = Coin(self,1,1,1)
        self.all_coin = pygame.sprite.Group()
        self.pressed = {}
        self.delay_spawn = 1500
        self.last_monster = pygame.time.get_ticks()

    def check_collision(self, sprite, group) :
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def SpawnUp(self, x):
        self.delay_spawn -= x

    def pause(self):
        self.monster.velocity = 0

    def spawn_monster(self):
        now = pygame.time.get_ticks()
        monster = Monster(self)
        if now - self.last_monster > self.delay_spawn :
            self.all_monsters.add(monster)
            self.last_monster = now


def options(menu):
    global volume,volume2
    global position,position2
    #Déclaration des variables de son#
    volume = float(saveread("volume"))
    position= int(saveread("position"))
    position2= int(saveread("position2"))
    volume2 = float(saveread("volume2"))
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("black")
        OPTIONS_TEXT = get_font(12).render("Choisir tes paramètres.", True, "white")
        OPTIONS_TEXT1 = get_font(12).render("Musique de fond", True, "white")
        OPTIONS_TEXT2 = get_font(12).render("Effets spéciaux ", True, "white")
        POURCENTAGE_FOND = get_font(12).render((str(int(200*(volume)))+"%"), True, "white")
        POURCENTAGE_FOND2 = get_font(12).render((str(int(200*(volume2)))+"%"), True, "white")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(200, 50))
        OPTIONS_RECT1 = OPTIONS_TEXT1.get_rect(center=(200, 150))
        OPTIONS_RECT2 = OPTIONS_TEXT1.get_rect(center=(200,300))
        OPTIONS_POURCENTAGE_FOND_RECT = POURCENTAGE_FOND.get_rect(center=(40, 205))
        OPTIONS_POURCENTAGE_FOND_RECT2 = POURCENTAGE_FOND2.get_rect(center=(40, 355))
        SESSION_TEXT = get_font(12).render(nom_session, True, "white")
        SESSION_RECT = SESSION_TEXT.get_rect(bottomleft=(15, 580))
        screen.blit(SESSION_TEXT,SESSION_RECT)
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        screen.blit(OPTIONS_TEXT1, OPTIONS_RECT1)
        screen.blit(OPTIONS_TEXT2, OPTIONS_RECT2)
        screen.blit(POURCENTAGE_FOND,OPTIONS_POURCENTAGE_FOND_RECT)
        screen.blit(POURCENTAGE_FOND2,OPTIONS_POURCENTAGE_FOND_RECT2)

        RESET_BUTTON = Button(image=buttonimg, pos=(200, 460), text_input="Reset", font=get_font(12), base_color="White", hovering_color="Green")

        OPTIONS_BACK = Button(image=None, pos=(200, 550), 
                            text_input="BACK", font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_MOINS = Button(image=None, pos=(350, 205),
                            text_input="-",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_PLUS = Button(image=None, pos=(380, 205),
                            text_input="+",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_MOINS2 = Button(image=None, pos=(350, 355),
                        text_input="-",font=get_font(12), base_color="white", hovering_color="Green")
        OPTIONS_PLUS2 = Button(image=None, pos=(380, 355),
                        text_input="+",font=get_font(12), base_color="white", hovering_color="Green")


        buttonlist = [OPTIONS_MOINS,OPTIONS_MOINS2,OPTIONS_PLUS,OPTIONS_PLUS2,OPTIONS_BACK,RESET_BUTTON]

        for button in buttonlist:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)


        pygame.draw.rect(screen, (75,75,75), pygame.Rect(72, 197, 256, 16),3,5)
        pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(75, 200, position, 10),0,2)
        pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(72, 347, 256, 16),3,5)
        pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(75, 350, position2, 10),0,2) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key==pygame.K_ESCAPE:
                    if menu == "menu":
                        return 0
                    else :
                        BG2 = pygame.image.load("assets/menu/blurrybg.jpg")
                        screen.blit(BG2, (0, 0))
                        return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    if menu == "menu":
                        return 0
                    else:
                        BG2 = pygame.image.load("assets/menu/blurrybg.jpg")
                        screen.blit(BG2, (0, 0))
                        return 0

                if OPTIONS_PLUS.checkForInput(OPTIONS_MOUSE_POS):
                    if volume<0.5 and position <250: 
                        volume += 0.05
                        position += 25
                        volume = round(volume,2)
                        save(int(saveread("score")),volume,position,saveread("volume2"),saveread("position2"))
                        mixer.music.set_volume(float(saveread("volume")))

                if OPTIONS_MOINS.checkForInput(OPTIONS_MOUSE_POS):
                    if volume>0 and position >0: 
                        volume -= 0.05
                        position -= 25
                        volume = round(volume,2)
                        save(int(saveread("score")),volume,position,saveread("volume2"),saveread("position2"))
                        mixer.music.set_volume(float(saveread("volume")))

                if OPTIONS_PLUS2.checkForInput(OPTIONS_MOUSE_POS):
                    if volume2<0.5 and position2 <250: 
                        volume2 += 0.05
                        position2 += 25
                        volume2 = round(volume2,2)
                        save(int(saveread("score")),saveread("volume"),saveread("position"),volume2,position2)
                        mixer.music.set_volume(float(saveread("volume")))

                if OPTIONS_MOINS2.checkForInput(OPTIONS_MOUSE_POS):
                    if volume2>0 and position2 >0: 
                        volume2 -= 0.05
                        position2 -= 25
                        volume2 = round(volume2,2)
                        save(int(saveread("score")),saveread("volume"),saveread("position"),volume2,position2)
                        mixer.music.set_volume(float(saveread("volume")))
                
                if RESET_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    if warning()==1:
                        volume = 0.5
                        volume2 = 0.5
                        position = 250
                        position2 = 250
                        save(-1,volume,position,volume2,position2)
                        mixer.music.set_volume(float(saveread("volume")))
    
        pygame.display.update()


def warning() :
    screen.fill("black")
    buttonimg1 = pygame.image.load("assets/menu/button.png")
    buttonimg1 = pygame.transform.scale(buttonimg1,(100,30))  
    while True:
        color = (131, 136, 143)

        pygame.draw.rect(screen, color, pygame.Rect(10, 175, 380, 130))

        warning_TEXT = get_font(9).render("Etes-vous sûr de vouloir réinitialiser ?", True, "white")
        warning_RECT = warning_TEXT.get_rect(topleft=(20, 200))
        warning_TEXT2 =  get_font(9).render("(cela inclut le score)", True, "white")
        warning_RECT2 = warning_TEXT.get_rect(topleft=(100, 220))
        screen.blit(warning_TEXT, warning_RECT)
        screen.blit(warning_TEXT2, warning_RECT2)

        YES_BUTTON = Button(image=buttonimg1, pos=(130, 270), text_input="Oui", font=get_font(8), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=buttonimg1, pos=(260, 270), text_input="Quitter", font=get_font(8), base_color="White", hovering_color="Green")   
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        for button in [YES_BUTTON,QUIT_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)
        
        pygame.display.update() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key==pygame.K_ESCAPE:
                    mixer.music.unpause()
                    return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    return 0
                if YES_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    return 1

def paused() :
    global pause
    pause = 1
    while True:
        PLAY_BUTTON = Button(image=buttonimg, pos=(200, 200), text_input="Reprendre", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=buttonimg, pos=(200, 280), text_input="Options", font=get_font(12), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=buttonimg, pos=(200, 360), text_input="Menu", font=get_font(12), base_color="White", hovering_color="Green")
        SESSION_TEXT = get_font(12).render(nom_session, True, "white")
        SESSION_RECT = SESSION_TEXT.get_rect(bottomleft=(35, 580))
        screen.blit(SESSION_TEXT,SESSION_RECT)
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                if event.key==pygame.K_ESCAPE:
                    mixer.music.unpause()
                    return 7
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    mixer.music.unpause()
                    return 0
                if OPTIONS_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    options("jeu")
                if QUIT_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    save(score,saveread("volume"),saveread("position"),saveread("volume2"),saveread("position2"))
                    mixer.music.unpause()
                    main_menu()
    

def over_menu():
    BG = pygame.image.load("assets/menu/Background.png")
    screen.blit(BG, (0, 0))
    MENU_TEXT = get_font(23).render("SpaceShooter", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
    OVER_TEXT = get_font(20).render("Game Over!", True, "white" )
    OVER_RECT = OVER_TEXT.get_rect(center=(200, 150))
    screen.blit(OVER_TEXT, OVER_RECT)
    best_score = pygame.image.load('assets/icon/best_score.png')
    best_score = pygame.transform.scale(best_score,(20,20))
    prec_score = pygame.image.load('assets/icon/prec_score.png')
    prec_score = pygame.transform.scale(prec_score,(20,20))
    Best_Score_TEXT = get_font(12).render("Meilleur Score: "+ saveread("bestscore"), True, "white")
    Best_Score_RECT = Best_Score_TEXT.get_rect(center=(215, 350))
    Prec_Score_TEXT = get_font(12).render(("Score Précédent: "+ saveread("prec")), True, "white")
    Prec_Score_RECT = Prec_Score_TEXT.get_rect(center=(215, 400))
    screen.blit(MENU_TEXT, MENU_RECT)
    screen.blit(Best_Score_TEXT, Best_Score_RECT)
    screen.blit(Prec_Score_TEXT, Prec_Score_RECT)
    screen.blit(best_score,(55,338))
    screen.blit(prec_score,(55,388))
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_MENU_BUTTON = Button(image=buttonimg, pos=(200, 250), text_input="Menu", font=get_font(12), base_color="White", hovering_color="Green")
        for button in [BACK_MENU_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
        pygame.display.update()

def main_menu():
    global nom_session
    mixer.music.load('sounds/01_Title-Screen.wav')    
    mixer.music.set_volume(float(saveread("volume")))
    mixer.music.play(-1, 0.0, 0)
    trashimg = pygame.image.load('assets/icon/trash.png')
    trashimg = pygame.transform.scale(trashimg,(30,30))
    while True:
        BG = pygame.image.load("assets/menu/Background.png")
        best_score = pygame.image.load('assets/icon/best_score.png')
        best_score = pygame.transform.scale(best_score,(20,20))
        prec_score = pygame.image.load('assets/icon/prec_score.png')
        prec_score = pygame.transform.scale(prec_score,(20,20))
        screen.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(23).render("SpaceShooter", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(200, 80))
        PLAY_BUTTON = Button(image=buttonimg, pos=(200, 200), text_input="PLAY", font=get_font(12), base_color="White", hovering_color="Green")
        OPTIONS_BUTTON = Button(image=buttonimg, pos=(200, 280), text_input="OPTIONS", font=get_font(12), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=buttonimg, pos=(200, 360),text_input="QUIT", font=get_font(12), base_color="White", hovering_color="Green")
        Best_Score_TEXT = get_font(12).render("Meilleur Score : "+ saveread("bestscore"), True, "white")
        Best_Score_RECT = Best_Score_TEXT.get_rect(topleft=(100, 442))
        Prec_Score_TEXT = get_font(12).render(("Score Précédent : "+ saveread("prec")), True, "white")
        Prec_Score_RECT = Prec_Score_TEXT.get_rect(topleft=(100, 493))
        SESSION_TEXT = get_font(12).render(nom_session, True, "white")
        SESSION_RECT = SESSION_TEXT.get_rect(bottomleft=(45, 578))
        DELETE_BUTTON = Button(image=trashimg, pos=(25, 570), text_input="", font=get_font(12), base_color="White", hovering_color="Green")
        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(Best_Score_TEXT, Best_Score_RECT)
        screen.blit(Prec_Score_TEXT, Prec_Score_RECT)
        screen.blit(best_score,(55,438))
        screen.blit(prec_score,(55,488))
        screen.blit(SESSION_TEXT,SESSION_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON,DELETE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    jeu()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    jeu()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options("menu")
                if DELETE_BUTTON.checkForInput(MENU_MOUSE_POS) :
                    nom = str(nom_session)
                    with open('initialisation.txt',"w+") as f:
                        f.write("0\n0\n0\n0\n0\n0\n")
                        f.close()
                    nom_session = 'initialisation.txt'
                    session(nom)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
            
        pygame.display.update()


def jeu():
    global color
    global score
    color="White"
    #Musique de fond#    
    mixer.music.load('sounds/10 Drummed vaus.mp3')
    mixer.music.play(-1, 0.0, 0)
    volume = float(saveread("volume"))

    #Temps du jeu #
    clock = pygame.time.Clock()
    # Générer une fenêtre de jeu #
    pygame.display.set_caption("SpaceShoot")

    #background# 
    global background
    background = pygame.image.load('assets/fond/frameBackground.png')
    background = pygame.transform.scale(background,(400,600))
    y_background = 0
    #Chargement de notre jeu#
    game = Game()

    #Chargement image pour score et bestscore#
    prec_score = pygame.image.load('assets/icon/prec_score.png')
    money = pygame.image.load('assets/coin/coin_01.png')
    # Boucle jeu #
    running = True

    #définition des variables qui concernent les vagues d'ennemis#
    velocity = game.monster.velocity
    vague = 1
    pause = 0
    last_seconde = pygame.time.get_ticks()
    delai = 1000
    count = 0
    pause = 0
    cost_power=1
    cost_life=300
    cost_delay=1
    cost_earning=1
    spawn_delay = 20
    last_seconde2 = pygame.time.get_ticks()
    bestscore = int(saveread("bestscore"))
    prec_score = pygame.transform.scale(prec_score,(20,20))
    money = pygame.transform.scale(money,(20,20)) 
    color1 = "Red"
    color2 = "Red"
    color3 = "Red"
    color4 = "Red"
    value = 1

    while running :

        #appliquer arrière plan et défilement#
        dt = clock.tick(2000)
        time = dt/1000

        # Si le jeu n'est pas en pause on fait défiler le fond d'écran verticalement#
        if pause != 1:
            y_background += 0.25
        if y_background < 600 :
            screen.blit(background,(0,y_background))
            screen.blit(background, (0, y_background-600))
        else :
            y_background = 0
            screen.blit(background, (0, y_background))

        #Appliquer image de notre joueur#
        screen.blit(game.player.image, game.player.rect)

        #Appliquer l'ensemble de mon grp de projectiles, de joueur, de monstres et de pièces en les dessinant#
        game.explosion_group.update()
        game.player.all_projectiles.draw(screen)
        game.all_monsters.draw(screen)
        game.explosion_group.draw(screen)
        game.all_coin.update()
        game.all_coin.draw(screen)

        # Si le joueur n'a plus de vie, on joue la musique et le menu Game Over#
        if game.player.health <= 0:
            soundObj = pygame.mixer.Sound('sounds/game_over.wav')
            soundObj.set_volume(volume)
            soundObj.play()
            pygame.mixer.music.stop()
            save(game.player.score,saveread("volume"),saveread("position"),saveread("volume2"),saveread("position2"))
            over_menu()
        #Affichage du score #
        Score_TEXT = get_font(13).render((str(game.player.score)), True, color )
        Score_RECT = Score_TEXT.get_rect(topleft=(60, 18))
        Money_TEXT = get_font(13).render((str(game.player.money)), True, "White" )
        Money_RECT = Score_TEXT.get_rect(topleft=(60, 50))

        #Affichage du score #
        Vague_TEXT = get_font(13).render(("Vague "+str(vague)), True, "White" )
        Vague_RECT = Vague_TEXT.get_rect(bottomright=(380, 590))
        
        #Si le joueur dépasse son ancien meilleur score, le texte du meilleur score s'affiche en rouge pour lui indiquer#
        if game.player.score > bestscore:
            color="Red"

        # On affiche les icons de meilleur score et de score avec leur textes respectifs#
        screen.blit(prec_score,(20,15))
        screen.blit(money,(20,45))
        screen.blit(Score_TEXT, Score_RECT)
        screen.blit(Vague_TEXT, Vague_RECT)
        screen.blit(Money_TEXT, Money_RECT)

        # On fait avancer tout les projectiles#
        for projectile in game.player.all_projectiles :
            projectile.move(time)

        #On actualise la barre de vie du joueur#
        game.player.update_health_bar(screen)
        #################################################################################
        ################################# VAGUE ENNEMIS #################################
        #################################################################################
        now = pygame.time.get_ticks()
        # Si le compteur de secondes est inférieur a 15 on l'incrémente de 1 chaque secondes#
        if (now - last_seconde > delai) and count<15 :
            count +=1 
            last_seconde = now
        # Tant que les 15 secondes ne sont pas finis on fait spawn des monstres#
        elif count<15 and pause == 0:
            game.spawn_monster()
        #Si les 15 secondes sont terminées et qu'il n'y a plus de monstres alors on affiche le menu de vague terminée
        elif count==15 and len(game.all_monsters)==0:
            COUT_POWER_TEXT = get_font(10).render((str(cost_power)), True, color1 )
            COUT_POWER_RECT = COUT_POWER_TEXT.get_rect(topleft=(120,436 ))
            COUT_LIFE_TEXT = get_font(10).render((str(cost_life)), True, color2 )
            COUT_LIFE_RECT = COUT_LIFE_TEXT.get_rect(topleft=(290,436 ))
            COUT_DELAY_TEXT = get_font(10).render((str(cost_delay)), True, color3 )
            COUT_DELAY_RECT = COUT_DELAY_TEXT.get_rect(topleft=(120,525 ))
            COUT_EARNING_TEXT = get_font(10).render((str(cost_earning)), True, color4 )
            COUT_EARNING_RECT = COUT_EARNING_TEXT.get_rect(topleft=(290,525 ))
            screen.blit(COUT_POWER_TEXT, COUT_POWER_RECT)
            screen.blit(COUT_LIFE_TEXT, COUT_LIFE_RECT)
            screen.blit(COUT_DELAY_TEXT, COUT_DELAY_RECT)
            screen.blit(COUT_EARNING_TEXT, COUT_EARNING_RECT)        

            VagueFinish_TEXT = get_font(20).render(("Vague "+str(vague)+" Terminée"), True, "White" )
            VagueFinish_RECT = VagueFinish_TEXT.get_rect(center=(200,300 ))
            screen.blit(VagueFinish_TEXT, VagueFinish_RECT)
            VAGUE_MOUSE_POS=pygame.mouse.get_pos()
            POWER_SHOOT_BUTTON = Button(image=buttonimg, pos=(120, 400), text_input="Power Shoot", font=get_font(8), base_color="White", hovering_color=color1)
            LIFE_BUTTON = Button(image=buttonimg, pos=(290, 400), text_input="Upgrade life", font=get_font(8), base_color="White", hovering_color=color2)
            SHOOT_DELAY_BUTTON = Button(image=buttonimg, pos=(120, 490), text_input="Shoot delay", font=get_font(8), base_color="White", hovering_color=color3)
            EARNING_BUTTON = Button(image=buttonimg, pos=(290, 490), text_input="Money Value", font=get_font(8), base_color="White", hovering_color=color4)
            screen.blit(money,(93,430))
            screen.blit(money,(93,520))
            screen.blit(money,(263,430))
            screen.blit(money,(263,520))                  
            
            for button in [POWER_SHOOT_BUTTON,LIFE_BUTTON,SHOOT_DELAY_BUTTON,EARNING_BUTTON]:
                    button.changeColor(VAGUE_MOUSE_POS)
                    button.update(screen)   

            # On définit les conditions pour afficher en vert ou en rouge les boutons en fonction du nombre de pièces suffisantes qu'a le joueur
            if game.player.money >= cost_power :
                color1="Green"
            if game.player.money < cost_power :
                color1="Red"
            if game.player.money >= cost_life :
                color2="Green"
            if (game.player.money < cost_life) or ((game.player.health+15) >= game.player.max_health)  :
                color2 = "Red"
            if game.player.money >= cost_delay :
                color3="Green"
            if game.player.money < cost_delay :
                color3 = "Red"   
            if game.player.money >= cost_earning :
                color4="Green"
            if game.player.money < cost_earning:
                color4 = "Red"   
            # Si les 15 secondes sont passées on rénitialise le compteur de secondes à 0, on incrémente le compteur de vague de 1 et on augmente les paramètres de difficultés#
            if now - last_seconde > 15000:
                count = 0
                last_seconde = now
                vague +=1
                velocity += 10
                game.SpawnUp(spawn_delay)
                spawn_delay += 75
                game.monster.attack += 10
                game.player.attack -= 100


        #################################################################################
        # vérifier si le joueur souhaite bouger ou tirer#
        if game.pressed.get(pygame.K_SPACE):
            game.player.launch_projectile()
        if (game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s)) and game.player.rect.y + (game.player.rect.height) < screen.get_height():
            game.player.move_down(time)
        if (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) and game.player.rect.y > 0:
            game.player.move_up(time)
        if (game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d)):
            game.player.move_right(time)
        if (game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q)):
            game.player.move_left(time)
        if not((game.pressed.get(pygame.K_DOWN) or game.pressed.get(pygame.K_s)) or  
            (game.pressed.get(pygame.K_UP) or game.pressed.get(pygame.K_z)) or 
            (game.pressed.get(pygame.K_RIGHT) or game.pressed.get(pygame.K_d)) or  
            (game.pressed.get(pygame.K_LEFT) or game.pressed.get(pygame.K_q)) ):
            game.player.no_move()
        if (game.player.rect.x) > screen.get_width():
            game.player.rect.x = 0 - game.player.rect.width 
        elif (game.player.rect.x) < -(game.player.rect.width) :
            game.player.rect.x = screen.get_width()

        # Si le jeu n'est pas en pause on fait avancer les pièces sinon on les arrête avec la fonction freeze
        for coin in game.all_coin :
            if pause == 0:
                coin.forward(time, velocity)
            else:
                coin.freeze()
        # Si le jeu n'est pas en pause on fait avancer les monstres sinon on les arrête avec la fonction freeze
        for monster in game.all_monsters :
            if pause == 0:
                monster.forward(time,velocity)
            else:
                monster.freeze()
        # On définit constamment la valeur des pièces
        for coin in game.all_coin :
            coin.value = value
        #fermeture du jeu#
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                running = False
                score = game.player.score
                save(score,saveread("volume"),saveread("position"),saveread("volume2"),saveread("position2"))
                pygame.quit()
                sys.exit()
            # On créer un évènement permettant de détecter si une fonction est enfoncée et d'effectuer une action plusieurs fois tant que la touche est enfoncée
            elif event.type == pygame.KEYDOWN :
                game.pressed[event.key]=True
                # SI le joeuur appuie sur la touche échape alors on lance le menu jeu, on mets en pause la musique et on mets le fond de jeu en flou#
                if event.key==pygame.K_ESCAPE:
                    mixer.music.pause()
                    score = game.player.score
                    pygame.image.save(screen,"assets/menu/currentbg.jpg")
                    OriImage = Image.open('assets/menu/currentbg.jpg')
                    blurImage = OriImage.filter(ImageFilter.BLUR)
                    blurImage.save('assets/menu/blurrybg.jpg')
                    BG2 = pygame.image.load('assets/menu/blurrybg.jpg')
                    screen.blit(BG2, (0, 0))
                    listkeys = [pygame.K_DOWN,pygame.K_UP,pygame.K_RIGHT,pygame.K_SPACE,pygame.K_LEFT,pygame.K_s,pygame.K_z,pygame.K_q,pygame.K_d]
                    # On mets la valeur de "touche enfoncée" sur pause pour régler un bug qui laissait le joueur bouger même si le menu pause est lancé
                    for key in listkeys:
                        game.pressed[key] = False
                    pause = 1
                    paused()
                    last_seconde2 = pygame.time.get_ticks()
            # Détection si le joueur relache une touche qu'il avait enfoncé
            if event.type == pygame.KEYUP :
                game.pressed[event.key] = False
            # Détection des clics de la souris du joueur lorsqu'il a le menu d'amélioration d'affiché entre deux vagues 
            if event.type == pygame.MOUSEBUTTONDOWN and count==15 and len(game.all_monsters)==0:
                    #Si le joueur appui sur le bouton amélioration de la puissance de tir alors :
                    if POWER_SHOOT_BUTTON.checkForInput(VAGUE_MOUSE_POS):
                        if game.player.money >= cost_power :
                            game.player.attack += 100
                            game.player.money -= cost_power
                            cost_power*=2
                    #Si le joueur appui sur le bouton amélioration de la vie alors :
                    if LIFE_BUTTON.checkForInput(VAGUE_MOUSE_POS):
                        if game.player.money >= cost_life and (game.player.health+15) <= game.player.max_health:
                            game.player.health += 15
                            game.player.money -= cost_life
                    #Si le joueur appui sur le bouton de réduction de delai de tir alors :
                    if SHOOT_DELAY_BUTTON.checkForInput(VAGUE_MOUSE_POS):
                        if game.player.money >= cost_delay and game.player.shoot_delay >=100:
                            game.player.shoot_delay -= 10
                            game.player.money -= cost_delay
                            cost_delay*=2
                    #Si le joueur appui sur le bouton amélioration de la valeur des pièces alors :
                    if EARNING_BUTTON.checkForInput(VAGUE_MOUSE_POS):
                        if game.player.money >= cost_earning :
                            value +=1
                            game.player.money -= cost_earning
                            cost_earning*=2

        now2 = pygame.time.get_ticks()
        if now2 - last_seconde2 >= 1:
            pause = 0

        #mettre à jour l'écran  #
        pygame.display.update()

session('test.txt')