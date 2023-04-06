import pygame as pg
from tkinter import *
from tkinter import messagebox
from tkinter import _setit as tks
import os
import pickle

screen= pg.display.set_mode((1280,  720))
bg=pg.image.load("images/bg2.png").convert()
bg =pg.transform.scale(bg,(1280,720))
buttonblue= [pg.image.load("images/Menu/blue_00n.png").convert_alpha(),pg.image.load("images/Menu/blue_01n.png").convert_alpha()]
buttonred= [pg.image.load("images/Menu/red_11n.png").convert_alpha(),pg.image.load("images/Menu/red_12n.png").convert_alpha()]
img_lvl = [pg.image.load("images/Menu/blue_00l.png").convert_alpha(),pg.image.load("images/Menu/blue_01l.png").convert_alpha()]
img_para = [pg.image.load("images/Menu/red_para0.png").convert_alpha(),pg.image.load("images/Menu/red_para1.png").convert_alpha()]
perso=[ pg.image.load("images/perso/Idle__000.png").convert_alpha()]
perso[0]= pg.transform.scale(perso[0],(80,121))
perso.append( pg.transform.flip( perso[0] , True , False))

for i in range(2):
    buttonblue[i]= pg.transform.scale(buttonblue[i],(350,90))
    buttonred[i]= pg.transform.scale(buttonred[i],(350,90))
    img_lvl[i]= pg.transform.scale(img_lvl[i],(350,90))
    img_para[i]= pg.transform.scale(img_para[i],(90,90))

#Variables pour savoir si on appuie sur un bouton
New_Game_pressed,Contiue_pressed,lvl_pressed,para_pressed=False,False,False,False


def main_menu():
    """
    Fonction principale du Menu
    "Game" est la partie du jeu à exécuter
    "level" correspond au nom du niveau choisi.
    """
    click_bouton()
    Game,level= affichage()
    return Game,level


def affichage():
    """
    Affichage général du menu.
    Une première image de chaque bouton est affichée s'il n'est pas cliqué sinon
    une autre image est affichée pour simuler une animation.
    La première valeur retournée correspond à la partie du jeu à exécuter:
        0: Menu principal
        1: Nouvelle partie
        2: Continue la partie
        3: Modifie le niveau
    level correspond au nom du niveau choisi.
    """
    global rectnew,rectcontinue,rectlvl,rect_para,New_Game_pressed,Contiue_pressed,lvl_pressed,para_pressed
    screen.blit(bg,(0,0))
    screen.blit(perso[0],(180,450))
    screen.blit(perso[1],(1000,450))

    if not New_Game_pressed:
        rectnew = screen.blit(buttonblue[0],(465,250))
    else:
        rectnew = screen.blit(buttonblue[1],(465,250))
        New_Game_pressed = False
        return 1,level

    if not Contiue_pressed:
        rectcontinue = screen.blit(buttonred[0],(465,400))
    else:
        rectcontinue = screen.blit(buttonred[1],(465,400))
        Contiue_pressed=False
        return 0,level

    if not lvl_pressed:
        rectlvl= screen.blit(img_lvl[0], (465,550))
    else:
        rectlvl= screen.blit(img_lvl[1], (465,550))
        lvl_pressed=False
        return 3,level

    if  not para_pressed:
        rect_para=screen.blit(img_para[0],(850,550))
    else:
        rect_para=screen.blit(img_para[1],(850,550))
        pg.display.flip()
        mainlooptkinter()
        para_pressed=False
    return 0,level

def click_bouton():

    """
    Si les coordonnées du click gauche de la souris correspondent au rect de
    l'image du bouton, sa variable "pressed" est égale à True.
    Sinon toutes les variables sont réinitialisées sur False.
    """
    global New_Game_pressed,Contiue_pressed,lvl_pressed,para_pressed
    if pg.mouse.get_pressed()[0]:
        pos=pg.mouse.get_pos()
        if rectnew.collidepoint(pos):
            New_Game_pressed = True
        elif rectcontinue.collidepoint(pos):
            Contiue_pressed = True
        elif rectlvl.collidepoint(pos):
            lvl_pressed = True
        elif rect_para.collidepoint(pos):
            para_pressed = True
    else:
        New_Game_pressed,Contiue_pressed,lvl_pressed,para_pressed = False,False,False,False

