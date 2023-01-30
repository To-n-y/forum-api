import os

from starlette.config import Config
from starlette.datastructures import Secret

dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3] + "db\\"
print(root_dir)
print(dir_path)
config = Config(f"{dir_path[:-3]}.env")
DATABASE_URL = f"sqlite:///{root_dir}" + config(
    "DB_NAME", cast=str, default=os.getenv("DB_NAME", "db.sqlite")
)
print(DATABASE_URL)

SECRET_KEY = config(
    "SECRET_KEY", cast=Secret, default=os.getenv("SECRET_KEY", "secret")
)
