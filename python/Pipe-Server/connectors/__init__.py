class AbstractConnector:
    def name(self):
        return "abstract_connector"

    def doEncoding(self):
        return False

    def process(self, **kwargs):
        return kwargs