def mainlooptkinter():
    global f,valeur,txt_nouveau,niveaux_disponibles,txt_niveau2
    f= Tk()

    # Affiche le niveau qui est chargé
    txt_niveau=Label(f,text="Niveau Chargé:",font= ("Arial",18))
    txt_niveau.grid(row=0,column=0,pady=10)
    txt_niveau2=Label(f,text=level,font= ("Arial",18))
    txt_niveau2.grid(row=0,columnspan=3)

    # Valeur par défaut du Menu à option
    valeur = StringVar(f)
    valeur.set(level)

    # Menu à option pour changer de niveau
    text_menu=Label(f,text="Changer de niveau:",font= ("Arial",18))
    text_menu.grid(row=1,column=0)
    niveaux_disponibles= OptionMenu(f,valeur,*liste_niveaux)
    niveaux_disponibles.grid(row=1,column=1)

    # Efface le niveau
    bouton_effacer= Button(f, text="Effacer", font=("Arial",18), command=effacer_niveau)
    bouton_effacer.grid(row=1,column=2,pady=10)

    # Crée un nouveau niveau
    txt=Label(f,text="Créer un nouveau niveau:",font= ("Arial",15))
    txt.grid(row=2,column=0,pady=10)
    txt_nouveau= Entry(f,font=("Arial",15 ) )
    txt_nouveau.grid(row=2,column=1)
    bouton_nouveau= Button(f, text=" Créer", font=("Arial",15),width=10, command=nouveau_niveau)
    bouton_nouveau.grid(row=2,column=2)

    # Bouton pour fermer la fenêtre tkinter et sauvegarder le niveau choisi
    bouton_save= Button(f, text=" Ok", font=("Arial",18),width=40, command=save)
    bouton_save.grid(row=3,columnspan=3,pady=10)
    mainloop()

def save():
    """
    Sauvegarde le nom du niveau choisi. Si aucun niveau n'est sélectionné,
    un message d'erreur s'affiche. Sinon la fenêtre se ferme normalement.
    """
    global level
    if valeur.get()=="": #
        messagebox.showerror("Erreur", "Aucun niveau sélectionné!")
    else:
        level=valeur.get() # Prend le nom du niveau choisi
        txt_niveau2["text"]=level
        f.destroy()

def nouveau_niveau():
    """
    Création du fichier .pickle du nouveau niveau, mise à jour des niveaux
    disponibles et du menu.
    """
    nom_nouveau= txt_nouveau.get()
    txt_nouveau.delete(0,END)

    file=open("./Niveaux/"+nom_nouveau+".pickle","wb")
    for i in range(6):
        pickle.dump([],file)
    pickle.dump([["9999","9999","9999","9999","9999"]],file)
    file.close()
    import_niveaux()
    refresh_menu()

def refresh_menu():
    """
    Mise à jour du menu à options. Toutes les options sont effacées, ensuite
    chaque niveau de la nouvelle liste est remis comme option.
    """
    global valeur
    valeur.set("")
    niveaux_disponibles['menu'].delete(0, 'end')
    for niveau in liste_niveaux:
        niveaux_disponibles['menu'].add_command(label=niveau , command=tks(valeur,niveau) )

def effacer_niveau():
    """
    Efface le fichier du système , mise à jour des niveaux
    disponibles et du menu.
    """
    global level
    os.remove("./Niveaux/"+valeur.get()+".pickle")
    valeur.set("")
    level=""
    txt_niveau2["text"]=""
    import_niveaux()
    refresh_menu()

def import_niveaux():
    """
    Importe une nouvelle liste avec tous les niveaux disponibles qui sont dans
    le dossier "Niveaux".
    """
    global liste_niveaux
    liste_niveaux=[]                             # Liste des niveaux disponibles
    for niveau in os.listdir("./Niveaux"):       # retourne une liste avec les noms des fichiers présents dans le dossier
        nom,extension=niveau.split(".")          # Sépare le nom du fichier de l'extension
        liste_niveaux.append(nom)                # Rajoute le nom à la liste des niveaux disponibles

def Fin_niveau():
    pass

def main():
    '''
    Cette fonction est appellée uniquement si le module est exécuté directement.
    '''
    affichage()
    click_bouton()

import_niveaux()
level="Niveau 1" # Niveau ouvert par defaut

if __name__=="__main__":
    """
    Cette partie n' est exécutée que si le module est exécuté directement
    """
    pg.init()
    clock = pg.time.Clock()
    pg.display.set_caption("Game Menu Preview")

    run= True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                run=False
        main()
        clock.tick(50)
        pg.display.flip()
    pg.quit()