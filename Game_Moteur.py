import pygame as pg
import random
import time
import Thomas_prog as Thomas
pressed = False
jump_distance =  [14,10,7,4,2,2,4,7,10,12]

class Player:
    """

    """
    def __init__(self,x,y,rect):

        self.rect= rect
        self.x = x
        self.y = y

        self.rect.height = 121 #Hitbox du joueur
        self.rect.width = 56

        self.left =  False #déplacement du perso
        self.right = False

        self.jump =  False
        self.jump_count = 0

        self.worldx = 0 #Valeurs de déplacement du perso dans le monde de jeu
        self.worldy = 0

        self.coin=0

        self.dead= False
        self.death_frame_count=0

        self.idle_frame=0
        self.frame_count = 0

        self.lastcheckpoint= (x,y,self.worldx,self.worldy,-506) # bgy
        self.debug= False


    def hitbox(self):
        """
        Mise à jour du Rect du perso
        """
        self.rect.x = self.x + 14
        self.rect.y = self.y

    def deplacement(self,bg1x,bg2x,dep_bg_right,dep_bg_left):
        global pressed
        """
        Test pour les touches.
        Les claviers Azerty et Qwerty sont supportés.
        Les touches sont:
            W, Z ou ESPACE pour sauter.
            A ou Q pour aller à gauche
            D pour aller à droite
            R pour mourir
            SHIFT + F3  pour ouvrir la fonction debug

        Le background commence à bouger quand le perso se rapproche des bords
        """
        k=pg.key.get_pressed()
        if (k[pg.K_w] or k[pg.K_z] or k[pg.K_SPACE]): self.jump=True
        if (k[pg.K_a] or k[pg.K_q]):
            if dep_bg_right:
                bg1x[0]    += 10
                bg2x[0]    += 10
                self.worldx -= 10
            else: self.x  -= 5
            self.left = True
            self.right = False

        elif k[pg.K_d]:
            if dep_bg_left:
                bg1x[0]    -= 10
                bg2x[0]    -= 10
                self.worldx+= 10
            else: self.x  +=  5
            self.left = False
            self.right = True

        else:
            self.left = False
            self.right = False
            self.frame_count = 0

        if k[pg.K_r]:
            self.dead = True

        if k[pg.K_LSHIFT] and k[pg.K_F3] :
            if not pressed:
                self.debug = not self.debug
                pressed=True
        else: pressed=False

    def _jump(self,bgy,dep_bg_top,dep_bg_bot):
        """
        Le saut est divisé en deux parties. La partie initiale où le perso monte( quand "jump_count" est inférieur à 30 )
        et la deuxième partie où il descend ( quand "jump_count" est supérieur à 30 )
        """

        if self.jump:
            if self.jump_count < 30:
                self.jump_count += 1
                if dep_bg_top:
                    bgy[0] += jump_distance[self.jump_count//6]
                    self.worldy -= jump_distance[self.jump_count//6]
                else:
                    self.y -= jump_distance[self.jump_count//6]


            elif 10 < self.jump_count:
                self.jump_count += 1
                if dep_bg_bot :
                    try:                # Pour les grandes distances la variable "jump count" devient trop grande comme index pour "jump_distance"....
                        bgy[0] -= jump_distance[self.jump_count//6]
                        self.worldy += jump_distance[self.jump_count//6]
                    except:
                        bgy[0] -= jump_distance[9] # ...donc la dernière valeur de la liste est prise comme distance parcourue
                        self.worldy += jump_distance[9]
                else:
                    try:
                        self.y += jump_distance[self.jump_count//6]
                    except:
                        self.y += jump_distance[9]


            if self.y > 452:
                self.jump_count = 0
                self.y = 450 - self.worldy
                self.jump = False

            elif self.y < 0:
                self.jump_count = 30


    def death(self,bgy):
        """

        """
        self.dead = False
        self.death_frame_count = 0
        self.x = self.lastcheckpoint[0]
        self.y = self.lastcheckpoint[1]
        self.worldx = self.lastcheckpoint[2]
        self.worldy = self.lastcheckpoint[3]
        bgy[0] = self.lastcheckpoint[4]
        self.jump = True
        self.jump_count = 30
        self.hitbox()

class obstacle:
    """
    L'obstacle est un objet "solide", on ne peut pas le traverser, on est donc bloqué
    en cas de collision.
    """
    def __init__(self,coordinates,rect):

        '''
        Initialise la position de l' obstacle dans le monde de jeu et la position
        du Rect
        '''
        self.X = coordinates[0]
        self.Y = coordinates[1]
        self.rect = rect
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.collision = False

    def main(self,player):

        self.redraw_obstacle(player)
        self.collision_obstacle(player)

    def collision_obstacle(self,player):
        """
        Collision avec les obstacles. Cette partie est mieux expliqué dans la synthese.
        """
        if self.rect.colliderect(player.rect):
                overlap = self.rect.clip(player.rect)
                if overlap.width> overlap.height: #collision verticale
                    if player.y + player.rect.height < self.rect.y + 30:
                        if player.jump_count > 30:
                            player.jump= False
                            player.jump_count=0
                            self.collision=True
                            player.y=self.rect.y - player.rect.height + 1

                    elif player.y < self.rect.y + self.rect.height - 15:
                        player.jump_count = 30
                else:                               #collision horizontale

                    if player.x + player.rect.width < self.rect.x :
                        player.x = self.rect.x - player.rect.width - 17
                    elif player.x>self.rect.x + 31:
                        player.x = self.rect.x + self.rect.width - 11

        elif  self.collision  and not  player.jump and  player.y != 450 - player.worldy :
            player.jump = True
            player.jump_count = 31
            self.collision=False




##    '''
    def redraw_obstacle(self,player):

        """
        Mise à jour des coordonnées x,y  du Rect de l' obstacle.

        """
        self.rect.x = self.X - player.worldx
        self.rect.y = self.Y - player.worldy


class coin:
    """
    Les pièces sont ramassées en cas de collision.
    """
    def __init__(self,coordinates,rect) :

        '''
        Initialise la position des pièces dans le monde de jeu, la position
        du Rect et la valeur de départ de l'affichage
        '''
        self.X = coordinates[0]
        self.Y = coordinates[1]
        self.rect = rect
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.collision = False
        self.frame = random.randint(0,40)

    def main(self,player):

        self.redraw(player.worldx,player.worldy)
        self.coin_collision(player)

    def redraw(self,world_x,world_y):
        self.rect.x = self.X - world_x
        self.rect.y = self.Y - world_y

    def coin_collision(self,player):
        if player.rect.colliderect(self.rect):

            self.collision = True
            player.coin  += 1

class spike:
    """
    Les piques sont mortelles si on rentre en collision.
    """
    def __init__(self,coordinates,rect):

        '''
        Initialise la position des pointes dans le monde de jeu et la position
        du Rect
        '''

        self.X = coordinates[0]
        self.Y = coordinates[1]
        self.rect = rect
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]

    def main(self,player):
        self.redraw(player.worldx,player.worldy)
        self.collision(player)

    def redraw(self,world_x,world_y):
        self.rect.x = self.X - world_x
        self.rect.y = self.Y - world_y

    def collision(self,player):
        if player.rect.colliderect(self.rect):
            player.dead = True

class flag:
    """
    Les drapeaux sont des checkpoint. Si on réussit à résoudre l' énigme, on débloque le checkpoint
    et le point de respawn (point de départ en cas de mort) est mis à jour.
    """
    def __init__(self,coordinates,rect):
        '''
        Initialise la position du drapeau (checkpoint) dans le monde de jeu, la position
        du Rect et si le drapeau a été prit ou non.
        '''
        self.X = coordinates[0]
        self.Y = coordinates[1]
        self.rect = rect
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]
        self.frame = 0
        self.taked = False

    def main(self,player,bgy):
        self.redraw(player.worldx,player.worldy)
        self.checkpoint(player,bgy)

    def redraw(self,world_x,world_y):
        self.rect.x = self.X - world_x
        self.rect.y = self.Y - world_y

    def checkpoint(self,player,bgy):
        """
        Test de collision avec le perso.
        S' il y a une collision, le module de Thomas est appellé.
        Si le module de Thomas retourne True (donc le joueur a répondu juste au
        quiz) le drapeau est pris et la position de "respawn" est mise à jour,
        sinon le perso meurt. Le checkpoint n'est pas débloqué et le perso
        revient donc au dernier checkpoint débloqué.
        """
        if player.rect.colliderect(self.rect) and not self.taked and not player.dead:
            if Thomas.mainThomas(): #Partie Thomas
                self.taked = True
                player.lastcheckpoint = (self.rect.x,self.rect.y  -  71,player.worldx,player.worldy,bgy)
            else: player.dead=True

class exit:
    """
    "Exit" est la fin du niveau. Il peut y en avoir un seul par niveau.
    """
    def __init__(self,coordinates,rect):
        '''
        Initialise la position de la fin dans le monde de jeu et  la position
        du Rect
        '''
        self.X = coordinates[0]
        self.Y = coordinates[1]
        self.rect = rect
        self.rect.x = coordinates[0]
        self.rect.y = coordinates[1]

    def main(self,player):
        self.redraw(player.worldx,player.worldy)
        return self.collision(player)

    def redraw(self,world_x,world_y):

        self.rect.x = self.X - world_x
        self.rect.y = self.Y - world_y

    def collision(self,player):
        if player.rect.colliderect(self.rect):
            return True
        return False


class knight:
    """
    Les knights sont sûrement les objets les plus complexes du jeu.
    Ils possèdent les variables de position absolue x et y,  la valeur "distancemax"
    qui représente la distance maximale que l'objet peut parcourir, la variable
    "x_dep" qui est la position relative dans le monde de jeu et les valeurs d'affichage.
    Les knights possèdent deux rect, un pour la détection de loin et l'autre pour l'attaque.
    """
    def __init__(self,coordinates,rect):
        """
        (x,y,distance parcourue )

        """
        self.x = coordinates[0]
        self.x_dep = coordinates[0]
        self.y = coordinates[1]
        self.distancemax =  coordinates[2]
        self.rect = rect
        self.rect.height =  106                #melee Hitbox
        self.rect.width =   70
        self.run_rect =   pg.Rect((self.x_dep,self.y - 60), (360, 192)) #run hitbox

        self.run_right =    False # Variables pour les differents états
        self.run_left =     False
        self.melee_left =   False
        self.melee_right =  False
        self.idle_left =    False
        self.idle_right =   False
        self.left =         False
        self.right=         True
        self.frame = 0
        self.melee_frame = 0

    def main(self,player):
        """
        Méthode principale du knight
        """
        self.deplacement()
        self.hitbox(player.worldx,player.worldy)
        self.Knight_Attack(player)

    def hitbox(self,world_x,world_y):

        """
        Mise à jour des positions des Rects
        """
        self.rect.x = self.x_dep - world_x + 20
        self.rect.y = self.y - world_y + 26
        self.run_rect.x = self.rect.x - 150
        self.run_rect.y = self.y - world_y - 60

    def deplacement(self):
        """
        Déplacement du Knight. seule la variable "x_dep" est modifiée
        """
        if self.x_dep>self.x + self.distancemax: # si Le knight a atteint la limite droite
            if self.run_right: # Si il était en train de poursuivre le joueur (à droite)
                self.idle_right = True # Il reste sur place
            elif not self.idle_right: # si il ne restait pas sur place (à droite)
                self.left = True # Il repart vers la gauche
            if not self.melee_right: # si il n'était pas en train d'attaquer (à droite)
                self.right = False # Il arrête d'aller vers la droite
            self.run_right = False

        elif self.x_dep + 30 < self.x:  # si Le knight a atteint la limite gauche
            if self.run_left: # Si il était en train de poursuivre le joueur (à gauche)
                self.idle_left = True # Il reste sur place
            elif not self.idle_left: # si il ne restait pas sur place (à gauche)
                self.right = True # Il repart vers la droite
            if not self.melee_left: # si il n'était pas en train d'attaquer (à gauche)
                self.left = False # Il arrête d'aller vers la gauche
            self.run_left = False

        if self.right:       self.x_dep += 2 # En fonction de ce qui se passe la variable "x_dep" est modifiée
        elif self.left:      self.x_dep -= 2
        elif self.run_right: self.x_dep += 4
        elif self.run_left:  self.x_dep -= 4

    def Knight_Attack(self,player):
        """
        Se le joueur rentre dans la première hitbox la méthode "Knight_run" est appelée
        Sinon si il se rapproche encore plus la méthode "Knight_Melee" est appelée
        """

        if self.rect.colliderect(player.rect) and not player.dead:
            self.Knight_Melee(player)

        elif self.run_rect.colliderect(player.rect) and not player.dead:
            self.Knight_Run(player.x)
        else:
            self.reset()

    def Knight_Run(self,player_x):
        """
        Le knight va poursuivre le joueur en fonction de où se trouve le perso (gauche ou droite)
        jusqu' à sa limite de déplacement
        """
        if player_x < self.run_rect.x + 180: # Le perso se trouve à gauche
            if not self.idle_left: # si il n'a pas atteint la limite (gauche)
                self.run_left=True #Il Court vers la gauche
                self.run_right,self.left,self.right=False,False,False # Réinitialise les autres variables
        else:           # Le perso se trouve à droite
            if not self.idle_right: # si il n'a pas atteint la limite (droite)
                self.run_right=True # Il Court vers la droite
                self.run_left,self.left,self.right=False,False,False # Réinitialise les autres variables
        self.melee_left,self.melee_right,self.melee_frame=False,False,0 # Réinitialise les variables d'attaque

    def Knight_Melee(self,player):
        """
        Le knight va attaquer le joueur en fonction de où se trouve le perso (gauche ou droite)
        Il va tuer le joueur à partir du 18ème frame.
        """
        self.run_right,self.left,self.right,self.run_left,self.idle_right,self.idle_left = False,False,False,False,False,False # Réinitialise toutes les autres variables
        if player.x < self.rect.x + 35: # si le perso se trouve à gauche
            self.melee_left = True # Attaque à gauche
            self.melee_right = False

        elif player.x > self.rect.x + 35: # Si le perso se trouve à droite
            self.melee_left = False  # Attaque à droite
            self.melee_right = True

        if self.melee_frame == 18:
            player.dead = True # Mort du perso
            if self.melee_left: # Le knight repart dans la direction où il a attaqué
                self.left = True
            elif self.melee_right: self.right = True
            self.melee_left,self.melee_right = False,False # Réinitialise les variables d'attaque

    def reset(self):

        """
        Réinitialisation de toutes les variables de mouvement du knight.
        Quand cette méthode est appelée, à moins que le night soit en train de
        marcher vers la gauche (donc il n'est pas en collision avec le perso),
        il va repartir vers la droite.
        """
        if self.run_left or self.run_right or self.melee_left or self.melee_right:
            self.right=True
        self.run_left=False
        self.run_right=False
        self.idle_right,self.idle_left=False,False
        self.melee_left,self.melee_right=False,False
        self.melee_frame=0

def visible(objet,world_x):
    """
    Si l'objet est visible, il est affiché et les collisions sont testées.
    Sinon seules ses coordonnées dans le monde de jeu sont mises à jour.
    "world_x" est l'avancement dans le monde de jeu du personnage.
    return True si l'objet est visible, return False si l'objet n'est
    pas visible.
    """
    if - 100 < objet.X - world_x < 1300:
        return True

    else:
        objet.rect.x = objet.X - world_x
        return False

def new_time():
    """
    Réinitialise les valeurs de temps de jeu.
    """
    global start,minutes
    start = time.time()
    minutes = 0

def current_time():
    """
    Mise à jour du temps de jeu.
    """
    global start,minutes
    end= time.time()
    secondes = end-start
    if  int(secondes)==60:
        start=time.time()
        minutes+=1
    return minutes,secondes
