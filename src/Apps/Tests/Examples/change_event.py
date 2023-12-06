import pathlib

from Tools.Pretix_API import Pretix_API

update_dict = {
                "name": {
                        "de": "Neuer Toller Name"
                        }
                }  


path = str(pathlib.Path(__file__).parent.resolve())



user = Pretix_API()
print(user.change_event("test1", update_dict))

