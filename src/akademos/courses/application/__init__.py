import importlib

from lato import ApplicationModule

courses_module = ApplicationModule("courses")
importlib.import_module("src.akademos.courses.application.commands")
