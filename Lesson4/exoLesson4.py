import requests
from bs4 import BeautifulSoup


def get_soup_from_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup


# Trouve les 10 villes de France les + peuplées
# (e.g https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peuplées)
def recuperation_des_villes():
    soup = get_soup_from_url("https://fr.wikipedia.org/wiki/Liste_des_communes_de_France_les_plus_peupl%C3%A9es")
    table_commune = soup.find('tbody')
    liste_ville = table_commune.findAll("tr")
    liste_ville_plus_peuple = []
    for i in range(10):
        ville = liste_ville[i + 1]
        nom_ville = ville.contents[3].text[:-1].replace("[19]", '')  # Replace pour Lille qui renvoie Lille[19]
        liste_ville_plus_peuple.append(nom_ville)
    return liste_ville_plus_peuple


# - Pour chaque ville, trouve sa distance avec les autres.
# - par exemple, avec google maps api (nécessite de s'authentifier / créer un token) avec
#   https://github.com/googlemaps/google-maps-services-python (cf. doc token dans le readme)
# - ou avec https://fr.distance24.org/ (pas besoin de s'authentifier)
def calcul_distance(list_ville):
    list_ville_tuple_ville_distance = []
    for ville_depart in list_ville:
        list_distance_ville = []
        for ville_arrive in list_ville:
            if ville_depart == ville_arrive:
                continue
            soup = get_soup_from_url("https://fr.distance24.org/" + ville_depart + "/" + ville_arrive)
            distance = soup.find('strong').text.split()[0]
            list_distance_ville.append((ville_arrive, distance))
        list_ville_tuple_ville_distance.append((ville_depart, list_distance_ville))
    return list_ville_tuple_ville_distance

#- Trouve les villes les plus proches
# Je trouve ici pour chaque ville quel autre ville est la plus proche j'avais compris l'énoncé comme cela
def trouve_ville_plus_proche(list_ville_tuple_ville_distance):
    list_output = []
    for ville, list_ville_distance in list_ville_tuple_ville_distance:
        list_ville_distance_sort = sorted(list_ville_distance, key=lambda x: x[1])
        list_output.append((ville, list_ville_distance_sort[0]))
    return list_output


liste_ville_plus_peuple = recuperation_des_villes()
list_ville_tuple_ville_distance = calcul_distance(liste_ville_plus_peuple)
print(trouve_ville_plus_proche(list_ville_tuple_ville_distance))
