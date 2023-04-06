import pygame as pg
from Game_Menu import main_menu
import pickle
import Game_lvl_Editor
import Game_Moteur as Moteur
import Game_debug as GD

'''
http://www.graphic-buffet.com/about-game-graphic-buffet/licenses-terms-conditions/
https://www.gameart2d.com/license.html
https://opengameart.org/content/ui-pack; https://opengameart.org/content/faq
https://opengameart.org/content/platformer-art-complete-pack-often-updated
https://commons.wikimedia.org/wiki/File:Pentagram.png
https://appagg.com/android-games/casino/ken-club-32593810.html?hl=en
'''
"""
Module principale du jeu.
Les touches pour jouer sont:
    W, Z ou ESPACE pour sauter.
    A ou Q pour aller à gauche
    D pour aller à droite
    R pour mourir
    SHIFT + F3  pour ouvrir la fonction debug
"""
pg.init()

screen= pg.display.set_mode((1280,  720))
load= pg.image.load("images/loading.png").convert()
screen.blit(load,(325,210))
pg.display.flip()
clock = pg.time.Clock()
pg.display.set_caption("Game Minouche LMAO XD ")
bg=pg.image.load("images/bg2n.png").convert()
img_player=[pg.image.load("images/perso/Idle__000.png").convert_alpha(),pg.image.load("images/perso/Idle__001.png").convert_alpha(),pg.image.load("images/perso/Idle__002.png").convert_alpha(),pg.image.load("images/perso/Idle__003.png").convert_alpha(),pg.image.load("images/perso/Idle__004.png").convert_alpha(),pg.image.load("images/perso/Idle__005.png").convert_alpha(), pg.image.load("images/perso/Idle__006.png").convert_alpha(),pg.image.load("images/perso/Idle__007.png").convert_alpha(),pg.image.load("images/perso/Idle__008.png").convert_alpha(),pg.image.load("images/perso/Idle__009.png").convert_alpha()]
img_player_right=[pg.image.load("images/perso/Run__000.png").convert_alpha(),pg.image.load("images/perso/Run__001.png").convert_alpha(),pg.image.load("images/perso/Run__002.png").convert_alpha(),pg.image.load("images/perso/Run__003.png").convert_alpha(),pg.image.load("images/perso/Run__004.png").convert_alpha(),pg.image.load("images/perso/Run__005.png").convert_alpha(), pg.image.load("images/perso/Run__006.png").convert_alpha(),pg.image.load("images/perso/Run__007.png").convert_alpha(),pg.image.load("images/perso/Run__008.png").convert_alpha(),pg.image.load("images/perso/Run__009.png").convert_alpha()]
img_player_left,img_player_j_left=[],[]
img_player_jump=[pg.image.load("images/perso/Jump__000.png").convert_alpha(),pg.image.load("images/perso/Jump__001.png").convert_alpha(),pg.image.load("images/perso/Jump__002.png").convert_alpha(),pg.image.load("images/perso/Jump__003.png").convert_alpha(),pg.image.load("images/perso/Jump__004.png").convert_alpha(), pg.image.load("images/perso/Jump__005.png").convert_alpha(),pg.image.load("images/perso/Jump__006.png").convert_alpha(),pg.image.load("images/perso/Jump__007.png").convert_alpha(),pg.image.load("images/perso/Jump__008.png").convert_alpha(),pg.image.load("images/perso/Jump__009.png").convert_alpha()]
img_player_death=[pg.image.load("images/perso/Dead__000.png").convert_alpha(),pg.image.load("images/perso/Dead__001.png").convert_alpha(),pg.image.load("images/perso/Dead__002.png").convert_alpha(),pg.image.load("images/perso/Dead__003.png").convert_alpha(),pg.image.load("images/perso/Dead__004.png").convert_alpha(),pg.image.load("images/perso/Dead__005.png").convert_alpha(),pg.image.load("images/perso/Dead__006.png").convert_alpha(),pg.image.load("images/perso/Dead__007.png").convert_alpha(),pg.image.load("images/perso/Dead__008.png").convert_alpha(),pg.image.load("images/perso/Dead__009.png").convert_alpha()]
img_knight_idle=[pg.image.load("images/knight/Idle (1).png").convert_alpha(),pg.image.load("images/knight/Idle (2).png").convert_alpha(),pg.image.load("images/knight/Idle (3).png").convert_alpha(),pg.image.load("images/knight/Idle (4).png").convert_alpha(),pg.image.load("images/knight/Idle (5).png").convert_alpha(),pg.image.load("images/knight/Idle (6).png").convert_alpha(),pg.image.load("images/knight/Idle (7).png").convert_alpha(),pg.image.load("images/knight/Idle (8).png").convert_alpha(),pg.image.load("images/knight/Idle (9).png").convert_alpha(),pg.image.load("images/knight/Idle (10).png").convert_alpha()]
img_knight_walk=[pg.image.load("images/knight/Walk (1).png").convert_alpha(),pg.image.load("images/knight/Walk (2).png").convert_alpha(),pg.image.load("images/knight/Walk (3).png").convert_alpha(),pg.image.load("images/knight/Walk (4).png").convert_alpha(),pg.image.load("images/knight/Walk (5).png").convert_alpha(),pg.image.load("images/knight/Walk (6).png").convert_alpha(),pg.image.load("images/knight/Walk (7).png").convert_alpha(),pg.image.load("images/knight/Walk (8).png").convert_alpha(),pg.image.load("images/knight/Walk (9).png").convert_alpha(),pg.image.load("images/knight/Walk (10).png").convert_alpha()]
img_knight_run=[pg.image.load("images/knight/Run (1).png").convert_alpha(),pg.image.load("images/knight/Run (2).png").convert_alpha(),pg.image.load("images/knight/Run (3).png").convert_alpha(),pg.image.load("images/knight/Run (4).png").convert_alpha(),pg.image.load("images/knight/Run (5).png").convert_alpha(),pg.image.load("images/knight/Run (6).png").convert_alpha(),pg.image.load("images/knight/Run (7).png").convert_alpha(),pg.image.load("images/knight/Run (8).png").convert_alpha(),pg.image.load("images/knight/Run (9).png").convert_alpha(),pg.image.load("images/knight/Run (10).png").convert_alpha()]
img_knight_melee=[pg.image.load("images/knight/Attack (1).png").convert_alpha(),pg.image.load("images/knight/Attack (2).png").convert_alpha(),pg.image.load("images/knight/Attack (3).png").convert_alpha(),pg.image.load("images/knight/Attack (4).png").convert_alpha(),pg.image.load("images/knight/Attack (5).png").convert_alpha(),pg.image.load("images/knight/Attack (6).png").convert_alpha(),pg.image.load("images/knight/Attack (7).png").convert_alpha(),pg.image.load("images/knight/Attack (8).png").convert_alpha(),pg.image.load("images/knight/Attack (9).png").convert_alpha(),pg.image.load("images/knight/Attack (10).png").convert_alpha()]
img_knight_w_left,img_knight_m_left,img_knight_r_left,img_knight_i_left=[],[],[],[]
crate=pg.image.load("images/Objects/Crate.png").convert_alpha()
crate=pg.transform.scale(crate,(51,51))
img_spike= pg.image.load("images/spike.png").convert_alpha()
img_spike= pg.transform.scale(img_spike,(100,40))
img_coin=[pg.image.load("images/coin/coin1.png").convert_alpha(),pg.image.load("images/coin/coin2.png").convert_alpha(),pg.image.load("images/coin/coin3.png").convert_alpha(),pg.image.load("images/coin/coin4.png").convert_alpha()]
img_coin[0]=pg.transform.scale(img_coin[0],(50,50))
bg =pg.transform.scale(bg,(1280,1226))
menu= pg.image.load("images/menu/menu.png").convert_alpha()
menu = pg.transform.scale( menu,(100,23))
menu2 = pg.transform.scale( menu,(200,46))
New_Game = pg.image.load("images/Menu/blue_01n.png").convert_alpha()
New_Game = pg.transform.scale( New_Game,(200,48))
img_checkpoint= [pg.image.load ("images/checkpoint/flagRed.png").convert_alpha(),pg.image.load("images/checkpoint/flagRed2.png").convert_alpha(),pg.image.load("images/checkpoint/flagRedtake.png").convert_alpha()]
img_exit = pg.image.load ("images/Exit.png").convert_alpha()
img_exit = pg.transform.scale( img_exit,(50,50))

