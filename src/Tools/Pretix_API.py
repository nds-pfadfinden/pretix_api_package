import json

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
            'events_url' : f'{organizer_url}events/'
        }
        self.authHeader = {
            "Authorization": f'Token {token}'
        }
        


    def __del__(self):
        self.s.close()

    def _check_response(self, response):
        if response.status_code not in [200,201]:
            #print(response.json())
            raise ValueError(response.status_code)
        return response.json()

    
    
    # GET Requests
    def _handle_pagination(self, url):
        data = []
        while True:
            r = self.s.get(url, headers=self.authHeader)
            self._check_response(r)
            data.extend(r.json()["results"])
            
            print(data)

            if not r.json()["next"]:
                break
            url = r["next"]
        
        return data
    
    def get_event(self, slug):
        r = self.s.get(f'{self.config["events_url"]}{slug}/', headers=self.authHeader)
        return self._check_response(r)

        
    def get_events(self):
        return self._handle_pagination(self.config["events_url"])
        
    def get_orders(self, slug, content, filter_by_item_id = None):
        orders = self._handle_pagination(self.config["events_url"] + slug+ "/orders")
        if content == "orders":
            return orders
        
        
        positions = []
        for  o in orders:
            positions.extend(o["positions"])
        if filter_by_item_id:
            positions = list(filter(lambda a: a["item"] in filter_by_item_id, positions))
        if content == "positions":
            return positions
        
        answers = []
        for  p in positions:
            answers.extend(p["answers"])
        if content == "answers":
            return answers
        
        raise Exception("Error : Wrong Content")
        

    # POST Requests
    def create_event(self, file_path, update_dict = {}):
        """
        method to create Events
        
        can't create plugins or saleschannels

        Args:
            file_path (String): path to json file with object to create an event
            update_dict (dict, optional): dict to update the json object.  Defaults to {}.

        Returns:
            response status
        """
        
        
        with open(file_path, "r") as read_file:
            data = json.load(read_file)
        data.update(update_dict)
        
        r = self.s.post(self.config["events_url"], data=data, headers=self.authHeader)
    
        return self._check_response(r)
    
    
    
    def clone_event(self, event_slug, update_dict):
        """
        method to Clone Events

        Args:
            file_path (String): path to json file with object to create an event
            update_dict (dict, optional): dict to update the json object.  Defaults to {}.

        Returns:
            response status
        """
        
        
        r = self.s.post(
                        url=f'{self.config["events_url"]}{event_slug}/clone/',
                        data=update_dict,
                        headers=self.authHeader
                        )
    
        return self._check_response(r)


    # Patch Requests
    
    def change_event(self, event_slug,data):

        print(f'{self.config["events_url"]}{event_slug}')
        
        r = self.s.patch(f'{self.config["events_url"]}{event_slug}', data=data, headers=self.authHeader)
        
        return self._check_response(r)

    
    # Delete Requests

    def delete_event(self,event_slug):
        r = self.s.delete(f'{self.config["events_url"]}{event_slug}', headers=self.authHeader)
        return self._check_response(r)




    # output
    def print_to_file(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data,f, ensure_ascii=False, indent=4)
        
