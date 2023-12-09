import pathlib

from Tools.Pretix_API import Pretix_API

path = str(pathlib.Path(__file__).parent.resolve())

update_dict = {
    "name" : "neueer Name",
    "slug" : "neu",
    "date_from": "2017-12-27T10:00:00Z",

                }  



user = Pretix_API()

print(user.clone_event("test", update_dict))