import pathlib

from Tools.Pretix_API import Pretix_API

path = str(pathlib.Path(__file__).parent.resolve())



user = Pretix_API()
answers = user.get_orders("lapfila", "positions", [11])


user.print_to_file(path+"\\get_orders.json", answers)
