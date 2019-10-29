import pandas as pd
import requests
import numpy as np
import string

#Check for currency after the price
def has_currency(price):
    priceSplit = price.split(" ")
    if(len(priceSplit) == 2):
        return priceSplit[1]
    else:
        return None

#Get the currency from the API freegeoip
def get_eur_price(row, currency_country, euro_rate):
    locationIp = requests.get("https://freegeoip.app/json/" + row["ip_address"])
    #Check if ip exist
    if (locationIp.status_code == 200):
        locationIp = locationIp.json()
    else:
        return row
    if (locationIp["country_code"] == ""):
        return row
    else:
        if (row["currency"] is None):
            row["currency"] = currency_country[locationIp["country_code"]]
        if(row["currency"] == "EUR"):
            row["price_eur"] = row["price"]
        #Non used currency anymore
        elif (row["currency"] == "BYR"):
            return row
        else:
            row["price_eur"] = row["price"] * euro_rate[row["currency"].lower()]["inverseRate"]
    return row

#################### PART 1  ######################
# - On aimerait avoir une colonne de prix unifiés en euros.
#     Problème: la currency n'est pas indiquée pour tous les produits: il va falloir essayer de "deviner" les currency
#     manquantes, en se basant sur l'adresse IP de l'utilisateur.
#Read data
data = pd.read_csv("products.csv", ";")
#Json of country to Currency
currency_country = pd.read_json("currency.json", typ='series')
#Rate of curency in euro
euro_rate = pd.read_json("eur.json")
#Separate the currency in a new col and reformat price
data["currency"] = data["price"].apply(has_currency)
data["price"] = data["price"].apply(lambda price: price.split(" ")[0])
#Prepare dataframe for calculation of the price output
data["price_eur"] = None
data = data.astype({'price_eur': np.float, 'price': np.float})
#Calculate price in euro
data = data.apply(lambda row: get_eur_price(row, currency_country, euro_rate), axis=1)

#On peut enlever les partie n'ayant pas de prix en euro
data = data.dropna(subset=["price_eur"])

################## PART 2 ###########################
#- La colonne "infos" liste des ingrédients présents dans le produit.
# On préfèrerait avoir une colonne de type bool par ingrédient, indiquant si le produit contient ou non cet ingrédient.

#Remise en forme de la colonne infos
data.infos = data.infos.str.lower()
data.infos = data.infos.str.replace(',', '')
data.infos = data.infos.str.replace(':', '')
#Separation des termes de info et creation d'un nouveau dataframe contenant cette liste
data.infos = data.infos.str.split()
#FlatMap de notre dataframe sur tous les éléments de infos
data_infos_product = data.explode("infos")["infos"]
#Creation de nouvelles colonnes pour chaque element différent de infos
data_infos_product = pd.get_dummies(data_infos_product, columns=["infos"])
#Group by sur notre index
data_infos_product = data_infos_product.groupby(level=0).sum()
#Drop des colonnes ne contenants pas d'ingrédient
data_infos_product = data_infos_product.drop(["may","and","contain","contains","ingredients"], axis=1)
#Recupération de la table annexe dans notre DataFrame initial
data = data.join(data_infos_product)

print(data.head())
