from openfisca_france.model.base import Variable, Individu, MONTH, set_input_dispatch_by_period, set_input_divide_by_period


class eligibilite_majoration_indemnite_service_civique(Variable):
    value_type = bool
    label = 'Majoration des indemnités pour les étudiants boursiers et les bénéficiaires du RSA'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F13278'

    def formula(individu, period):
        bcs = individu('bourse_criteres_sociaux', period)
        rsa = individu.famille('rsa', period) > 0
        return (bcs + rsa) > 0


class service_civique(Variable):
    value_type = bool
    label = 'Est en contrat de service civique'
    entity = Individu
    definition_period = MONTH
    set_input = set_input_dispatch_by_period
    reference = 'https://www.service-public.fr/particuliers/vosdroits/F13278'


class montant_indemnite_service_civique(Variable):
    value_type = float
    label = "Montant de l'indemnité de Service Civique"
    entity = Individu
    definition_period = MONTH
    set_input = set_input_divide_by_period

    def formula_2022_07_01(individu, period, parameters):
        modalites_service_civique = parameters(period).prestations_sociales.education.service_civique

        service_en_cours = individu('service_civique', period)
        montant = modalites_service_civique.montant_indemnites

        eligibilite_majoration = individu('eligibilite_majoration_indemnite_service_civique', period)
        montant_majoration = modalites_service_civique.montant_majoration

        montant_final = montant + (eligibilite_majoration * montant_majoration)
        return montant_final * service_en_cours
