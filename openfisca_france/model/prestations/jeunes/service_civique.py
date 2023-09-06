from openfisca_france.model.base import Variable, Individu, MONTH, set_input_dispatch_by_period, set_input_divide_by_period


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
        service_en_cours = individu('service_civique', period)
        montant = parameters(period).prestations_sociales.education.service_civique.montants_indemnites
        return montant * service_en_cours
