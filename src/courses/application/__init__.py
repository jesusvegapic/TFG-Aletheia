import importlib

from lato import ApplicationModule

courses_module = ApplicationModule("courses")
importlib.import_module("src.courses.application.commands")
