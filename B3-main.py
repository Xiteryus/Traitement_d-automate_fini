import os


def lire_automate_sur_fichier(nom_fichier): #Création de l'automate
    automate = { #Initialisation de l'automate dans un dictionnaire
        'alphabet': [],
        'nb_etats': 0,
        'etats_initiaux': [],
        'etats_terminaux': [],
        'transitions': []
    }
    with open(nom_fichier, 'r') as f:
        automate['alphabet'] = f.readline().split()
        automate['nb_etats'] = int(f.readline())
        automate['etats_initiaux'] = list(map(str, f.readline().split()[0:]))
        automate['etats_terminaux'] = list(map(str, f.readline().split()[0:]))
        nb_transitions = int(f.readline())
        for i in range(nb_transitions):
            transition = tuple(f.readline().split())
            automate['transitions'].append(transition)
    return automate

def afficher_automate(automate): #affichage de l'automate
    print("Alphabet:", automate['alphabet'])
    print("Nombre d'états:", automate['nb_etats'])
    print("États initiaux:", automate['etats_initiaux'])
    print("États terminaux:", automate['etats_terminaux'])
    print("Transitions:")
    for transition in automate['transitions']:
        print(transition)


#----------------------------------------------------------------------------------------------
#STANDARDISATION :
#----------------------------------------------------------------------------------------------

def est_standard(automate):
    if len(automate['etats_initiaux']) != 1: #S'il y a plusieurs entrées, l'automate ne peut pas être standard
        return False

    etat_initial = automate['etats_initiaux'][0]

    for transition in automate['transitions']: #On parcourt ensuite l'automate pour trouver si etat ne va pas sur l'automate initial
        etat_source, _, etat_destination = transition #on utilise pas le symbole donc on met un _ pour le symboliser
        if etat_destination == etat_initial:
            return False

    return True


def standardisation(automate):
    test_vide = False
    if est_standard(automate) == False :
        nouvel_etat_initial = str(automate['nb_etats'])
        automate['nb_etats'] += 1
        nouvelles_transitions = []
        for i in automate['etats_initiaux']:
            for transition in automate['transitions']:
                etat_depart, symbole, etat_arrivee = transition
                if etat_depart == i:
                    # Ajouter une nouvelle transition vers l'ancien état d'arrivée
                    nouvelles_transitions.append((nouvel_etat_initial, symbole, etat_arrivee))
            #Test si l'automate reconnait le mot vide
            if i in automate['etats_terminaux']:
                test_vide = True
        # Ajout du nouveau etat final si le mot vide est reconnu
        if test_vide == True:
            automate['etats_terminaux'].extend([nouvel_etat_initial])
        # Ajouter les nouvelles transitions à l'ensemble des transitions
        automate['transitions'].extend(nouvelles_transitions)
        automate['etats_initiaux'] = [nouvel_etat_initial]
    return automate


#----------------------------------------------------------------------------------------------
#DETERMINISATION :
#----------------------------------------------------------------------------------------------

def est_deterministe(automate):
    if len(automate['etats_initiaux']) != 1:
        return False

    transitions = {} #initialisation des transitions
    for transition in automate['transitions']:
        etat_source, symbole, etat_destination = transition
        if (etat_source, symbole) in transitions: #on verifie que l'etat et le symbole ne soient déja dans le dictionnaire
            return False #si la paire existe, l'automate n'est pas deterministe
        transitions[(etat_source, symbole)] = etat_destination

    return True



def Determinisation(automate):

    if len(automate['etats_initiaux']) != 1: #Si l'automate à plusieurs entré on standardise
        automate = standardisation(automate)

    etats_visites = set()
    etats_a_traiter = [tuple(automate['etats_initiaux'])] #initialise une liste

    nouveaux_etats = {} #initialise un dictionnaire
    nouvelles_transitions = [] #initialise une liste

    while etats_a_traiter:
        etat_courant = etats_a_traiter.pop() #Enleve un état à chaque iteration
        etats_visites.add(etat_courant)

        transitions_par_symbole = {}
        for symbole in automate['alphabet']:
            etats_suivants = set()
            for etat in etat_courant:
                for transition in automate['transitions']: #on parcourt chaque transition
                    if transition[0] == etat and transition[1] == symbole:
                        etats_suivants.add(transition[2])
            transitions_par_symbole[symbole] = etats_suivants #les etats suivants sont ajoutés au dictionnaire

        for symbole, etats_suivants in transitions_par_symbole.items():
            nouvel_etat = tuple(sorted(list(etats_suivants)))
            nouvelles_transitions.append((etat_courant, symbole, nouvel_etat)) #les nouvelles transitions sont ajoutées à la liste

            if nouvel_etat not in etats_visites: #si le nouvel état n'est pas traité, il est ajouté dans liste
                etats_a_traiter.append(nouvel_etat)

        nouveaux_etats[etat_courant] = None

    automate_deterministe = {
        'alphabet': automate['alphabet'],
        'nb_etats': len(nouveaux_etats),
        'etats_initiaux': [tuple(automate['etats_initiaux'])],
        'etats_terminaux': [],
        'transitions': nouvelles_transitions
    }

    for etat, _ in nouveaux_etats.items():
        for etat_terminal in automate['etats_terminaux']:
            if etat_terminal in etat:
                automate_deterministe['etats_terminaux'].append(etat)

    #afficher_automate(automate_deterministe)
    #print("L'automate est standard :", est_standard(automate_deterministe))
    #print("L'automate est deterministe :", est_deterministe(automate_deterministe))
    #print("L'automate est complet :", est_complet(automate_deterministe))

    if not(est_complet(automate_deterministe)):#si l'automate n'est pas complet, on le complete
        automate_deterministe = completion(automate_deterministe)

    return automate_deterministe

