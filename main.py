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
    if len(automate['etats_initiaux']) > 1:
        nouvel_etat_initial = automate['nb_etats']
        automate['nb_etats'] += 1
        nouvelles_transitions = []
        for i in automate['etats_initiaux']:

            for transition in automate['transitions']:
                etat_depart, symbole, etat_arrivee = transition
                print(repr(etat_depart), type(etat_depart))
                print(repr(i), type(i))
                if etat_depart == i:
                    # Ajouter une nouvelle transition vers l'ancien état d'arrivée
                    nouvelles_transitions.append((nouvel_etat_initial, symbole, etat_arrivee))
                    print('a')

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

#COMPLETION

def est_complet(automate):
    alphabet = automate['alphabet']
    etats = []
    for transition in automate['transitions']:
        etat_source, _, _ = transition
        if etat_source not in etats:
            etats.append(etat_source)
    for etat in etats:
        symboles_sortants = {transition[1] for transition in automate['transitions'] if transition[0] == etat}
        if len(symboles_sortants) < len(alphabet):
            return False
    return True


def main():
    # Lecture de l'automate depuis un fichier
    nom_fichier = "Automates.txt"
    automate = lire_automate_sur_fichier(nom_fichier)
    # Affichage de l'automate
    afficher_automate(automate)
    # Vérification si l'automate est déterministe, complet, etc.
    print("L'automate est standard :", est_standard(automate))
    print("L'automate est deterministe :", est_deterministe(automate))
    print("L'automate est complet :", est_complet(automate))



    if input("Voulez-vous le standardiser ? (oui/non) : ").lower() == "oui":
        standardisation(automate)
        afficher_automate(automate)

if __name__ == "__main__":
    main()