Game=0 #0: Menu , 1:New Game, 2: Continue, 3:lvl editor ; 4:fin niveau
for i in range(10):
    """
    Creation et "rescale" de toutes les images necessaire pour le jeu.
    """
    img_player[i]= pg.transform.scale(img_player[i],(80,121))
    img_player_right[i]= pg.transform.scale(img_player_right[i],(90,129) )
    img_player_left.append(pg.transform.flip( img_player_right[i], True , False))
    img_player_jump[i]= pg.transform.scale(img_player_jump[i],(90,132))
    img_player_j_left.append(pg.transform.flip( img_player_jump[i], True , False))
    img_player_death[i]=pg.transform.scale(img_player_death[i],(150,150))
    img_knight_walk[i]=pg.transform.scale(img_knight_walk[i],(116,140))
    img_knight_w_left.append(pg.transform.flip( img_knight_walk[i],True,False))
    img_knight_run[i]=pg.transform.scale(img_knight_run[i],(116,140))
    img_knight_r_left.append(pg.transform.flip( img_knight_run[i],True,False))
    img_knight_melee[i]=pg.transform.scale(img_knight_melee[i],(116,140))
    img_knight_m_left.append(pg.transform.flip( img_knight_melee[i],True,False))
    img_knight_idle[i]= pg.transform.scale(img_knight_idle[i],(116,140))
    img_knight_i_left.append(pg.transform.flip( img_knight_idle[i],True,False))
    if i<3:
        img_checkpoint[i]=pg.transform.scale(img_checkpoint[i],(50,50))
