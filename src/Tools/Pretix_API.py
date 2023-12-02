
import requests
from decouple import config as c


class Pretix_API():
    def __init__(self, organizer_url = c("organizer_url"), token= c("TOKEN")):
        """        
        Args:
        events_url (String) -> Url for the Pretix-Organizer (default from .env file)
        token (String) -> API Token for the Pretix-Organizer (default from .env file)
        """

        self.s = requests.Session()
        self.config = {
            'organizer_url': organizer_url,
        }
        self.authHeader = {
            "Authorization": f'Token {token}'
        }

    def __del__(self):
        self.s.close()

    def _check_response(self, response):
        if response.status_code != 200:
            raise ValueError(response.status_code)
        return response.json()

    
    
    # GET Requests
    
    def getEvents(self):
        events_url = self.config["organizer_url"] + "events/"
        r = self.s.get(events_url, headers=self.authHeader)
        return self._check_response(r)

    def getOrders(self, url):
        r = self.s.get(url, headers=self.authHeader)
        return self._check_response(r)
    
    
    
    # POST Requests
    
    
    
    
    
    
    
