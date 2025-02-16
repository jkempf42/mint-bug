import azure.functions as func
import datetime
import importlib
import json
import logging


def enter_darth_vader(name):
    return func.HttpResponse(f"{name} should have caused an error by now.",
                             status_code=500
                        )
