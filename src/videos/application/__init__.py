import importlib

from lato import ApplicationModule

videos_module = ApplicationModule("videos")
importlib.import_module("src.videos.application.events")
