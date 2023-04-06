import pygame as pg
pg.font.init()
font = pg.font.SysFont("comicsansms", 14)
font2 =  pg.font.SysFont("comicsansms", 25)
RED = (255,0,0)
GREEN = (0,255,0)
couleur_idle,couleur_walk,couleur_jump,couleur_dead = RED,RED,RED,RED
couleur_k_idle,couleur_k_walk,couleur_k_run,couleur_k_melee = RED,RED,RED,RED
"""
Ce Module contient des informations supplémentaires qui peuvent être affichées avec la touche SHIFT + F3
Les informations peuvent être les coordonnées du perso des ennemis et les différentes hitbox
Ces informations aident à mieux comprendre le fonctionnement du jeu
"""


def affichage_hitbox_player(screen,player):
    '''
    Les informations affichées par cette fonction sont l'hitbox du perso,
    ses coordonnéees (x,y) et ses différents états ( idle, walk, jump, death).
    '''
    maj_player(player)
    player_hit = ( player.rect.x , player.rect.y , player.rect.width , player.rect.height )
    pg.draw.rect(screen,(255,0,0) , player_hit , 2 )
    texte_idle = font.render( "Idle", True, couleur_idle)
    texte_walk = font.render( "Walk", True, couleur_walk)
    texte_jump = font.render( "Jump", True, couleur_jump)
    texte_dead = font.render( "Dead", True, couleur_dead)
    texte_x = font.render(x, True, RED)
    texte_y = font.render(y, True, RED)
    screen.blit(texte_idle,(player.rect.x + 58, player.rect.y - 2 ))
    screen.blit(texte_walk,(player.rect.x + 58, player.rect.y + 10))
    screen.blit(texte_jump,(player.rect.x + 58, player.rect.y + 20))
    screen.blit(texte_dead,(player.rect.x + 58, player.rect.y + 30))
    screen.blit(texte_x,(player.rect.x , player.rect.y - 30) )
    screen.blit(texte_y,(player.rect.x , player.rect.y - 15) )

def maj_player(player):
    '''
    Mise à jour de la couleur des états du perso.
    Rouge inactif, vert actif
    '''
    global couleur_idle,couleur_jump,couleur_walk,couleur_dead,x,y
    if player.left or player.right:
        couleur_walk = GREEN
    else: couleur_walk = RED

    if player.jump:
        couleur_jump = GREEN
    else: couleur_jump = RED

    if not player.left and not player.right and not player.jump and not player.dead:
        couleur_idle = GREEN
    else: couleur_idle = RED

    if player.dead:
        couleur_dead = GREEN
    else: couleur_dead = RED

    x="X:"+ str(player.x ) # Mise à jour de l'affichage des coordonnées
    y="Y:"+ str(player.y)

def affichage_hitbox_knight(screen,knight):
    '''
    Les informations affichées par cette fonction sont les hitbox des ennemis ,
    leurs coordonnéees (x,y et le déplacement) et leurs différents états ( idle, walk, run, attack).
    '''
    maj_knight(knight)
    coo = ["X: " + str(knight.x), "Y: " + str(knight.y), str(knight.x_dep - knight.x )]
    hit=(knight.rect.x , knight.rect.y , knight.rect.width , knight.rect.height )
    pg.draw.rect(screen,(255,0,0) , hit , 2 )
    hit=(knight.run_rect.x , knight.run_rect.y , knight.run_rect.width , knight.run_rect.height )
    pg.draw.rect(screen, (0,255,0) , hit , 2 )
    texte_walk = font.render( "Walk", True, couleur_k_walk)
    texte_run = font.render( "Run", True, couleur_k_run)
    texte_idle = font.render( "Idle", True, couleur_k_idle)
    texte_melee = font.render( "Melee", True, couleur_k_melee)
    texte_x = font.render( coo[0], True, RED)
    texte_y = font.render( coo[1], True, RED)
    texte_dep = font.render( coo[2], True, RED)
    texte_affichage_x = font.render( str( knight.rect.x), True, RED)
    texte_affichage_y = font.render( str(knight.rect.y), True, RED)
    screen.blit( texte_walk, ( knight.rect.x + 75 , knight.rect.y ))
    screen.blit( texte_run, ( knight.rect.x + 75 , knight.rect.y + 10 ))
    screen.blit( texte_idle, ( knight.rect.x + 75 , knight.rect.y + 20 ))
    screen.blit( texte_melee, ( knight.rect.x + 75 , knight.rect.y + 30 ))
    screen.blit( texte_x, ( knight.run_rect.x , knight.run_rect.y - 25 ))
    screen.blit( texte_y, ( knight.run_rect.x , knight.run_rect.y - 15 ))
    screen.blit( texte_dep, ( knight.run_rect.x + 70, knight.run_rect.y - 25 ))
    screen.blit( texte_affichage_x, ( knight.run_rect.x + 300, knight.run_rect.y - 25 ))
    screen.blit( texte_affichage_y, ( knight.run_rect.x + 300, knight.run_rect.y - 15 ))

def maj_knight(knight):
    '''
    Mise à jour de la couleur des états des ennemis.
    Rouge inactif, vert actif
    '''
    global couleur_k_idle,couleur_k_walk,couleur_k_run,couleur_k_melee
    if knight.left or knight.right:
        couleur_k_walk = GREEN
    else: couleur_k_walk = RED

    if knight.run_left or knight.run_right:
        couleur_k_run = GREEN
    else: couleur_k_run = RED

    if knight.idle_left or knight.idle_right:
        couleur_k_idle = GREEN
    else: couleur_k_idle = RED

    if knight.melee_left or knight.melee_right:
        couleur_k_melee = GREEN
    else: couleur_k_melee = RED

def affichage_coordonees(screen, world_x , world_y , fps ):
    '''
    Affichage des informations générales sur le jeu.
    L'avancement dans le monde de jeu (worldx, worldy) et les fps
    '''
    world = ["World x: "+str(world_x), "World Y: "+str(world_y), "FPS: "+str(round(fps,1)) ]
    text_x = font2.render( world[0], True, RED)
    text_y = font2.render( world[1], True, RED)
    text_fps = font2.render( world[2], True, RED)
    screen.blit(text_x , ( 5 , 95 ))
    screen.blit(text_y , ( 5 , 140 ))
    screen.blit(text_fps , ( 5 , 185 ))

