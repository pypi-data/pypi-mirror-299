from .INIKeywords import INILibrary
from robot.api.deco import library

@library(scope="GLOBAL", version="1.0.1")
class INILibrary(INILibrary):
    pass