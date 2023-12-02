
from socketserver import ThreadingTCPServer

import requests
from decouple import config as c


class API():
    def __init__(self):
        """
        Initialization with token from .env file
        """

        self.s = requests.Session()
        self.config = {
            'events_url': 'https://anmeldung.bundeslager.pfadfinden.de/api/v1/organizers/Bula22/events/',
        }
        self.allEvents = []
        self.authHeader = {
            "Authorization": f'Token {c("TOKEN")}'
        }

    def __del__(self):
        self.s.close()

    def _check_response(self, response):
        if response.status_code != 200:
            raise ValueError(response.status_code)
        return response.json()

    def getEvent(self):
        url = f'{self.config["events_url"]}'
        r = self.s.get(url, headers=self.authHeader)

        return self._check_response(r)

    def getOrders(self, slug, url):

        r = self.s.get(url, headers=self.authHeader)
        return self._check_response(r)
