import importlib

from lato import ApplicationModule

akademos_courses_module = ApplicationModule("akademos_courses")
importlib.import_module("src.akademos.courses.application.commands")
