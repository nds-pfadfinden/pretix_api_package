import pathlib

from Tools.Pretix_API import Pretix_API

update_dict = {
               "currency": "EUR"
                }  


path = str(pathlib.Path(__file__).parent.resolve())



user = Pretix_API()
print(user.change_event("test", update_dict))

