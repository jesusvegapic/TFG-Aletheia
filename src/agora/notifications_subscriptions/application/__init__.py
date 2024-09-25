import importlib

from lato import ApplicationModule

notifications_subscriptions_module = ApplicationModule("notifications_subscriptions")
importlib.import_module("src.agora.notifications_subscriptions.application.queries")
importlib.import_module("src.agora.notifications_subscriptions.application.commands")
