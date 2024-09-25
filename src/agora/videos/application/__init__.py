import importlib

from lato import ApplicationModule

agora_videos_module = ApplicationModule("videos")
importlib.import_module("src.agora.videos.application.queries")
