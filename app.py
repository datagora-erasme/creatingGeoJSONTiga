# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 11:21:38 2022

@author: pierr
"""

import requests
import flask
import re
import time
import json

def get_interesting_naf_codes():
    """Fonction qui permet de récupérer les codes NAF qui nous intéresent pour les requêter à l'API"""
    codes_naf = []
    codes_sp = []
    definitions = []
    dico_naf = {}
    # ursl contient les urls des blocks à analyser =
    urls = [
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#cca152a983b148bbb4ef4323a4cbeb50",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#3258f0238d2847a0a5d5c17215893ecc",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#ff3f205c57e743bcbb1fd3b3f06abc4e",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#f499d30971934fe19aeeaf26747f8f39",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#6ce53a54a2bd4256afbaf077fbba9d1e",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#7cd489356fb5478283124624cd5b9b4d",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#20bffa6fd5124de69cca9d4a6fffd482",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#b0d7ef12ffd04774b8e077604ee6970c",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#218a03f964734edca85da19d766dc826",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#3e6ba423acf24ee0b5b3a3254c23f3f4",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#f3053073078e423ab26535febf14945d",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#d33b3788699f44b086a419d3eb0a6bc7",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#ebb8dd6dd5954002bb62c03781ad58e7",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#b7c9a63139c04c89a86f4c052fe0f8e9",
        "https://www.notion.so/Atelier-nouveaux-usages-ff2ffa13eeb94d91a2d672d56b62be0a-5198447ed79746c590da4c3c9cb0cc81#b8cece22716a454796414766c310fc2c"]
    
    for url in urls:
        block_id = url[112:]
        print(block_id)
        url = f"https://api.notion.com/v1/blocks/{block_id}"
    
        headers = {
        
            "Accept": "application/json",
        
            "Notion-Version": "2022-02-22",
        
            "Authorization": "Bearer secret_VyB7EbB3zAW0SVcGE1UfuMQc80uQ1vrlurKHbMnxalK"
        
        }
        
        response = requests.get(url, headers=headers)
        
        print(response.text)
        
        text = response.text
        pattern = "\d\d\d\d[A-Z]"
        a = re.findall("\d\d\d\d[A-Z]", text)
        a = a[:(len(a)//2)]
        print(a)
        definition = re.findall("\((.*?)\)", text)
        definition = definition[:(len(definition)//2)]
        definition = definition[1:]
        print("Définitions : ", definition)
        definitions += definition
        
        # parcourir a pour construire le dico
        for code in a:
            # get_definition of NAF
            i = text.index(code)
            print("indice de debut", i)
            codes_sp.append(code)
            code_naf = code[0:2] + '.' + code[2:]
            codes_naf.append(code_naf)
            
    """save the list of NAF codes in order to reuse it later"""
    with open("interesting_naf_codes.txt", "w") as f:
        for i in range(len(codes_sp)):
            f.write(codes_sp[i])
            #ajout de l'écriture f.write(',' + definition)
            f.write(';/ ')
            f.write(definitions[i])
            f.write('\n')
    
    return codes_sp, definitions

def get_entreprises(codes_naf, departements):
    
    begin = 0
    geo_entr  = dict(type='FeatureCollection')
    geo_entr['features'] = []
    
    """fonction qui prend en compte les codes NAF qui nous intéressent et renvoie les données sur les industries qui nous intéressent"""
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer 600bdba2-5faa-33df-8c8c-c3532dfe6585',
    }
    curseur = '*'
    maxi = 100
    compte = False
    for departement in departements:
        for code_naf in codes_naf:  
            # on peut demander au maximum 1000 entreprises à la fois
            response = requests.get('https://api.insee.fr/entreprises/sirene/V3/siret?q=activitePrincipaleUniteLegale%3A'+code_naf+'%20AND%20codeCommuneEtablissement%3A'+departement+'*&nombre=1000&curseur='+curseur, headers=headers)
            if response.ok:
                if compte:
                    t1 = time.time()
                    print("temps écoulé : ", t1-t0)
                    compte = False
                # print("Curseur = ", curseur)
                # print(response)
                # print(response.json())
                curseur = response.json()['header']['curseurSuivant']
                etablissements = response.json()['etablissements']
                
                for etablissement in etablissements:
                    # c'est ici qu'il faut construire le GeoJSON
                    feature = dict(type='Feature')
                    # adresse
                    feature["properties"] = {}
                    feature["properties"]["siren"] = etablissement['siren']
                    feature["properties"]["siret"] = etablissement['siret']
                    feature["properties"]["trancheEffectifsEtablissement"] = etablissement["trancheEffectifsEtablissement"]
                    feature["properties"]["nom"] = etablissement['uniteLegale']["denominationUniteLegale"]
                    
                    #faire le geocodage de l'adresse
                    #geocodage avec l'API gouvernement
                    print(response)
                    adresse = list(etablissement['adresseEtablissement'].values())
                    str_adresse = ' '.join(filter(None,adresse))
                    feature["properties"]["adresse"] = str_adresse
                    params = {
                        'q': str_adresse,
                        'limit': '1',
                    }
                    
                    response = requests.get('https://api-adresse.data.gouv.fr/search/', params=params)
                    try:
                        feature["geometry"] = response.json()['features'][0]['geometry']
                    except:
                        pass
                    
                    geo_entr['features'].append(feature)
                    begin+=1
                    print(begin)
                    if begin > maxi:
                        break
            if not response.ok and not compte:
                print("Réponse : ", response)
                # début du compte à rebours
                compte = True
                t0 = time.time()
                # print("début compte", t0)
            if begin > maxi:
                print('stop')
                break
        if begin > maxi:
            print('stop')
            break
    return geo_entr

def test():
    
    #exemple pour lequel il n'y a que 25 solutions afin de voir ce que le curseur dit quand on arrive au bout
    departement = '69'
    code_naf = '35.11Z'
    curseur = '*'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer 600bdba2-5faa-33df-8c8c-c3532dfe6585',
    }
    
    response = requests.get('https://api.insee.fr/entreprises/sirene/V3/siret?q=activitePrincipaleUniteLegale%3A'+code_naf+'%20AND%20codeCommuneEtablissement%3A'+departement+'*%20AND%20denominationUniteLegale%3ACa*&nombre=1000&curseur='+curseur, headers=headers)
    adresse = list(response.json()['etablissements'][0]['adresseEtablissement'].values())
    
    str_adresse = ' '.join(filter(None,adresse))
    
    curseur = response.json()['header']["curseurSuivant"]
    
    #OK donc il faut juste tester si curseur = curseurSuivant !!
        
    pass

def get_adresse_from_dic(dic):
    adresse={'complementAdresseEtablissement': None,
     'numeroVoieEtablissement': '46',
     'indiceRepetitionEtablissement': None,
     'typeVoieEtablissement': 'AV',
     'libelleVoieEtablissement': 'HENRI RENARD',
     'codePostalEtablissement': '80120',
     'libelleCommuneEtablissement': 'QUEND',
     'libelleCommuneEtrangerEtablissement': None,
     'distributionSpecialeEtablissement': None,
     'codeCommuneEtablissement': '80649',
     'codeCedexEtablissement': None,
     'libelleCedexEtablissement': None,
     'codePaysEtrangerEtablissement': None,
     'libellePaysEtrangerEtablissement': None}

    
if __name__ == '__main__':
    NAFs = get_interesting_naf_codes()
    # departements = ['01', '38', '42', '69', '71']
    # geo = get_entreprises(NAFs, departements)
    
    # with open('geo_entreprises.json', 'w') as fp:
    #     json.dump(geo, fp)
    