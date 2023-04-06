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























