import pathlib

from Tools.Pretix_API import Pretix_API

update_dict = {
                "name": {
                        "Yanniks Veranstaltung"
                        },
                }  


path = str(pathlib.Path(__file__).parent.resolve())



user = Pretix_API()
print(user.change_event("neu", update_dict))

