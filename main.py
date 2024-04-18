def lire_automate_sur_fichier(nom_fichier):
    automate = {
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

def afficher_automate(automate):
    print("Alphabet:", automate['alphabet'])
    print("Nombre d'états:", automate['nb_etats'])
    print("États initiaux:", automate['etats_initiaux'])
    print("États terminaux:", automate['etats_terminaux'])
    print("Transitions:")
    for transition in automate['transitions']:
        print(transition)

#STANDARDISATION :

def est_standard(automate):
    if len(automate['etats_initiaux']) != 1:
        return False

    etat_initial = automate['etats_initiaux'][0]

    for transition in automate['transitions']:
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

#DETERMINISATION :


def est_deterministe(automate):
    if len(automate['etats_initiaux']) != 1:
        return False

    transitions = {}
    for transition in automate['transitions']:
        etat_source, symbole, etat_destination = transition
        if (etat_source, symbole) in transitions:
            return False
        transitions[(etat_source, symbole)] = etat_destination

    return True


def Determinisation(automate):

    if len(automate['etats_initiaux']) != 1:
        standardisation(automate)

    etats_visites = set()
    etats_a_traiter = [tuple(automate['etats_initiaux'])]

    nouveaux_etats = {}
    nouvelles_transitions = []

    while etats_a_traiter:
        etat_courant = etats_a_traiter.pop()
        etats_visites.add(etat_courant)

        transitions_par_symbole = {}
        for symbole in automate['alphabet']:
            etats_suivants = set()
            for etat in etat_courant:
                for transition in automate['transitions']:
                    if transition[0] == etat and transition[1] == symbole:
                        etats_suivants.add(transition[2])
            transitions_par_symbole[symbole] = etats_suivants

        for symbole, etats_suivants in transitions_par_symbole.items():
            nouvel_etat = tuple(sorted(list(etats_suivants)))
            nouvelles_transitions.append((etat_courant, symbole, nouvel_etat))

            if nouvel_etat not in etats_visites:
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


    print("L'automate est standard :", est_standard(automate_deterministe))
    print("L'automate est deterministe :", est_deterministe(automate_deterministe))
    print("L'automate est complet :", est_complet(automate_deterministe))


    return automate_deterministe


#COMPLETION

def est_complet(automate):
    transitions = {}
    for transition in automate['transitions']:
        etat_depart, symbole, etat_arrivee = transition
        transitions[(etat_depart, symbole)] = etat_arrivee
    for etat in range(automate['nb_etats']):
        for symbole in automate['alphabet']:
            if (etat, symbole) not in transitions:
                return False
    return True

def completion(automate):
    etat_poubelle = str(automate['nb_etats'])
    automate['nb_etats'] += 1

    nouvelles_transitions = []

    for etat in range(automate['nb_etats']):
        for lettre in automate['alphabet']:
            transition_existante = False
            for transition in automate['transitions']:
                etat_depart, symbole, _ = transition
                if etat_depart == str(etat) and symbole == lettre:
                    transition_existante = True
                    break
            if not transition_existante:
                nouvelles_transitions.append((str(etat), lettre, etat_poubelle))

    automate['transitions'].extend(nouvelles_transitions)

    return automate

#Complementaire

def automate_complementaire(automate):

    etats = set(automate['etats_initiaux'] + automate['etats_terminaux'])
    for transition in automate['transitions']:
        etats.update([transition[0], transition[2]])

    automate['etats_terminaux'] = list(etats - set(automate['etats_terminaux']))

    return automate



def main():
    # Lecture de l'automate depuis un fichier
    nom_fichier = "Test.txt"
    automate = lire_automate_sur_fichier(nom_fichier)
    # Affichage de l'automate
    afficher_automate(automate)
    # Vérification si l'automate est déterministe, complet, etc.
    print("L'automate est standard :", est_standard(automate))
    print("L'automate est deterministe :", est_deterministe(automate))
    print("L'automate est complet :", est_complet(automate))

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




if __name__ == "__main__":
    main()