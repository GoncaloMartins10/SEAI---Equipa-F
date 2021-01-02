class AttributeException(Exception):
    def __init__(self, message=None):
        self.message = self.message if message!=None else self.__class__.__name__
        super.__init__(self.message)

