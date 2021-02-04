import toml

from toml import TomlEncoder

with open('./model.toml', 'r') as fp:
    obj = toml.load(fp)

print(obj)