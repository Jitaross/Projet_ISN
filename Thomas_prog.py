from tkinter import *
import random

#récupération liste
def getQA():
    global question, réponse
    with open("QA.txt",'r') as file:
        qa=file.read()
        q=qa.split('\n#fin#\n')[0]
        a=qa.split('\n#fin#\n')[1]
        Q=q.split('°\n')
        A=a.split('°\n')
        question=Q
        réponse=A



#enregistrement liste
def saveQA():
    global question, réponse
    Q=question
    A=réponse
    with open('QA.txt','w') as file:
        q='°\n'.join(Q)
        a='°\n'.join(A)
        qa=q+'\n#fin#\n'+a
        file.write(qa)

getQA()

repspé=["A:Une de chaque couleur","B:Quatre violettes, quatre jaunes, quatre oranges", "C:Une violette, deux oranges, trois jaunes", "A:Une de chaque couleur"]

verif=False ## on initialise la condition verif qui nous permettra plus tard de vérifier si la réponse donée est juste ou pas
n=0
g=len(question)
quest=r

def mainThomas():
    """
    fonction principale lançant l'interface de l'énigme en fonction du nombre aléatoire obtenu
    """
    global ans,fen, quest,boutton,f, f1,spin, var, r

    fen=Tk()
    fen.title("Enigme minouche")
    fen['bg']="navajo white"
    f1=Frame(fen)
    f1['bg']="navajo white"
    f=Frame(fen)
    f['bg']="navajo white"
    f.grid(rowspan =10, columnspan =12 , padx = 5)
    f1.grid(rowspan =14, columnspan =12 , padx = 5)

    label=Label(f, text="Voici l'énigme :", font=("stencil",35 ),fg='red',bg='navajo white' )
    label.grid(row=2, column=0, pady=5)
    label1=Label(f, text="Si tu réponds correctement, le checkpoint s'activera, \n sinon tu retournes au checkpoint d'avant; bonne chance!", font=("system", 18), fg="blue", bg='navajo white')
    label1.grid(row=0, column=0, pady=5)
    q=Label(f, text=question[quest],bg='navajo white', font=("system", 18), fg="blue")
    q.grid(row=3, column=0, pady=5)
    boutton=Button(f1, text="Vérifier", font=("stencil", 20, ),bg='navajo white',fg='orchid4', relief=FLAT, command=testall)
    boutton.grid(row=13, column=0, pady=5)

    if quest==10:
        spin=Spinbox(f, from_=0, to=50)
        spin.grid()

    elif quest==13:
        var = StringVar()
        var.set(repspé[1])

        for i in range(3):
            y = Radiobutton(f, variable=var, text=repspé[i], value=repspé[i],bg='navajo white')
            y.grid()

    else:
        a= Label(f, text="Faîtes attention à bien mettre \n les accents, car si vous ne le faîtes pas, vous aurez forcément une réponse fausse", font=("fixedsys", 12, 'italic'), bg='navajo white', fg='red')
        a.grid(row=1, column=0, pady=1)
        ans=Entry(f, font=("stencil", 18))
        ans.grid(row=5, column=0, pady=1)

    def test_event(e):
            testall()
            fen.bind('<Return>', close_event)

    fen.bind('<Return>', test_event)

    fen.mainloop()
    if verif:return True
    return False


def testall():
    """
    fonction de test qui récupère la réponse donnée et vérifie si elle est juste ou non
    """
    global verif
    if quest==10:
        r=spin.get()
        if r=="9":verif=True
        else: verif=False

    elif quest==13:
        n=var.get()
        if n==repspé[3]:verif=True
        else:verif=False

    elif quest>=14:
        rep=ans.get()
        if rep==réponse[quest-1]:verif=True
        else:verif=False

    else:
        rep=ans.get()
        rep=rep.lower()
        if rep==réponse[quest]:verif=True
        else:verif=False

    f.destroy()

    if verif:
        boutton["bg"]="green"
        boutton['fg']='bisque'
        boutton["text"]="Correct"
        b=Label(f1, text="BRAVO, vous avez correctement répondu à l'énigme,\n le checkpoint va s'activer", bg='navajo white', font=("fixedsys", 20))
        b.grid(row=1, column=0, pady=5)

    else:
        boutton["bg"]="red"
        boutton['fg']='azure'
        boutton["text"]="FAUUUUX!!"
        c=Label(f1, text="HAHA, tu t'es loupé, retour a checkpoint d'avant!",bg='navajo white', font=("system", 20))
        c.grid(row=1, column=0, pady=5)

    boutton1=Button(f1, text="Close", font=("stencil", 20, ),bg='navajo white', fg="red", command=close, relief=FLAT)
    boutton1.grid(row=14, column=0, pady=5)


def quizz():
    """
    fonction choisissant un nombre au hasard entre 0 et 13 (car il y a 13 énigmes)
    """
    global r, n, g
    r=random.randint(n,g)
    return r


def close():
    fen.destroy()

def close_event(e):
    close()

def autoenigme():
    global en, question, réponse, re, r, text, text2
    fe=Tk()
    ff=Frame(fe)
    ff.grid()
    ff['bg']="navajo white"
    lab=Label(ff, text="Votre énigme :",font=("stencil",35 ),fg='red',bg='navajo white')
    lab.grid()
    text=Entry(ff,font=("stencil",35 ))
    text.grid(column=1)
    lab2=Label(ff, text="La réponse à votre énigme :",font=("stencil",35 ),fg='red',bg='navajo white')
    lab2.grid()
    text2=Entry(ff, font=('stencil', 35))
    text2.grid(column=1)
    bouton5=Button(ff, text="valider", command=ajout)
    bouton5.grid()
    fe.mainloop()

def ajout():
    print(1)
    global en, question, réponse, re, r, text, text2
    en=text.get()
    if en != "":
        question.append(en)
    else: pass
    re=text2.get()
    if re!="":
        réponse.append(re)
    else: pass

    g=len(question)
    saveQA()



autoenigme()
mainThomas()