for i in range(1,4):
    img_coin[4-i]=pg.transform.scale(img_coin[4-i],(50,50))
    img_coin.append(pg.transform.flip( img_coin[4-i], True , False))
bg1x,bg2x,bgy=[0],[1280],[-506] # Position initiale des backgrounds
dep_bg_left,dep_bg_right,dep_bg_top,dep_bg_bot=False,False,False,False

def deplacement_bg():
    """
    Déplacement des backgrounds
    """
    global dep_bg_right,dep_bg_left,dep_bg_right,dep_bg_top,dep_bg_bot

    if player.x > 650:   # le bg ne se déplace que si le perso s'approche des bords
        dep_bg_left = True
    elif  player.x < 100:
        dep_bg_right = True
    else: dep_bg_left,dep_bg_right = False,False

    if  player.y < 100 and bgy[0] < -6:
        dep_bg_top = True

    elif 350 < player.y < 410 and bgy[0] > -506:
        dep_bg_bot = True

    else: dep_bg_top,dep_bg_bot = False,False


    if bg1x[0]==-1270       : bg1x[0] = 1280 #Mouvement cyclique du background
    elif bg1x[0] == 1290    : bg1x[0] = -1270
    if bg2x[0] == 1290      : bg2x[0] = -1270
    elif bg2x[0] == -1270   : bg2x[0] = 1280


def affichage():
    """
    Affichage des deux backgrounds
    """
    screen.blit(bg,(bg1x[0],bgy[0]))
    screen.blit(bg,(bg2x[0],bgy[0]))

def Test_Bouton_Menu():
    """
    Test si le bouton pour revenir au Menu est appuyé
    """
    global Game
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 :
        pos=event.pos
        try:
            if rect_menu.collidepoint(pos) :
                Game=0
        except:pass

def affichage_infos():
    """
    Affichage des pièces et du temps de jeu.
    """
    global minutes,secondes
    if Game!=4: #Si la partie est finie, le temps n'est pas mis à jour
        minutes,secondes= Moteur.current_time()
    font= pg.font.SysFont("Arial", 25)
    Nombre_coin="Coins: "+ str(player.coin) + "/" +str(len(liste_coin))
    temps= "Time: 0" + str(minutes) + ":" + str(round(secondes,4))
    texte_coin = font.render( Nombre_coin, True, (139,0,0))
    texte_temps = font.render( temps, True, (139,0,0))
    screen.blit(texte_coin,(5,50))
    screen.blit(texte_temps,(5,5))

