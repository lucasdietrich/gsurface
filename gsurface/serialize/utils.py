from gsurface.serialize.functions import save, load


# caller = __file__
def save_attached(obj, caller: str):
    filename = caller + ".json"
    try:
        save(filename, obj, 4)
    except Exception as e:
        print("Failed to serialize object : ", e)
        return False

    try:
        l = load(filename)
    except Exception as e:
        print("Failed to parse serialized object : ", e)
        return None

    return l