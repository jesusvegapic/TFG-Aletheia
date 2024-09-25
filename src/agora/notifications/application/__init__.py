import importlib

from lato import ApplicationModule

notifications_module = ApplicationModule("notifications")
importlib.import_module("src.agora.notifications.application.events")
