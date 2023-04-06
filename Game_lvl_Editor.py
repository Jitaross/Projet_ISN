import pygame as pg
import pickle

screen= pg.display.set_mode((1280,  720))
bg=pg.image.load("images/bg2n.png").convert()
bg =pg.transform.scale(bg,(1280,1226))
menu= pg.image.load("images/menu/menu.png").convert_alpha()
menu = pg.transform.scale( menu,(100,23))
img_line =pg.image.load("images/tic.png").convert_alpha()
img_line=pg.transform.scale(img_line,(50,50))
img_crate=pg.image.load("images/Objects/Crate.png").convert_alpha()
img_crate=pg.transform.scale(img_crate,(51,51))
img_coin=pg.image.load("images/coin/coin1.png").convert_alpha()
img_coin=pg.transform.scale(img_coin,(50,50))
img_spike=pg.image.load("images/spike.png").convert_alpha()
img_spike= pg.transform.scale(img_spike,(100,40))
img_gomme=pg.image.load("images/gomme.png").convert_alpha()
img_gomme= pg.transform.scale(img_gomme,(80,50))
img_flag=pg.image.load("images/checkpoint/flagRed.png").convert_alpha()
img_flag= pg.transform.scale(img_flag,(50,50))
img_knight=pg.image.load("images/knight/Idle (1).png").convert_alpha()
img_knight=pg.transform.scale(img_knight,(50,50))
img_exit = pg.image.load("images/Exit.png").convert_alpha()
img_exit = pg.transform.scale( img_exit,(50,50))

draw_line,place_crate,place_coin,place_spike,gomme,place_checkpoint,place_knight,place_exit=False,False,False,False,False,False,False,False
knight_click=0
click_counter=0

knight_coordinates,knight_distances=[],[]
knight_height_difference=82


def affichage():
    """
    Affichage de tous les objets présents dans le niveau, la variable d'avancement
    dans le monde de jeu est enlevée pour calculer les coordonnées d' affichage
    """

    if draw_line:
        for i in range(1,27):
            pg.draw.line(screen, (0,0,0), (50*i,0), (50*i,720))
        for i in range(1, 16):
            pg.draw.line(screen,(0,0,0),  (0,50*i-30),(1280,50*i-30))
    for obstacle in liste_obstacle:
        screen.blit(img_crate,(obstacle[0]+background.x , obstacle[1]-background.y))
    for coin in liste_coin:
        screen.blit(img_coin,(coin[0]+background.x , coin[1]-background.y))
    for spike in liste_spike:
        screen.blit(img_spike,(spike[0]+background.x , spike[1]-background.y))
    for flag in liste_flag:
        screen.blit(img_flag,(flag[0]+background.x,flag[1]-background.y))
    for fin in liste_fin:
        screen.blit(img_exit,(fin[0]+background.x , fin[1]-background.y))
    for i,y in zip(knight_coordinates,knight_distances):
        screen.blit(img_knight,(i[0]+background.x,i[1]-background.y+knight_height_difference))
        pg.draw.line(screen,(255,0,0), (i[0]+background.x+25,i[1]-background.y+knight_height_difference),(i[0]+background.x+y+25,i[1]-background.y+knight_height_difference) )

    Affichage_Option()

def Affichage_Option():
    """
    Affichage du menu de tous les objets du jeu
    """

    global rect_crate,rect_line,rect_coin,rect_spike,rect_gomme,rect_flag,rect_knight,rect_exit

    rect_crate  = screen.blit(img_crate , (200,0))
    rect_line   = screen.blit(img_line , ( 100,0))
    rect_coin   = screen.blit(img_coin , (300,0))
    rect_spike  = screen.blit(img_spike , (400,0))
    rect_gomme  = screen.blit(img_gomme, (1050,1))
    rect_flag   = screen.blit(img_flag , (550,0))
    rect_knight = screen.blit(img_knight , (650,0))
    rect_exit   = screen.blit(img_exit , (750,0))

