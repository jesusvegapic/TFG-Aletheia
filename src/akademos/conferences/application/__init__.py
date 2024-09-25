import importlib

from lato import ApplicationModule

akademos_conferences_module = ApplicationModule("akademos_conferences")
importlib.import_module("src.akademos.conferences.application.commands")

