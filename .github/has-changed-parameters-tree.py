from os import getcwd

GITHUB_WORKSPACE=".../openfisca-france"


# CAS 1) le répertoire a-t-il changé ?
parameters = {
    "chomage": ["allocation_retour_emploi", "allocations_assurance_chomage", "allocations_chomage_solidarite", "preretraites"]
}

# si le répertoire a changé, afficher un message et terminer en erreur


# CAS 2) y a-t-il eu un ajout de répertoire ?

if __name__ == '__main__':
    print(getcwd())
