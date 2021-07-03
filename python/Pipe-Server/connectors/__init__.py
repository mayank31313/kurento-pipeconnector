class AbstractConnector:
    def name(self):
        return "abstract_connector"

    def process(self, **kwargs):
        return kwargs