#----------------------------------------------------------------------------------------------
#COMPLETION :
#----------------------------------------------------------------------------------------------

def recup_etat(automate):
    etat_dans_automate = []
    for transition in automate['transitions']:
        etat_depart, symbole, etat_arrivee = transition
        if etat_depart not in etat_dans_automate:#on verifie si l'etat de depart n'est pas present dans la liste
            etat_dans_automate.append(etat_depart)#on l'ajoute s'il ne l'est pas
        if etat_arrivee not in etat_dans_automate:
            etat_dans_automate.append(etat_arrivee)
    return etat_dans_automate


def est_complet(automate):
    transitions = {}
    etat_automate = recup_etat(automate)
    for transition in automate['transitions']:
        etat_depart, symbole, etat_arrivee = transition
        transitions[(etat_depart, symbole)] = etat_arrivee #on associe l'etat de depart et le symbole à l'etat d'arrivée
    for etat in etat_automate:
        for symbole in automate['alphabet']:
            if (etat, symbole) not in transitions:
                # s'il manque une transition pour un état donné avec un symbole donné, l'automate n'est pas complet
                return False
    return True


def completion(automate):
    nouvel_etat_initial = 'P' #initialisation de l'etat poubelle
    automate['nb_etats'] += 1

    nouvelles_transitions = []
    etat_automate = recup_etat(automate)

    for etat in etat_automate:
        for lettre in automate['alphabet']:
            transition_existante = False #transition_existante indique si une transition existe
            for transition in automate['transitions']:
                etat_depart, symbole, etat_arrivee = transition
                if etat_depart == str(etat) and symbole == lettre:
                    transition_existante = True
                    break
            if not transition_existante:# il manque une transition, on ajoute donc une transition qu'on relie à l'etat poubelle
                nouvelles_transitions.append((str(etat), lettre, nouvel_etat_initial))

    automate['transitions'].extend(nouvelles_transitions)

    return automate
#----------------------------------------------------------------------------------------------
#Complementaire :
#----------------------------------------------------------------------------------------------

def complementaire(automate):

    etats = set(automate['etats_initiaux'] + automate['etats_terminaux']) #ensemble d'etats initiaux et terminaux
    for transition in automate['transitions']:
        etats.update([transition[0], transition[2]])#on parcourt les transitions et met à jour l'ensemble en y ajoutant les etats de depart et d'arrivée

    automate['etats_terminaux'] = list(etats - set(automate['etats_terminaux']))#on fait la difference entre l'ensemble des etats et les etats terminaux de base

    return automate

#----------------------------------------------------------------------------------------------
#test de reconnaissance de mots   :
#----------------------------------------------------------------------------------------------

def test_reconnaissance(automate,mot):

    etats_actuels = set(automate['etats_initiaux'])

    for lettre in mot:#on boucle pour chaque lettre
        nouveaux_etats = set()

        for etat in etats_actuels:
            for transition in automate['transitions']:
                etat_source, symbole, etat_destination = transition
                if etat_source == etat and symbole == lettre:
                    nouveaux_etats.add(etat_destination)

        etats_actuels = nouveaux_etats

    for etat in etats_actuels:
        if etat in automate['etats_terminaux']:
            return True

    return False

def test_reconnaissance_automates(mot):
    list_automates = []

    for i in range(1, 45):

        # Lire l'automate à partir du fichier
        automate = lire_automate_sur_fichier(f"B3-{i:02d}.txt")

        # Tester la reconnaissance du mot dans l'automate
        if test_reconnaissance(automate, mot):
            list_automates.append(i)

    if list_automates:
        print("Mot reconnu dans les automates :", ', '.join(map(str, list_automates)))
    else:
        print("Le mot n'est reconnu dans aucun automate.")

