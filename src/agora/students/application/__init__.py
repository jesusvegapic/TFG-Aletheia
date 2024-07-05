import importlib

from lato import ApplicationModule

students_module = ApplicationModule("students")
importlib.import_module("src.agora.students.application.queries")
importlib.import_module("src.agora.students.application.commands")
