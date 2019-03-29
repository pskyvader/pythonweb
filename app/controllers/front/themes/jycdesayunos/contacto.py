from app.models.texto import texto
from core.app import app
from core.functions import functions
from core.view import view


class contacto(base):
    def __init__(self):
        super().__init__(app.get["idseo"])

    def index(self):
        ret = {"body": []}
        self.meta(self.seo)

        var = {}
        if self.seo["tipo_modulo"] != 0:
            var["tipo"] = self.seo["tipo_modulo"]

        if self.modulo["hijos"]:
            var["idpadre"] = 0

        row = seccion_model.getAll(var)

        if len(row) > 0:
            self.url = functions.url_seccion([self.url[0], "detail"], row[0], True)

        url_return = functions.url_redirect(self.url)
        if url_return != "":
            ret["error"] = 301
            ret["redirect"] = url_return
            return ret

        h = head(self.metadata)
        ret_head = h.normal()
        if ret_head["headers"] != "":
            return ret_head
        ret["body"] += ret_head["body"]

        he = header()
        ret["body"] += he.normal()["body"]

        ba = banner()
        ret["body"] += ba.individual(
            self.seo["banner"], self.metadata["title"], self.seo["subtitulo"]
        )["body"]

        bc = breadcrumb()
        ret["body"] += bc.normal(self.breadcrumb)["body"]

        data = {}

        campos = []
        campos.append(
            {
                "campo": "input",
                "type": "text",
                "field": "nombre",
                "title": "Nombre",
                "required": True,
            }
        )
        campos.append(
            {
                "campo": "input",
                "type": "email",
                "field": "email",
                "title": "Email",
                "required": True,
            }
        )
        campos.append(
            {
                "campo": "input",
                "type": "text",
                "field": "telefono",
                "title": "Teléfono",
                "required": False,
            }
        )
        campos.append(
            {
                "campo": "input",
                "type": "file",
                "field": "archivo",
                "title": "Archivo",
                "required": False,
            }
        )
        campos.append(
            {
                "campo": "textarea",
                "type": "text",
                "field": "mensaje",
                "title": "Comentario",
                "required": True,
            }
        )

        data["campos"] = campos

        informacion = []
        textos = texto.getAll({"tipo": 1})
        for t in textos:
            icono = ""
            link = ""
            if t[0] == 1:
                icono = "fa-phone"
                link = "tel:" + t["texto"]
            elif t[0] == 2:
                icono = "fa-envelope-o"
                link = "mailto:" + t["texto"]
            elif t[0] == 6:
                icono = "fa-map-marker"
            informacion.append(
                {"icono": icono, "title": t["titulo"], "text": t["texto"], "url": link}
            )

        data["informacion"] = informacion
        data["texto_contacto"] = functions.remove_tags(texto.getById(7)["descripcion"])
        data["title"] = self.seo["titulo"]
        data["action"] = functions.generar_url(["enviar"])

        mapa = texto.getById(8)
        data["is_mapa"] = mapa["estado"]
        data["lat"] = mapa["mapa"]["lat"]
        data["lng"] = mapa["mapa"]["lng"]
        data["title_map"] = mapa["titulo"]
        data["direccion"] = mapa["mapa"]["direccion"]

        config = app.get_config()
        data["googlemaps_key"] = config["googlemaps_key"]
        data["google_captcha"] = config["google_captcha"]

        ret["body"].append(("contact", data))

        f = footer()
        ret["body"] += f.normal()["body"]
        return ret