#----------------------------------------------------------------------------------------------
def contient_mot_vide(automate): #parcourt les transition, s'il'y le mot vide symbolisé par E, alors la fonction retourne True
    transitions = automate['transitions']
    for transition in transitions:
        if transition[1] == 'E':
            return True
    return False

def supprimer_mot_vide(automate): #Fonction inutile
    transitions_sans_e = []
    for transition in automate['transitions']:
        source, symbole, destination = transition
        if symbole != 'E':
            transitions_sans_e.append(transition)
    nouveau_automate = automate.copy()
    nouveau_automate['transitions'] = transitions_sans_e
    return nouveau_automate


#----------------------------------------------------------------------------------------------
def selection_automate():
    x = True

    while x == True:
        a = input("Quel automate voulez-vous sélectionner (de 01 à 44) ? ")
        nom_fichier = "B3-"+a + ".txt"
        if not os.path.exists(nom_fichier): #si l'automate choisit n'existe pas, on envoie un message d'erreur au lieu de fermer le programme
            print("L'automate n'existe pas.")
        else:
            # Lire l'automate à partir du fichier
            automate = lire_automate_sur_fichier(nom_fichier)
            x = False

    return automate



def main():
    # Lecture de l'automate depuis un fichier
    # Affichage de l'automate



    #print("L'automate est standard :", est_standard(automate))
    #print("L'automate est deterministe :", est_deterministe(automate))
    #print("L'automate est complet :", est_complet(automate))
    #print("L'automate contient le mot vite :", contient_mot_vide(automate))

    a = selection_automate()
    q = False
    while not q:
        print("MENU : ")
        print("1. Selection d'un autre automate")
        print("2. Afficher les informations de l'automate")
        print("3. Rendre l'automate déterministe")
        print("4. Rendre l'automate complet")
        print("5. Rendre l'automate standard")
        print("6. Reconnaissance de mot dans l'automate selectionne")
        print("7. Reconnaissance de mot dans tous les automates")
        print("8. Donner l'automate complementaire")
        print("9. Quitter")
        choix = input("Entrez votre choix : ")
        if choix == '1':
            a = selection_automate()
        elif choix == '2':
            afficher_automate(a)
            print("L'automate est standard :", est_standard(a))
            print("L'automate est deterministe :", est_deterministe(a))
            print("L'automate est complet :", est_complet(a))
            print("L'automate contient le mot vite :", contient_mot_vide(a))
            afficher_automate(supprimer_mot_vide(a))

        elif choix == '3':
            if est_deterministe(a):
                print("L'automate est deja deterministe")
            else:
                a = Determinisation(a)
                afficher_automate(a)
        elif choix == '4':
            if est_complet(a):
                print("L'automate est deja complet")
            else:
                a = completion(a)
                afficher_automate(a)
        elif choix == '5':
            if est_standard(a):
                print("L'automate est deja standard")
            else:
                a = standardisation(a)
                afficher_automate(a)
        elif choix == '6':
                mot = input("Entrez le mot que vous voulez reconnaître : ")
                if test_reconnaissance(a,mot)==True:
                    print("Le mot est reconnu par l'automate.")
                else:
                    print("Le mot n'est pas reconnu par l'automate.")
        elif choix == '7':
                mot = input("Entrez le mot que vous voulez reconnaître : ")
                test_reconnaissance_automates(mot)
        elif choix=='8':
            a = complementaire(a)
            afficher_automate(a)
        elif choix == "9":
            q = True
        else:
            print("Choix invalide. Veuillez choisir une option valide.")

'''    # Vérification si l'automate est déterministe, complet, etc.
    print("L'automate est standard :", est_standard(automate))
    print("L'automate est deterministe :", est_deterministe(automate))
    print("L'automate est complet :", est_complet(automate))

    test_reconnaissance(automate)

    if input("Voulez-vous le determiniser ? (oui/non) : ") == "oui":
        afficher_automate(Determinisation(automate))

    if input("Voulez-vous le complementariser ? (oui/non) : ") == "oui":
        automate_complementaire(automate)
        afficher_automate(automate)



    if input("Voulez-vous le Completer ? (oui/non) : ") == "oui":
        completion(automate)
        afficher_automate(automate)

    if input("Voulez-vous le standardiser ? (oui/non) : ") == "oui":
        standardisation(automate)
        afficher_automate(automate)

'''


if __name__ == "__main__":
    main()