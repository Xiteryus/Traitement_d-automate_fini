def lire_automate_sur_fichier(nom_fichier):
    automate = {
        'alphabet': [],
        'nb_etats': 0,
        'etats_initiaux': [],
        'etats_terminaux': [],
        'transitions': []
    }
    with open(nom_fichier, 'r') as f:
        automate['alphabet'] = f.readline()
        automate['nb_etats'] = int(f.readline())
        automate['etats_initiaux'] = list(map(int, f.readline().split()[1:]))
        automate['etats_terminaux'] = list(map(int, f.readline().split()[1:]))
        nb_transitions = int(f.readline())
        for _ in range(nb_transitions):
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

def est_un_automate_deterministe(automate):
    transitions = {}
    for transition in automate['transitions']:
        etat_depart, symbole, etat_arrivee = transition
        if (etat_depart, symbole) in transitions:
            return False
        transitions[(etat_depart, symbole)] = etat_arrivee
    return True

def est_un_automate_complet(automate):
    transitions = {}
    for transition in automate['transitions']:
        etat_depart, symbole, etat_arrivee = transition
        transitions[(etat_depart, symbole)] = etat_arrivee
    for etat in range(automate['nb_etats']):
        for symbole in automate['alphabet']:
            if (etat, symbole) not in transitions:
                # S'il manque une transition pour un état donné avec un symbole donné, l'automate n'est pas complet
                return False
    return True

def completion(automate):
    transitions = {}
    for transition in automate['transitions']:
        etat_depart, symbole, etat_arrivee = transition
        transitions[(etat_depart, symbole)] = etat_arrivee
    for etat in range(automate['nb_etats']):
        for symbole in automate['alphabet']:
            if (etat, symbole) not in transitions:
                # Si une transition manque, on ajoute une transition vers un nouvel état poubelle
                transitions[(etat, symbole)] = automate['nb_etats']
    automate['nb_etats'] += 1  # On ajoute un nouvel état
    automate['etats_terminaux'].append(automate['nb_etats'] - 1)  # Le nouvel état est terminal
    automate['transitions'] = list(transitions.keys())

def standardisation(automate):
    if len(automate['etats_initiaux']) > 1:
        # S'il y a plus d'un état initial, on les remplace par un seul nouvel état initial
        nouvel_etat_initial = automate['nb_etats']
        automate['nb_etats'] += 1
        for etat_initial in automate['etats_initiaux']:
            automate['transitions'].append((nouvel_etat_initial, '', etat_initial))
        automate['etats_initiaux'] = [nouvel_etat_initial]

def reconnaitre_mot(automate, mot):
    etat_courant = automate['etats_initiaux'][0]
    for symbole in mot:
        transition_trouvee = False
        for transition in automate['transitions']:
            etat_depart, symbole_transition, etat_arrivee = transition
            if etat_depart == etat_courant and symbole_transition == symbole:
                etat_courant = etat_arrivee
                transition_trouvee = True
                break
        if not transition_trouvee:
            return False
    return etat_courant in automate['etats_terminaux']

def automates_complementaire(automate):
    automate_complementaire = {
        'alphabet': automate['alphabet'],
        'nb_etats': automate['nb_etats'],
        'etats_initiaux': automate['etats_initiaux'],
        'etats_terminaux': [
            etat for etat in range(automate['nb_etats']) if etat not in automate['etats_terminaux']
        ],
        'transitions': [
            (etat_depart, symbole, etat_arrivee)
            for etat_depart in range(automate['nb_etats'])
            for symbole in automate['alphabet']
            for etat_arrivee in range(automate['nb_etats'])
            if (etat_depart, symbole, etat_arrivee) not in automate['transitions']
        ]
    }
    return automate_complementaire

def afficher_table_correspondance(automate):
    print("Table de correspondance des états:")
    for etat in range(automate['nb_etats']):
        print(f"État {etat} de l'automate correspond à {correspondance_etat(automate, etat)}")

def correspondance_etat(automate, etat):
    return etat

def main():
    # Lecture de l'automate depuis un fichier
    automate = lire_automate_sur_fichier("Automate")
    # Affichage de l'automate
    afficher_automate(automate)
    # Vérification si l'automate est déterministe, complet, etc.
    if not est_un_automate_deterministe(automate):
        # Si l'automate n'est pas déterministe
        if input("Voulez-vous le standardiser ? (oui/non) : ") == "oui":
            standardisation(automate)
    if not est_un_automate_complet(automate):
        completion(automate)
    afficher_automate(automate)
    # Reconnaissance de mots
    mot = input("Entrez un mot à reconnaître (ou 'fin' pour terminer) : ")
    while mot.lower() != "fin":
        if reconnaitre_mot(automate, mot):
            print("Le mot est reconnu par l'automate.")
        else:
            print("Le mot n'est pas reconnu par l'automate.")
        mot = input("Entrez un autre mot (ou 'fin' pour terminer) : ")

    # Construction de l'automate complémentaire
    automate_complementaire = automates_complementaire(automate)
    afficher_automate(automate_complementaire)
    afficher_table_correspondance(automate)

if __name__ == "__main__":
    main()
