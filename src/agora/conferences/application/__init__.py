import importlib

from lato import ApplicationModule

agora_conferences_module = ApplicationModule("agora_conferences")
importlib.import_module("src.agora.conferences.application.queries")
