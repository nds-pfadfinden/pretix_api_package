import pathlib

from Tools.Pretix_API import Pretix_API

path = str(pathlib.Path(__file__).parent.resolve())


user = Pretix_API()

print(user.create_event(path+"\\event_blueprint.json"))