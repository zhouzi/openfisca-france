#! /usr/bin/env python

'''Associe les départements avec leurs régions.

Utilise les données du code officiel géographique :
https://www.insee.fr/fr/information/2560452.
'''

import csv
import io
import os
import zipfile

import requests


verify_certificate = False


departement_region_associations = []
latest_association_index_by_code_departement = {}

for year, inseeId in [
        (1999, 2560686),
        (2000, 2560681),
        (2001, 2560676),
        (2002, 2560671),
        (2003, 2560666),
        (2004, 2560661),
        (2005, 2560656),
        (2006, 2560651),
        (2007, 2560646),
        (2008, 2560640),
        (2009, 2560635),
        (2010, 2560630),
        (2011, 2560625),
        (2012, 2560620),
        (2013, 2560615),
        (2014, 2560563),
        (2015, 2560698),
        (2016, 2114819),
        (2017, 2666684),
        (2018, 3363419),
        ]:
    region_by_code = {}
    url = f'https://www.insee.fr/fr/statistiques/fichier/{inseeId}/reg{year}-txt.zip'
    response = requests.get(url, verify=verify_certificate)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zipFile:
        tsvData = zipFile.read(f'reg{year}.txt').decode('iso-8859-15')
        tsvReader = csv.reader(io.StringIO(tsvData), delimiter='\t')
        labels = next(tsvReader)
        for row in tsvReader:
            region = {
                label: cell
                for label, cell in zip(labels, row)
                }
            region_by_code[region['REGION']] = region

    url = f'https://www.insee.fr/fr/statistiques/fichier/{inseeId}/depts{year}-txt.zip'
    response = requests.get(url, verify=verify_certificate)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zipFile:
        tsvData = zipFile.read(f'depts{year}.txt').decode('iso-8859-15')
        tsvReader = csv.reader(io.StringIO(tsvData), delimiter='\t')
        labels = next(tsvReader)
        for row in tsvReader:
            departement = {
                label: cell
                for label, cell in zip(labels, row)
                }
            region = region_by_code[departement['REGION']]
            departement_region_association = {
                'code_departement': departement['DEP'],
                'code_region': region['REGION'],
                'date': f'{year}-01-01',
                'libelle_departement': departement['NCCENR'],
                'libelle_region': region['NCCENR'],
                }
            latest_association_index = latest_association_index_by_code_departement.get(
                departement['DEP'])
            if latest_association_index is not None:
                latest_association = departement_region_associations[
                    latest_association_index]
                if all(
                        value == latest_association[key]
                        for key, value in departement_region_association.items()
                        if key != 'date'
                        ):
                    # Association already exists.
                    continue
            latest_association_index_by_code_departement[departement['DEP']] = len(
                departement_region_associations)
            departement_region_associations.append(departement_region_association)

for year, inseeId in [
        (2019, 3720946),
        (2020, 4316069),
        (2021, 5057840),
        ]:
    region_by_code = {}
    url = f'https://www.insee.fr/fr/statistiques/fichier/{inseeId}/region{year}-csv.zip'
    response = requests.get(url, verify=verify_certificate)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zipFile:
        csvData = zipFile.read(f'region{year}.csv').decode('utf-8')
        csvReader = csv.reader(io.StringIO(csvData), delimiter=',')
        labels = next(csvReader)
        for row in csvReader:
            region = {
                label.lower(): cell
                for label, cell in zip(labels, row)
                }
            region_by_code[region['reg']] = region

    url = f'https://www.insee.fr/fr/statistiques/fichier/{inseeId}/departement{year}-csv.zip'
    response = requests.get(url, verify=verify_certificate)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zipFile:
        csvData = zipFile.read(f'departement{year}.csv').decode('utf-8')
        csvReader = csv.reader(io.StringIO(csvData), delimiter=',')
        labels = next(csvReader)
        for row in csvReader:
            departement = {
                label.lower(): cell
                for label, cell in zip(labels, row)
                }
            region = region_by_code[departement['reg']]
            departement_region_association = {
                'code_departement': departement['dep'],
                'code_region': region['reg'],
                'date': f'{year}-01-01',
                'libelle_departement': departement['nccenr'],
                'libelle_region': region['nccenr'],
                }
            latest_association_index = latest_association_index_by_code_departement.get(
                departement['dep'])
            if latest_association_index is not None:
                latest_association = departement_region_associations[
                    latest_association_index]
                if all(
                        value == latest_association[key]
                        for key, value in departement_region_association.items()
                        if key != 'date'
                        ):
                    # Association already exists.
                    continue
            latest_association_index_by_code_departement[departement['dep']] = len(
                departement_region_associations)
            departement_region_associations.append(departement_region_association)

for year, inseeId in [
        (2022, 6051727),
        ]:
    region_by_code = {}
    url = f'https://www.insee.fr/fr/statistiques/fichier/{inseeId}/region_{year}.csv'
    response = requests.get(url, verify=verify_certificate)
    csvReader = csv.reader(io.StringIO(response.content.decode('utf-8')), delimiter=',')
    labels = next(csvReader)
    for row in csvReader:
        region = {
            label: cell
            for label, cell in zip(labels, row)
            }
        region_by_code[region['REG']] = region

    url = f'https://www.insee.fr/fr/statistiques/fichier/{inseeId}/departement_{year}.csv'
    response = requests.get(url, verify=verify_certificate)
    csvReader = csv.reader(io.StringIO(response.content.decode('utf-8')), delimiter=',')
    labels = next(csvReader)
    for row in csvReader:
        departement = {
            label: cell
            for label, cell in zip(labels, row)
            }
        region = region_by_code[departement['REG']]
        departement_region_association = {
            'code_departement': departement['DEP'],
            'code_region': region['REG'],
            'date': f'{year}-01-01',
            'libelle_departement': departement['NCCENR'],
            'libelle_region': region['NCCENR'],
            }
        latest_association_index = latest_association_index_by_code_departement.get(
            departement['DEP'])
        if latest_association_index is not None:
            latest_association = departement_region_associations[
                latest_association_index]
            if all(
                    value == latest_association[key]
                    for key, value in departement_region_association.items()
                    if key != 'date'
                    ):
                # Association already exists.
                continue
        latest_association_index_by_code_departement[departement['DEP']] = len(
            departement_region_associations)
        departement_region_associations.append(departement_region_association)

package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_dir = os.path.join(package_dir, 'assets')
geopolitique_dir = os.path.join(assets_dir, 'geopolitique')
with open(os.path.join(geopolitique_dir, 'departements_regions.csv'), 'w') as csv_file:
    fieldnames = [
        'date',
        'code_departement',
        'libelle_departement',
        'code_region',
        'libelle_region',
        ]
    csvWriter = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csvWriter.writeheader()
    for departement_region_association in sorted(
            sorted(
                departement_region_associations,
                key=lambda association: association['date'],
                reverse=True),
            key=lambda association: association['code_departement']):
        csvWriter.writerow(departement_region_association)