def Choisie_Objet_A_Place():
    """
    Test si un des objets à placer est appuyé, la variable
    correspondante est True et toutes les autres False.
    "Click_counter" sert à appuyer une seule fois
    """
    global place_crate,draw_line,click_counter,place_coin,place_spike,gomme,place_checkpoint,place_knight,knight_click,place_exit
    if pg.mouse.get_pressed()[0]:
        pos = pg.mouse.get_pos()
        if rect_line.collidepoint (pos) and click_counter==0:
            draw_line=not draw_line
            click_counter+=1
        elif rect_crate.collidepoint(pos) and click_counter==0:
            place_crate= True
            place_coin,place_spike,gomme,place_checkpoint,place_knight,place_exit=False,False,False,False,False,False
            click_counter+=1
        elif rect_coin.collidepoint(pos) and click_counter==0:
            place_coin= True
            place_crate,place_spike,gomme,place_checkpoint,place_knight,place_exit=False,False,False,False,False,False
            click_counter+=1
        elif rect_spike.collidepoint(pos) and click_counter==0:
            place_spike=True
            place_coin,place_crate,place_checkpoint,gomme,place_knight,place_exit= False,False,False,False,False,False
            click_counter+=1
        elif rect_gomme.collidepoint(pos) and click_counter==0:
            gomme=True
            place_spike,place_coin,place_crate,place_checkpoint,place_knight,place_exit=False,False,False,False,False,False
            click_counter+=1
        elif rect_flag.collidepoint(pos) and click_counter==0:
            place_checkpoint=True
            place_spike,place_coin,place_crate,gomme,place_knight,place_exit=False,False,False,False,False,False
            click_counter+=1
        elif rect_knight.collidepoint(pos) and click_counter==0:
            place_knight=True
            place_spike,place_coin,place_crate,gomme,place_checkpoint,place_exit=False,False,False,False,False,False

        elif rect_exit.collidepoint(pos) and click_counter==0:
            place_exit = True
            click_counter+=1
    elif pg.mouse.get_pressed()[2]: # Si la touche gauche de la souris est appuyée, toutes les variables sont réinitialisées
        knight_click=0
        place_crate,place_coin,place_spike,gomme,place_checkpoint,place_knight,place_exit=False,False,False,False,False,False,False
    else:click_counter=0

