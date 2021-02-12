from gsurface.serialize.functions import save, load


# caller = __file__
def save_attached(obj, caller: str):
    filename = caller + ".json"
    save(filename, obj, 4)
    return load(filename)