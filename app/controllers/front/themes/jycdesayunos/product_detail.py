from core.image import image


class product_detail:
    producto = None
    url = []

    def __init__(self, producto, url):
        self.producto = producto
        self.url = url

    def galeria(recorte="foto1"):
        lista_imagenes = []
        thumb = []
        for foto in self.producto["foto"]:
            li = {"srcset": []}
            th = {}
            # li['title'] = this->producto['titulo']
            li["image"] = image.generar_url(foto, recorte)
            li["thumb"] = th["thumb"] = image.generar_url(foto, "cart")
            th["url"] = image.generar_url(foto, "")
            src = image.generar_url(foto, recorte, "webp")
            if src != "":
                li["srcset"].append({"media": "", "src": src, "type": "image/webp"})

            if li["image"] != "":
                lista_imagenes.append(li)
                thumb.append(th)

        data = {}
        data["lista_imagenes"] = lista_imagenes
        data["thumb"] = thumb
        return data

