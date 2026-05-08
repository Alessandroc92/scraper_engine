import extruct


class JsonLdParser:
    def __init__(self, html: str):
        self.html = html

    def extract(self):
        jslde = extruct.jsonld.JsonLdExtractor()
        return jslde.extract(self.html)