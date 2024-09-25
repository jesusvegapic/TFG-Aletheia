import importlib

from lato import ApplicationModule

agora_courses_module = ApplicationModule("agora_courses")
importlib.import_module("src.agora.courses.application.queries")
