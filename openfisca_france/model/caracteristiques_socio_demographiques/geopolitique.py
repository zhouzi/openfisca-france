import codecs
import csv
import pkg_resources

import numpy as np

import openfisca_france
from openfisca_france.model.base import *


class code_departement(Variable):
    value_type = str
    max_length = 3
    entity = Menage
    label = 'Code INSEE du département de résidence'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period):
        depcom = menage('depcom', period)
        return np.fromiter(
            (
                depcom_cell[:3] if depcom_cell.startswith(('97', '98')) else depcom_cell[:2]
                for depcom_cell in depcom
                ),
            dtype=(str, 3),
            )


dated_code_region_by_code_departement = None


def preload_departements_regions():
    global dated_code_region_by_code_departement
    if dated_code_region_by_code_departement is None:
        with pkg_resources.resource_stream(
                openfisca_france.__name__,
                'assets/geopolitique/departements_regions.csv',
                ) as csv_file:
            utf8_reader = codecs.getreader('utf-8')
            csv_reader = csv.DictReader(utf8_reader(csv_file))
            dated_code_region_by_code_departement = {}
            for row in csv_reader:
                code_departement = row['code_departement']
                code_region = row['code_region']
                dated_code_region = dated_code_region_by_code_departement.get(code_departement)
                if dated_code_region is None:
                    dated_code_region_by_code_departement[code_departement] = [(row['date'], code_region)]
                elif code_region != dated_code_region[-1][1]:
                    dated_code_region.append((row['date'], code_region))


def code_region_from_code_departement(date, code_departement):
    for start_date, code_region in dated_code_region_by_code_departement[code_departement]:
        if start_date <= date:
            return code_region
    return ""


class code_region(Variable):
    value_type = str
    max_length = 2
    entity = Menage
    label = 'Code INSEE de la région de résidence'
    definition_period = MONTH
    set_input = set_input_dispatch_by_period

    def formula(menage, period, parameters):
        code_departement = menage('code_departement', period)
        start_date = str(period.start)
        return np.fromiter(
            (
                code_region_from_code_departement(start_date, code_departement_cell)
                for code_departement_cell in code_departement
                ),
            dtype=(str, 2),
            )
