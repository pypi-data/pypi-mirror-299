class IRIRefResolveError(Exception):
    
    def __init__(self, iri):
        self.msg = "Can only resolve when base is IRI, not IRelativeRef. Given {}".format(iri)

    def __str__(self):
        return repr(self.msg)