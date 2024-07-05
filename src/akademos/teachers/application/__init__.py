import importlib

from lato import ApplicationModule

teachers_module = ApplicationModule("teachers")
importlib.import_module("src.akademos.teachers.application.commands")
