#Fonctions pour la sauvegarde#

def saveread(score):
    with open("scores.txt","r") as fichier:
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

def save(score,vol,pos,vol2,pos2):
    bestscore = saveread("bestscore")
    fichier = open("scores.txt","w+")
    if score > int(bestscore):
        fichier.write(str(score)+"\n"+str(score)+"\n"+str(vol)+"\n"+str(pos)+"\n"+str(vol2)+"\n"+str(pos2))
        fichier.close()
    else:
        fichier.write(bestscore+"\n"+str(score)+"\n"+str(vol)+"\n"+str(pos)+"\n"+str(vol2)+"\n"+str(pos2))
        fichier.close()