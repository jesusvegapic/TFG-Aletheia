import importlib

from lato import ApplicationModule

agora_teachers_module = ApplicationModule("agora_teachers_module")
importlib.import_module("src.agora.teachers.application.queries")
