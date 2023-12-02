import json
import pathlib

from Tools.Pretix_API import Pretix_API

path = str(pathlib.Path(__file__).resolve())

user = Pretix_API()
data = user.getEvent()

with open(path + 'output.json', 'w') as f:
    json.dump(data,f, ensure_ascii=False, indent=4)
