import pathlib

from Tools.Pretix_API import Pretix_API

path = str(pathlib.Path(__file__).parent.resolve())

update_dict = {
    "name" : "LaPfiLa Anmeldung - Stamm Weiße Kothe",
    "slug" : "weissekothe",
    "date_from": "2024-06-17T00:00:00+02:00",
    "date_to": "2024-06-20T00:00:00+02:00"


                }  



user = Pretix_API()

print(user.clone_event("lapfila", update_dict))