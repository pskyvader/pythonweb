from .base_model import base_model
from core.database import database
from core.app import app
import json


class sitemap(base_model):
    idname = 'idsitemap'
    table = 'sitemap'