def Place_objets():
    """
    Fonction pour afficher l'objet qui doit être placé.
    """
    pos= pg.mouse.get_pos() # Position souris
    if (pos[1]<570 or background.y<-100) and pos[1]>70: # On ne peut pas placer d' objets au dessous du sol.
        a_pos = (pos[0]//50*50,(pos[1]+30)//50*50-30) # Coordonnées d'affichage de l objet à placer
        if place_crate:
            screen.blit(img_crate,(a_pos))
            Add_at_List(liste_obstacle,a_pos)

        elif place_coin:
            screen.blit(img_coin,(a_pos))
            Add_at_List(liste_coin,a_pos)

        elif place_spike:
            a_pos=(pos[0]//50*50,(pos[1]+30)//50*50-20) # L' image des piques est plus petite
            screen.blit(img_spike,(a_pos))
            Add_at_List(liste_spike,a_pos)

        elif place_checkpoint:
            screen.blit(img_flag,(a_pos))
            Add_at_List(liste_flag,a_pos)

        elif place_exit:
            screen.blit(img_exit,(a_pos))
            if pg.mouse.get_pressed()[0]:
                if len(liste_fin)==0:
                    Add_at_List(liste_fin,a_pos)

        elif place_knight:
            Place_knight(a_pos)

        elif gomme:
            a_pos=(pos[0]//50*50+5,(pos[1]+30)//50*50-35) # Position d' affichage de la gomme
            screen.blit(img_gomme,(a_pos)) # Affichage Gomme
            Utilise_Gomme(pos)


def Add_at_List(liste,position):
    """
    Rajoute à la liste donnée en paramètre les coordonnées "position".
    Les coordonnées de l'avancement dans le monde de jeu sont rajoutéex pour avoir
    les coordonnées absolues.
    Les coordonnées ne sont rajoutées que si elles ne sont pas déjà présentes dans la liste
    """
    Position_Absolue = (position[0]-background.x,position[1]+background.y)
    if pg.mouse.get_pressed()[0]:
        if liste.count(Position_Absolue)==0:
            liste.append(Position_Absolue)



def Utilise_Gomme(pos):
    """
    Si possible, donc si il y a un objet à ces coordonnées, il est éliminé de la liste.
    """
    efface_pos=((pos[0]//50*50)-background.x,((pos[1]+30)//50*50-30)+background.y) # Position de l'objet à effacer.
    if pg.mouse.get_pressed()[0] :
        try: del liste_obstacle[liste_obstacle.index(efface_pos)]
        except: pass
        try: del liste_coin[liste_coin.index(efface_pos)]
        except: pass
        try: del liste_spike[liste_spike.index((efface_pos[0],efface_pos[1]+10))] # (L'image des piques n'a pas la meme grandeur)
        except: pass
        try: del liste_flag[liste_flag.index(efface_pos)]
        except:pass
        try: del liste_fin[liste_fin.index(efface_pos)]
        except: pass
        try:
            effacer_index=knight_coordinates.index((efface_pos[0],efface_pos[1]-knight_height_difference))
            del knight_coordinates[effacer_index]
            del knight_distances[effacer_index]
        except:pass



def Place_knight(Postions_Affichage ):
    """
    Le positionnement des ennemis est divisé en deux parties.
    La première partie ("knight_click=0") détermine la position initiale de l'ennemi.

    La deuxième partie ("knight_click=1") détermine la distance parcourue par
    l' ennemi à partir de la position initiale.

    """
    global knight_click,click_counter
    Position_Absolue = (Postions_Affichage[0]-background.x,Postions_Affichage[1]+background.y-knight_height_difference ) # Calcul de la postion absolue. L'ennemi est plus grand que 50 pixels

    if knight_click==0 or click_counter>0:
        screen.blit(img_knight,(Postions_Affichage)) # Affichage knight

        if pg.mouse.get_pressed()[0]:
            if  click_counter==0: # Pour le rajouter une seule fois à la liste
                knight_coordinates.append((Position_Absolue[0],Position_Absolue[1])) #Rajoute les coordonnées à la liste des ennemis
                knight_click+=1
            click_counter+=1
        else:
            click_counter=0 # Réinitialise variable

    elif knight_click==1:
        if knight_coordinates[-1][0] + background.x < Postions_Affichage[0]+25 and knight_coordinates[-1][1]+knight_height_difference-background.y==Postions_Affichage[1]: # Le trajet de l'eenemi doit être forcément vers la droite et sur la même ligne
            pg.draw.line(screen,(255,0,0), (knight_coordinates[-1][0]+background.x,knight_coordinates[-1][1]+knight_height_difference-background.y+25),(Postions_Affichage[0]+25,Postions_Affichage[1]+25)) # Dessin de la trajectoire

            if pg.mouse.get_pressed()[0]:
                knight_distances.append(Position_Absolue[0]-knight_coordinates[-1][0]) # Rajoute la distance parcourue par l' ennemi
                knight_click=0 # Réinitialise variable
                click_counter=1
def lvl_save():
    """
    Sauvergarde le niveau dans le fichier .pickle
    """
    knight1=[] # Réinitialise variable
    file=open(niveau,"wb")
    pickle.dump(liste_obstacle,file)
    pickle.dump(liste_coin,file)
    pickle.dump(liste_spike,file)
    pickle.dump(liste_flag,file)
    for i,y in zip(knight_coordinates,knight_distances):
        knight1.append((i[0],i[1],y))
    pickle.dump(knight1,file)
    pickle.dump(liste_fin,file)
    pickle.dump(lvl_info,file)
    file.close()

def lvl_open():
    """
    Ouvre Le niveau du fichier .pickle.
    Création de toutes les listes avec les coordonnées
    """
    global liste_obstacle,liste_coin,liste_spike,liste_flag,knight_distances,knight_coordinates,liste_fin,lvl_info
    knight_coordinates,knight_distances=[],[] # Réinitialisation des coordonnées
    file=open(niveau,"rb")
    liste_obstacle=pickle.load(file)
    liste_coin=pickle.load(file)
    liste_spike=pickle.load(file)
    liste_flag= pickle.load(file)
    knight1= pickle.load(file)
    liste_fin = pickle.load(file)
    lvl_info = pickle.load(file)
    file.close()
    for i in knight1: # La position des knights est séparée de leurs distances
        knight_coordinates.append((i[0],i[1]))
        knight_distances.append(i[2])

class c_background:
    """
    Class pour gérer les backgrounds
    """
    def __init__(self):
        self.x=0
        self.y=0
        self.bgy= -506
        self.left=False
        self.right=False
        self.top=False
        self.bot=False

    def main(self):
        screen.blit(bg,(0,self.bgy))
        self.deplacement()
        self.deplacement_bg()

    def deplacement(self):
        """
        Déplacement du background
        """
        k=pg.key.get_pressed()
        if (k[pg.K_w] or k[pg.K_z]): self.top=True
        elif k[pg.K_s]: self.bot=True
        else: self.top=False;self.bot=False
        if (k[pg.K_a] or k[pg.K_q]): self.left=True
        elif k[pg.K_d]: self.right=True
        else: self.left=False;self.right=False

    def deplacement_bg(self):
        if self.top and self.y>-480:
            self.y-=50
            self.bgy+=50
        elif  self.bot and self.y<0:
            self.y+=50
            self.bgy-=50

        if  self.left:
            self.x+=50
        elif self.right:
            self.x-=50

def initialise(level_name):
    """
    Initialise le lvl editor
    """
    global background,niveau
    niveau= "./Niveaux/"+level_name+".pickle"
    lvl_open() # Ouvre le niveau selectionné
    background=c_background() # Création de l' instance background

def lvl_Editor_main():
    """
    Fonction principale du lvl editor
    """
    background.main()
    affichage()
    Choisie_Objet_A_Place()
    Place_objets()

def return_menu(event):
    """
    Bouton pour revenir au menu
    """
    rect_menu= screen.blit(menu,(1179,1))
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 :
        pos=event.pos
        if rect_menu.collidepoint(pos):
            lvl_save() # Sauvegarde du niveau
            return True
    return False