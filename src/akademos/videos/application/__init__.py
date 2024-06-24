import importlib

from lato import ApplicationModule

videos_module = ApplicationModule("videos")
importlib.import_module("src.akademos.videos.application.events")
