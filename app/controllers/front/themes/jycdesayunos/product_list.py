from .base import base

from core.app import app
from core.functions import functions


class product_list(base):
    view = "grid"
    order = "orden"
    search = ""
    page = 1
    limit = 6
    count = 0

    def __init__(self):
        super().__init__(app.idseo)

        self.view = (
            "list" if "view" in app.get and app.get["view"] == "list" else "grid"
        )
        self.order = (
            functions.remove_tags(app.get["order"]).strip()
            if "order" in app.get and app.get["order"] != ""
            else "orden"
        )
        self.search = (
            functions.remove_tags(app.get["search"]).strip()
            if "search" in app.get
            else ""
        )
        self.page = (
            int(functions.remove_tags(app.get["page"]).strip())
            if "page" in app.get and app.get["page"] != ""
            else 1
        )
        self.limit = (
            int(functions.remove_tags(app.get["limit"]).strip())
            if "limit" in app.get and app.get["limit"] != ""
            else 6
        )

