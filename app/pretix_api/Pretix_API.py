import json

import requests


class Pretix_API():
    
    def __init__(self, organizer_url : str , token: str):
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
        response.raise_for_status()
        return response.json()

    
    def _handle_pagination(self, url):
        data = []
        while True:
            r = self.s.get(url, headers=self.authHeader)
            self._check_response(r)
            data.extend(r.json()["results"])
            
            if not r.json()["next"]:
                break
            url = r["next"]
        
        return data
    
    ### Events ###
    # GET Requests for Events
        
    def get_event(self, slug):
        r = self.s.get(f'{self.config["events_url"]}{slug}/', headers=self.authHeader)
        return self._check_response(r)

        
    def get_events(self):
        return self._handle_pagination(self.config["events_url"])
    
    
    # POST Requests for Events
    
    def create_event(self, file_path : str, update_dict = {}):
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
    
    
    def clone_event(self, event_slug : str, update_dict : dict):
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
    
    
    # Patch Events
    
    def change_event(self, event_slug : str, data : dict):
        r = self.s.patch(f'{self.config["events_url"]}{event_slug}/', data=data, headers=self.authHeader)
        return self._check_response(r)
    
    
    # Delete Events

    def delete_event(self, event_slug : str):
        r = self.s.delete(f'{self.config["events_url"]}{event_slug}/', headers=self.authHeader)
        return self._check_response(r)

    
    ### Orders ###
    # GET Requests for Orders
        
        
    def get_orders(self, slug : str, content : str, filter_by_item_id = None):
        orders = self._handle_pagination(self.config["events_url"] + slug+ "/orders?include_canceled_positions=true")
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
        
        raise Exception("Error : Wrong Content parameter")
        
    
    ### Items/Produkte ###
    # Get Items
    
    def get_items(self,event_slug :str):
        items = self._handle_pagination(self.config["events_url"] + event_slug+ "/items")
        return items
    
    
    # Patch Items
    
    def change_item(self, id : int, event_slug :str, update_dict : dict ):
        r = self.s.patch(f'{self.config["events_url"]}{event_slug}/items/{str(id)}/',update_dict,headers=self.authHeader)
        return self._check_response(r)
    
    
    ### Quotas/Kontingente ###
    
    def get_quotas(self, event_slug : str):
        quotas = self._handle_pagination(self.config["events_url"] + event_slug+  "/quotas/")
        return quotas
    
    def create_quota(self, event_slug: str, data : dict):
        r = self.s.post(f'{self.config["events_url"]}{event_slug}/quotas/' ,data,headers=self.authHeader )
        return self._check_response(r)
    
    def update_quota(self, event_slug : str, quota_id :int, update_dict : dict):
        r = self.s.patch(f'{self.config["events_url"]}{event_slug}/quotas/{quota_id}/', update_dict, headers=self.authHeader)

        return self._check_response(r)


