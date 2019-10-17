class Appearance:
    def __init__(self, doc_index, name, frequency):
        self.docIndex = doc_index
        self.name = name
        self.frequency = frequency

    def __repr__(self):
        return str(self.__dict__)