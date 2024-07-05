import importlib

from lato import ApplicationModule

faculties_module = ApplicationModule("faculties")
importlib.import_module("src.akademos.faculties.application.queries")
importlib.import_module("src.akademos.faculties.application.commands")