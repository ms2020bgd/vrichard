import http
import sys

import wikipedia
from threading import Thread
import threading
import time
import numpy as np

# test = wikipedia.WikipediaPage(start_page)
# links = test.links
# print(start_page)
# print(links)


class LanceurAlerte(Thread):
    def __init__(self, titre):
        Thread.__init__(self)
        self.titre = titre

    def run(self):
        ChercheurPhilosophique(self.titre).start()
        while(event.is_set()):
            time.sleep(0.5)
        return


class ChercheurPhilosophique(Thread):
    def __init__(self, titre, compteur=0):
        Thread.__init__(self)
        self.titre = titre
        self.compteur = compteur
        self.setDaemon(True)

    def run(self):

        print(threading.active_count() < 151)
        trouver_philosophie(self.titre, self.compteur)

        return


def trouver_philosophie(titre_page, compteur=0):
    print(threading.active_count())
    try:
        wikiPage = wikipedia.WikipediaPage(titre_page)
    except wikipedia.exceptions.PageError:
        return("PageError")
    except wikipedia.exceptions.DisambiguationError:
        return ("DisambiguationError")
    compteur = compteur + 1
    for link in wikiPage.links:
        # if(any(link for elem in already_seen_list)):
        #     continue
        if (link == "Philosophie"):
            print("La page philosophie a été trouvé en " + str(compteur) + " saut de pages wikipedia")
            event.clear()
            return
        else:
            # with lock_already_seen_list:
            # already_seen_list.append(link)
            # print(link)
            # semaphore.release()
            semaphore.acquire()
            try:
                ChercheurPhilosophique(link, compteur).start()
            finally:
                semaphore.release()
    return


semaphore = threading.BoundedSemaphore(150)
# lock_already_seen_list = threading.Lock
# already_seen_list = ["init"]
event = threading.Event()
event.set()
wikipedia.set_lang('fr')
start_page = wikipedia.random()
print("La page de départ est : " + "Socrate")

thread_init = LanceurAlerte("Socrate")
thread_init.start()
# print(thread_init.is_alive())