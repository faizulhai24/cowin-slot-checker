import os
import importlib

ENVIRONMENT = os.getenv('ENVIRONMENT')

if not ENVIRONMENT:
    try:
        from .local import *
    except ImportError as exc:
        try:
            from .common import *
        except ImportError as exc:
            raise Exception('Environment not defined and local settings not found')
else:
    importlib.import_module(
        "skynet_v2.settings.{mname}".format(mname=ENVIRONMENT)
    )