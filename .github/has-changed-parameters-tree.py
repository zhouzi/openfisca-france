from os import getenv, getcwd, listdir, walk
from glob import glob

# chemin vers le dépôt openfisca-france/
GITHUB_WORKSPACE=getenv("GITHUB_WORKSPACE", default=getcwd())
PARAMETERS_PATH = GITHUB_WORKSPACE+"/openfisca_france/parameters"


# CAS 1) le répertoire a-t-il changé ?
# si le répertoire a changé, afficher un message et terminer en erreur

patterns = ["/chomage",
    "/chomage/allocation_retour_emploi",
    "/chomage/allocations_assurance_chomage",
    "/chomage/allocations_chomage_solidarite",
    "/chomage/preretraites",
    "/geopolitique",
    "/impot_revenu",
    "/marche_travail",
    "/marche_travail/epargne",
    "/marche_travail/remuneration_dans_fonction_publique",
    "/marche_travail/salaire_minimum",
    "/prelevements_sociaux",
    "/prelevements_sociaux/autres_taxes_participations_assises_salaires",
    "/prelevements_sociaux/contributions_assises_specifiquement_accessoires_salaire",
    "/prelevements_sociaux/contributions_sociales",
    "/prelevements_sociaux/cotisations_regime_assurance_chomage",
    "/prelevements_sociaux/cotisations_secteur_public",
    "/prelevements_sociaux/cotisations_securite_sociale_regime_general",
    "/prelevements_sociaux/cotisations_taxes_independants_artisans_commercants",
    "/prelevements_sociaux/cotisations_taxes_professions_liberales",
    "/prelevements_sociaux/pss",
    "/prelevements_sociaux/reductions_cotisations_sociales",
    "/prelevements_sociaux/regimes_complementaires_retraite_secteur_prive",
    "/prestations_sociales",
    "/prestations_sociales/aides_jeunes",
    "/prestations_sociales/aides_logement",
    "/prestations_sociales/fonc",
    "/prestations_sociales/prestations_etat_de_sante",
    "/prestations_sociales/prestations_etat_de_sante/invalidite",
    "/prestations_sociales/prestations_etat_de_sante/perte_autonomie_personnes_agees",
    "/prestations_sociales/prestations_familiales",
    "/prestations_sociales/prestations_familiales/bmaf",
    "/prestations_sociales/prestations_familiales/def_biactif",
    "/prestations_sociales/prestations_familiales/def_pac",
    "/prestations_sociales/prestations_familiales/education_presence_parentale",
    "/prestations_sociales/prestations_familiales/logement_cadre_vie",
    "/prestations_sociales/prestations_familiales/petite_enfance",
    "/prestations_sociales/prestations_familiales/prestations_generales",
    "/prestations_sociales/solidarite_insertion",
    "/prestations_sociales/solidarite_insertion/autre_solidarite",
    "/prestations_sociales/solidarite_insertion/minima_sociaux",
    "/prestations_sociales/solidarite_insertion/minimum_vieillesse",
    "/prestations_sociales/transport",
    "/taxation_capital",
    "/taxation_capital/impot_fortune_immobiliere_ifi_partir_2018",
    "/taxation_capital/impot_grandes_fortunes_1982_1986",
    "/taxation_capital/impot_solidarite_fortune_isf_1989_2017",
    "/taxation_capital/prelevement_forfaitaire",
    "/taxation_capital/prelevements_sociaux",
    "/taxation_indirecte",
    "/taxation_societes"
    ]


def subdirectories_exist(directory_pathname, directory_subpath):
    path = directory_pathname+directory_subpath
    assert glob(path) != [], (
        f"répertoire introuvable : {path} \n \
        Ce répertoire doit être conservé pour la concordance des hiérarchies de paramètres entre openfisca-france et les barèmes IPP."
    )


def validate_directories_tree(directory_pathname, patterns):
    for pattern in patterns:
        subdirectories_exist(directory_pathname, pattern)


# TODO CAS 2) y a-t-il eu un ajout de répertoire ?


if __name__ == '__main__':
    validate_directories_tree(PARAMETERS_PATH, patterns)
