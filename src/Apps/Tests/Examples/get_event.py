import pathlib

from Tools.Pretix_API import Pretix_API

path = str(pathlib.Path(__file__).parent.resolve())



user = Pretix_API()
data = user.get_event("lapfila")

user.print_to_file(path+"\\get_event.json", data)
