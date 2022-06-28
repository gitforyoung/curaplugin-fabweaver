from . import FabWeaver

def getMetaData():
    return {}

def register(app):
    return {"extension": FabWeaver.FabWeaver()}