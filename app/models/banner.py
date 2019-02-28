from core.database import database
from .base_model import base_model
from core.app import app
from core.functions import functions


class banner(base_model):
    idname = 'idbanner'
    table = 'banner'