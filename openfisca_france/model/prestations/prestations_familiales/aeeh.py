from openfisca_france.model.base import *
from openfisca_france.model.caracteristiques_socio_demographiques.logement import TypesLieuResidence


class aeeh_niveau_handicap(Variable):
    value_type = int
    entity = Individu
    label = "Catégorie de handicap prise en compte pour l'AEEH"
    definition_period = MONTH
    set_input = set_input_dispatch_by_period


class aeeh(Variable):
    value_type = float
    entity = Famille
    label = "Allocation d'éducation de l'enfant handicapé"
    reference = "http://vosdroits.service-public.fr/particuliers/N14808.xhtml"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2006_01_01(famille, period, parameters):
        """Allocation d'éducation de l'enfant handicapé.

        Rremplace l'allocation d'éducation spéciale (AES) depus le 1er janvier 2006.
        Ce montant peut être majoré par un complément accordé par la Cdaph qui prend en compte :
        le coût du handicap de l'enfant,
        la cessation ou la réduction d'activité professionnelle d'un ou l'autre des deux parents,
        l'embauche d'une tierce personne rémunérée.
        Une majoration est versée au parent isolé bénéficiaire d'un complément d'Aeeh lorsqu'il cesse ou réduit
        son activité professionnelle ou lorsqu'il embauche une tierce personne rémunérée.
        """
        janvier = period.this_year.first_month
        isole = not_(famille('en_couple', janvier))
        prestations_familiales = parameters(period).prestations.prestations_familiales

        base = prestations_familiales.aeeh.base
        complement_d_allocation = prestations_familiales.aeeh.complement_d_allocation
        majoration = prestations_familiales.aeeh.majoration_pour_parent_isole

        age = famille.members('age', janvier)
        handicap = famille.members('handicap', janvier)
        niveau_handicap = famille.members('aeeh_niveau_handicap', period)
        # Indicatrice d'isolement pour les indidivus
        isole = famille.project(isole)

        enfant_handicape = handicap * (age < prestations_familiales.aeeh.age_maximum_de_l_enfant)

        montant_par_enfant = enfant_handicape * prestations_familiales.af.bmaf * (
            base
            + (niveau_handicap == 1) * complement_d_allocation._children['1ere_categorie']
            + (niveau_handicap == 2) * (complement_d_allocation._children['1ere_categorie'] + majoration._children['2e_categorie'] * isole)
            + (niveau_handicap == 3) * (complement_d_allocation._children['2e_categorie'] + majoration._children['3e_categorie'] * isole)
            + (niveau_handicap == 4) * (complement_d_allocation._children['3e_categorie'] + majoration._children['4e_categorie'] * isole)
            + (niveau_handicap == 5) * (complement_d_allocation._children['4e_categorie'] + majoration._children['5e_categorie'] * isole)
            + (niveau_handicap == 6) * majoration._children['6e_categorie'] * isole
            ) + (niveau_handicap == 6) * complement_d_allocation._children['6e_categorie_1']

        montant_total = famille.sum(montant_par_enfant, role=Famille.ENFANT)

        # L'attribution de l'AEEH de base et de ses compléments éventuels ne fait pas obstacle au
        # versement des prestations familiales.
        # L'allocation de présence parentale peut être cumulée avec l'AEEH de base, mais pas avec son
        # complément ni avec la majoration de parent isolé.
        # Tous les éléments de la prestattion de compensation du handicap (PCH) sont également ouverts
        # aux bénéficiaires de l'AEEH de base, sous certaines conditions, mais ce cumul est exclusif du
        # complément de l'AEEH. Les parents d'enfants handicapés doivent donc choisir entre le versement
        # du complément d'AEEH et la PCH.

        # Ces allocations ne sont pas soumises à la CRDS
        return montant_total


class aes(Variable):
    value_type = float
    entity = Famille
    label = "Allocation d'éducation spéciale"
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add
    end = "2005-12-31"

    def formula_2002_04_01(famille, period, parameters):
        janvier = period.this_year.first_month
        isole = not_(famille('en_couple', janvier))
        prestations_familiales = parameters(period).prestations.prestations_familiales

        base = prestations_familiales.aes.base
        complement_d_allocation = prestations_familiales.aes.complement_d_allocation
        complement_d_allocation._children['6e_categorie_1'] = complement_d_allocation._children['6e_categorie_2']

        age = famille.members('age', janvier)
        handicap = famille.members('handicap', janvier)
        niveau_handicap = famille.members('aeeh_niveau_handicap', period)
        # Indicatrice d'isolement pour les indidivus
        isole = famille.project(isole)

        enfant_handicape = handicap * (age < prestations_familiales.aes.age_maximum_de_l_enfant)

        montant_par_enfant = enfant_handicape * prestations_familiales.af.bmaf * (
            base
            + (niveau_handicap == 1) * complement_d_allocation._children['1ere_categorie']
            + (niveau_handicap == 2) * complement_d_allocation._children['1ere_categorie']
            )

        montant_total = famille.sum(montant_par_enfant, role = Famille.ENFANT)
        return montant_total


class besoin_educatif_particulier(Variable):
    value_type = bool
    entity = Individu
    label = "Enfant possède une reconnaissance d’un besoin éducatif particulier"
    definition_period = MONTH


class aeeh_eligible(Variable):
    value_type = bool
    entity = Famille
    label = "Éligilité à l'Allocation d'éducation de l'enfant handicapé"
    reference = "https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006073189/LEGISCTA000006156691/#LEGIARTI000006750709"
    documentation = """
                    Art. L. 541-1 à 4 du Code de la sécurité sociale (CSS), art. R. 541-1 à 10 du CSS, art. D. 541-1
                    à 4 du CSS, arrêté du 24 avril 2002 relatif aux conditions d’attribution des six catégories de
                    complément d’allocation d’éducation spéciale.
                    """
    definition_period = MONTH
    set_input = set_input_divide_by_period
    calculate_output = calculate_output_add

    def formula_2020_01(famille, period, parameters):
        janvier = period.this_year.first_month
        age = famille.members('age', janvier)
        taux_incapacite = famille.members('taux_incapacite', janvier)
        besoin_educatif_particulier = famille.members('besoin_educatif_particulier', janvier)

        aeeh_parameters = parameters(period).prestations.prestations_familiales.aeeh
        residence = famille.members.menage('residence', period)

        condition_age = (age < aeeh_parameters.age_maximum_de_l_enfant)
        condition_taux_incapacite = (
            (
            taux_incapacite >= aeeh_parameters.taux_incapacite_maximal.taux_incapacite_maximal_aeeh
            ) + (
                (
                    taux_incapacite >= aeeh_parameters.taux_incapacite_minimal.taux_incapacite_minimal_aeeh
                    ) * (
                        taux_incapacite < aeeh_parameters.taux_incapacite_maximal.taux_incapacite_maximal_aeeh
                        ) * besoin_educatif_particulier
                    )
            )

        condition_residence_FR = False if residence ==TypesLieuResidence.non_renseigne else True

        return condition_age * condition_taux_incapacite * condition_residence_FR
