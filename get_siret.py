# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 11:11:32 2022

@author: pierr
"""
import requests

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer 600bdba2-5faa-33df-8c8c-c3532dfe6585',
}

#parcourir une liste de codes NAF
codeNaf = '13.95Z'
#parcourir une liste de départements (en 1er)
departement = '69'

response = requests.get('https://api.insee.fr/entreprises/sirene/V3/siret?q=activitePrincipaleUniteLegale%3A' + codeNaf +'AND%20codeCommuneEtablissement%3A' + departement + '*', headers=headers)