import pandas as pd
import requests
import datetime

key =""

data = pd.read_csv("people_clean.csv")

#- mettre la colonne `inactive` à `true` pour tous les users dont le `last_seen` date d'au moins un an
data['last_seen'] = pd.to_datetime(data.last_seen)
data["inactive"] = data["last_seen"]  < (datetime.datetime.now() - datetime.timedelta(days=365))
#- avec une regex: filtrer les numéros de téléphone invalides
data.phone = data.phone[data.phone.str.contains('^0\d{9}$', na=False)]
#- ajouter une colonne indiquant si le numéro de tel correspond à un téléphone portable (06/07)
data["is_mobile"] = data.phone.str.contains('^0[67]', na=False)
#- ajouter une colonne indiquant si les coordonnées GPS de l'utilisateur correspondent bien au "country"
data["check_gps"] = None
def check_gps(row):
    request = requests.get("https://api.opencagedata.com/geocode/v1/json?q="+str(row["lat"])+"+"+str(row["lon"])+"&key="+key).json()
    country = request["results"][0]["components"]["country"]
    if (country == "PRC"):
        country = "China"
    if(country == row["country"]):
        row["check_gps"] = 1
    else:
        row["check_gps"] = 0
    return row

data = data.apply(check_gps, axis=1)
