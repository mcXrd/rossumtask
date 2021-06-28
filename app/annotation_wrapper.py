import xmltodict


class Annotation:
    raw_str = None

    def __init__(self, raw_str: str):
        self.raw_str = raw_str
        self.dict_repr = xmltodict.parse(self.raw_str)
