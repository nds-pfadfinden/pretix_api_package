import json

import requests


class Pretix_API():
    
    def __init__(self, organizer_url : str , api_token: str) -> None:
        """        
        Args:
        events_url (String) -> Url for the Pretix-Organizer (default from .env file)
        api_token (String) -> API Token for the Pretix-Organizer (default from .env file)
        """

        self.s = requests.Session()
        self.config = {
            'organizer_url': organizer_url,
            'events_url' : f'{organizer_url}events/'
        }
        self.authHeader = {
            "Authorization": f'Token {api_token}',
                    "Content-Type": "application/json"
        }
        self.s.headers.update(self.authHeader)
        

    def __del__(self) -> None:
        self.s.close()
        return


    def _check_response(self, response):
        response.raise_for_status()
        return response.json()

    
    def _handle_pagination(self, url):
        data = []
        while True:
            r = self.s.get(url)
            self._check_response(r)
            data.extend(r.json()["results"])
            
            if not r.json()["next"]:
                break
            url = r.json()["next"]
        
        return data
    
    ### Events ###
    # GET Requests for Events
        
    def get_event(self, slug):
        r = self.s.get(f'{self.config["events_url"]}{slug}/')
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
        
        r = self.s.post(self.config["events_url"], json=data)
    
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
                        json=update_dict
                        )
    
        return self._check_response(r)
    
    
    # Patch Events
    
    def change_event(self, event_slug : str, data : dict):
        r = self.s.patch(f'{self.config["events_url"]}{event_slug}/', json=data)
        return self._check_response(r)
    
    
    # Delete Events

    def delete_event(self, event_slug : str):
        r = self.s.delete(f'{self.config["events_url"]}{event_slug}/')
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
    # GET Items
    
    def get_items(self,event_slug :str):
        items = self._handle_pagination(self.config["events_url"] + event_slug+ "/items")
        return items
    
    
    # Patch Items
    
    def change_item(self, id : int, event_slug :str, update_dict : dict ):
        r = self.s.patch(f'{self.config["events_url"]}{event_slug}/items/{str(id)}/',json=update_dict)
        return self._check_response(r)
    
    
    ### Quotas/Kontingente ###
    
    def get_quotas(self, event_slug : str) -> list:
        quotas = self._handle_pagination(self.config["events_url"] + event_slug+  "/quotas/")
        return quotas
    
    def create_quota(self, event_slug: str, data : dict):
        r = self.s.post(f'{self.config["events_url"]}{event_slug}/quotas/' ,json=data )
        return self._check_response(r)
    
    def update_quota(self, event_slug : str, quota_id :int, update_dict : dict):
        r = self.s.patch(f'{self.config["events_url"]}{event_slug}/quotas/{quota_id}/', json=update_dict)
        return self._check_response(r)

    ### Invoices/Rechnungen ###
    
    # GET Invoices
    
    def get_invoices(self, event_slug : str) -> list[dict]:
        invoices = self._handle_pagination(self.config["events_url"] + event_slug+  "/invoices/")        
        return invoices
    
    
    def download_invoice(self, event_slug : str, invoice_number : str, path : str, invoice_filename = "") -> None:
        if invoice_filename == "":
            invoice_filename = invoice_number
        
        invoice_pdf_r = self.s.get(f'{self.config["events_url"]}{event_slug}/invoices/{invoice_number}/download/' )
        with open(path + f"\\{invoice_filename}.pdf", "wb") as f:
            f.write(invoice_pdf_r.content)
            
        return
            
    
    def download_all_invoices(self, event_slug : str, path: str) -> None:
        invoices = self.get_invoices(event_slug)
        for invoice in invoices:
            self.download_invoice(event_slug, invoice["number"], path)
            
        return