from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool

def get_soup_from_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    return soup

def scrap_list_of_contributor():
    soup = get_soup_from_url("https://gist.github.com/paulmillr/2657075")
    contributor_list = []

    table_contributor = soup.find('tbody')
    contributorListScrapped = table_contributor.findAll('tr')
    for contributor in contributorListScrapped:
        contributor_dict = {}
        # Recupération du row
        tr = contributor.contents[1]
        row = tr.contents[0][1:]

        td = contributor.contents[3]
        # Recuperation du nom du contributeur si présent
        name = ""
        if (len(td.contents) >= 2):
            name = td.contents[1][2:-1]
        # Récupération du lien de la page des contributeurs
        url = td.contents[0].attrs["href"]
        #Recuperation du username
        username = td.contents[0].contents[0]
        #Creation du dictionnaire
        contributor_dict["row"] = row
        contributor_dict["name"] = name
        contributor_dict["url"] = url
        contributor_dict["username"] = username
        contributor_list.append(contributor_dict)
    return contributor_list

def calcul_mean_star_contributor(contributor):
    headers = {'Authorization': "Token b1bafc078cd31eb8226cff0fff161fc92017c386"}
    contributor["meanStar"] = 0.0
    print(contributor["row"])
    git_repos = requests.get("https://api.github.com/users/" + contributor["username"] + "/repos", headers=headers).json()
    star_repo = 0
    for repo in git_repos:
        star_repo += repo["stargazers_count"]
    if len(git_repos.json()) != 0:
        contributor["meanStar"] = star_repo / len(git_repos)
    return contributor

def get_repos(contributor_list):
    for contributor in contributor_list:
        calcul_mean_star_contributor(contributor)
    return contributor_list

def comparator(contributor_dict):
    return contributor_dict["meanStar"]

contributor_list = scrap_list_of_contributor()
# contributor_list = get_repos(contributor_list)
p = Pool(processes=4)
contributor_list = p.map(calcul_mean_star_contributor, contributor_list)
contributor_list.sort(key=comparator)
print(contributor_list)


import unittest

class EcoGithubTest(unittest.TestCase):
    def test_comparator(self):
        contributor_list = [
            {
                "row":"1",
                "name":"aaa",
                "url":"",
                "username":"aaa",
                "meanStar": 22
            },
            {
                "row": "2",
                "name": "bbb",
                "url": "",
                "username": "bbb",
                "meanStar": 2
            },
            {
                "row": "3",
                "name": "ccc",
                "url": "",
                "username": "ccc",
                "meanStar": 40}
        ]
        contributor_list.sort(key=comparator)
        # We should have found 3 products:
        self.assertEqual(contributor_list[0]["name"], "bbb")
        self.assertEqual(contributor_list[1]["name"], "aaa")
        self.assertEqual(contributor_list[2]["name"], "ccc")


def run_tests():
    test_suite = unittest.makeSuite(EcoGithubTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)


if __name__ == '__main__':
    run_tests()