def affichage_player():
    """
    Fonction principale de l'affichage du perso
    """
    if player.frame_count > 10 :
        player.frame_count = 0

    affichage_player_walk()
    affichage_player_jump()

def affichage_player_walk():
    """
    Affichage du perso quand il reste sur place et quand il marche
    """
    if not player.left and not player.right and not player.jump :
        if player.idle_frame == 50 : player.idle_frame = 0
        screen.blit(img_player[player.idle_frame//5],(player.x , player.y ))
        player.idle_frame += 1
    elif player.left  and not player.jump:
        screen.blit(img_player_left[player.frame_count//3],(player.x , player.y))
        player.frame_count += 1
    elif player.right and not player.jump:
        screen.blit(img_player_right[player.frame_count//3],(player.x , player.y))
        player.frame_count += 1

def affichage_player_jump():
    """
    Affichage du perso quand il saute
    """
    if player.jump and player.left:
         try:
            screen.blit( img_player_j_left[player.jump_count//7],(player.x,player.y))
            player.frame_count+=1
         except:
            screen.blit( img_player_j_left[9],(player.x,player.y))
    elif player.jump and not player.left:
        try:
            screen.blit( img_player_jump[player.jump_count//7],(player.x , player.y))
            player.frame_count += 1
        except:
            screen.blit( img_player_jump[9],(player.x,player.y))


def affichage_player_death():
    """
    Affichage du perso quand il meurt
    """
    if player.death_frame_count < 50 :
        screen.blit(img_player_death[player.death_frame_count//5],(player.x , player.y))
        player.death_frame_count += 1
        return False
    else:
        return True

def affichage_objet(image,x,y):
    """
    Affiche une image aux coordonnées données en paramètre.
    """
    screen.blit(image,(x,y))

def affichage_coin(coin):
    """
    Affichage de la pièce passée en paramètre
    """
    if coin.frame<49:
        screen.blit(img_coin[coin.frame//7],(coin.rect.x,coin.rect.y))
        coin.frame+=1
    else:
        coin.frame=0
        screen.blit(img_coin[0],(coin.rect.x,coin.rect.y))

def affichage_flag(flag):
    """
    Affichage du drapeau passé en paramètre
    """
    if flag.frame<30 and not flag.taked:
        screen.blit(img_checkpoint[flag.frame//15],(flag.rect.x,flag.rect.y))
        flag.frame+=1
    elif not flag.taked:
        screen.blit(img_checkpoint[0],(flag.rect.x,flag.rect.y))
        flag.frame=0
    if flag.taked:
        screen.blit(img_checkpoint[2],(flag.rect.x,flag.rect.y))

def affichage_knight(knight):
    """
    Affichage de l'ennemi
    """
    if knight.frame==39: knight.frame = 0
    elif knight.melee_frame==39: knight.melee_frame = 0
    if knight.right:
        screen.blit(img_knight_walk[knight.frame//4],(knight.rect.x - 23 , knight.rect.y - 26))
    elif knight.left:
        screen.blit(img_knight_w_left[knight.frame//4],(knight.rect.x - 27 , knight.rect.y - 26))
    elif knight.run_right:
        screen.blit(img_knight_run[knight.frame//4],(knight.rect.x - 25 , knight.rect.y - 26))
    elif knight.run_left:
        screen.blit(img_knight_r_left[knight.frame//4],(knight.rect.x - 25 , knight.rect.y - 26))
    elif knight.idle_right:
        screen.blit(img_knight_idle[knight.frame//4],(knight.rect.x - 25 , knight.rect.y - 24))
    elif knight.idle_left:
        screen.blit(img_knight_i_left[knight.frame//4],(knight.rect.x - 25 , knight.rect.y - 24))
    elif knight.melee_right:
        screen.blit(img_knight_melee[knight.melee_frame//4] , (knight.rect.x - 25 , knight.rect.y - 26))
        knight.melee_frame += 1
    elif knight.melee_left:
        screen.blit(img_knight_m_left[knight.melee_frame//4] , (knight.rect.x - 25 , knight.rect.y - 26))
        knight.melee_frame += 1
    knight.frame +=1

def Affichage_Fin():
    """
    Affichage de la fin avec le Top 5 des meilleurs temps, le bouton pour rejouer
    et le bouton pour revenir au menu
    """
    global Game
    font = pg.font.SysFont("Arial", 50)
    texte_Top5_title = font.render("TOP 5:", True, (139,0,0))
    font2 = pg.font.SysFont("Arial", 40)
    top1 = "1. "+ str(high_score_list[0])
    top2 = "2. "+ str(high_score_list[1])
    top3 = "3. "+ str(high_score_list[2])
    top4 = "4. "+ str(high_score_list[3])
    top5 = "5. "+ str(high_score_list[4])
    texte_Top1 = font.render(top1, True, (139,0,0))
    texte_Top2 = font.render(top2, True, (139,0,0))
    texte_Top3 = font.render(top3, True, (139,0,0))
    texte_Top4 = font.render(top4, True, (139,0,0))
    texte_Top5 = font.render(top5, True, (139,0,0))

    screen.blit( texte_Top5_title,(575,100))
    screen.blit( texte_Top1,(525,150))
    screen.blit( texte_Top2,(525,200))
    screen.blit( texte_Top3,(525,250))
    screen.blit( texte_Top4,(525,300))
    screen.blit( texte_Top5,(525,350))
    Test_Bouton_Menu()
    rect_menu2 =  screen.blit(menu2,( 260,450))
    rect_New = screen.blit(New_Game,( 800,450))
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        pos=event.pos
        if rect_menu2.collidepoint(pos):
            Game=0
        elif rect_New.collidepoint(pos):
            Game=1
def Refresh_HighScore():
    """
    Mise à jour de la liste des meilleurs temps. Si le temps de cette run est
    présent dans la liste return True
    """
    global New_Best_Score,high_score_list
    final_time = str(minutes) + ":" + str(round(secondes,4))
    high_score_list = info_lvl[0]
    high_score_list.append(final_time)
    high_score_list.sort()
    del high_score_list[5]
    if final_time in high_score_list:
        New_Best_Score = True
    update_lvl()

def new():

    """
    Cette fonction est appellée lorsque une nouvelle partie est lancée ("New Game").
    La position initiale du perso et toutes les listes d'objets sont réinitialisées.
    Appeller la mort du perso pour un seul tour de boucle (51) sert à
    réinitialiser toutes les autres variables.
    """
    global player,liste_obstacle,liste_coin,liste_knight,liste_spike,liste_flag,fin
    liste_obstacle,liste_coin,liste_flag,liste_spike,liste_knight,fin=[],[],[],[],[],[]
    player.lastcheckpoint= (110,450,0,0,-506)
    player.coin=0
    player.death_frame_count=51
    player.death(bgy)

def lvl_open():

    """
    Le fichier du niveau est ouvert et toutes les coordonnées des objets sont
    sorties.
    La fonction pour créer les objets est ensuite appelée.
    """
    global info_lvl
    fichier_à_ouvrir = "./Niveaux/"+level_name+".pickle"
    file = open(fichier_à_ouvrir,"rb")
    coo_obstacle = pickle.load(file)
    coo_coin = pickle.load(file)
    coo_spike = pickle.load(file)
    coo_flag = pickle.load(file)
    coo_knight = pickle.load(file)
    coo_exit = pickle.load(file)
    info_lvl = pickle.load(file)
    file.close()
    creation_objets(coo_obstacle,coo_coin,coo_spike,coo_flag,coo_knight,coo_exit)

def update_lvl():
    """
    Le fichier est réécrit avec le nouveau meilleur score
    """
    coo = [0]*6
    fichier_à_ouvrir = "./Niveaux/"+level_name+".pickle"
    with open(fichier_à_ouvrir,"rb") as file:
        for i in range(6):
            coo[i]=pickle.load(file)
    with open(fichier_à_ouvrir,"wb") as file:
        for i in range(6):
            pickle.dump(coo[i],file)
        pickle.dump([high_score_list],file)


def creation_objets(coo_obstacle,coo_coin,coo_spike,coo_flag,coo_knight,coo_exit):

    """
    Création de chaque objet présent dans le niveau.
    """
    for coordonnées in coo_obstacle:
        liste_obstacle.append(Moteur.obstacle(coordonnées,crate.get_rect()))

    for coordonnées in coo_coin:
        liste_coin.append(Moteur.coin(coordonnées,img_coin[0].get_rect()))

    for coordonnées in coo_spike:
        liste_spike.append(Moteur.spike(coordonnées,img_spike.get_rect()))

    for coordonnées in coo_flag:
        liste_flag.append(Moteur.flag(coordonnées,img_checkpoint[0].get_rect()))

    for coordonnées in coo_knight:
        liste_knight.append(Moteur.knight(coordonnées,img_knight_walk[0].get_rect()))

    for coordonnées in coo_exit:
        fin.append( Moteur.exit( coordonnées , img_exit.get_rect()))

def main_obstacles():

    """
    Pour chaque objet dans chaque liste, sa visibilité dans la fenêtre de jeu
    est testée. Si l'objet est visible, il est donc affiché et sa méthode
    principale est appelée.
    """
    global Game
    world_x=player.worldx
    for obstacle in liste_obstacle:
        if Moteur.visible(obstacle,world_x):
            affichage_objet(crate,obstacle.rect.x,obstacle.rect.y)
            obstacle.main(player)

    for coin in liste_coin:
        if Moteur.visible(coin,world_x) and not coin.collision:
            affichage_coin(coin)
            coin.main(player)

    for spike in liste_spike:
        if Moteur.visible(spike,world_x):
            affichage_objet(img_spike,spike.rect.x,spike.rect.y)
            spike.main(player)

    for flag in liste_flag:
        if Moteur.visible(flag,world_x):
            affichage_flag(flag)
            flag.main(player,bgy[0])

    for knight in liste_knight:
        affichage_knight(knight)
        knight.main(player)
        if player.debug:
            GD.affichage_hitbox_knight(screen,knight)
    for ex in fin:
        if Moteur.visible(ex, world_x):
            affichage_objet(img_exit,ex.rect.x,ex.rect.y)
            if ex.main(player):
                Refresh_HighScore()
                Game= 4


def main():
    """
    Fonction principale du jeu. Le jeu est divisé en quatre parties.
    Le menu
    Le jeu principal
    Le lvl Editor
    Le menu tkinter pour changer de niveau
    """
    global Game,rect_menu,level_name
    if Game == 0: #Menu
        Game,level_name = main_menu()

    elif Game == 1: #Lance nouvelle partie
        new()
        lvl_open()
        Moteur.new_time()
        Game=2

    elif Game == 2: #Jeu principal
        affichage()
        Test_Bouton_Menu()
        if player.dead:
            if affichage_player_death():
                player.death(bgy)
                affichage()
        else:
            affichage_player()
            player.deplacement(bg1x,bg2x,dep_bg_right,dep_bg_left)
            player.hitbox()
            player._jump(bgy,dep_bg_top,dep_bg_bot)

        main_obstacles()
        deplacement_bg()
        rect_menu = screen.blit(menu,(1179,1))
        affichage_infos()
        if player.debug:
            GD.affichage_hitbox_player(screen,player)
            GD.affichage_coordonees(screen,player.worldx,player.worldy,clock.get_fps())

    elif Game==3: # initialise Lvl Editor
        Game_lvl_Editor.initialise(level_name)
        Game=3.5

    elif Game == 3.5: # Lvl editor
        Game_lvl_Editor.lvl_Editor_main()
        if Game_lvl_Editor.return_menu(event):
            Game = 0
    elif Game == 4: # Fin du jeu
        Affichage_Fin()



"""
DEBUT ALGO

"""
player= Moteur.Player(110,450,img_player[0].get_rect())
liste_obstacle,liste_coin,liste_spike,liste_knight=[],[],[],[]



run= True
while run:
    for event in pg.event.get():
         if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            if Game==3.5:
                    Game_lvl_Editor.lvl_save()
            run=False
    main()

    clock.tick(50)
    pg.display.flip()
pg.quit()