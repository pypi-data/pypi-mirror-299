import textxirirefs.iri

class URIRefContainer(textxirirefs.iri.IRIRefContainer):
    pass

class URIReference(textxirirefs.iri.IRIReference):
    pass

class URI(textxirirefs.iri.IRI, URIReference):
    
     def __init__(self, scheme, authority, path, query, fragment):
        super().__init__(scheme, authority, path, query, fragment)
        if not self.isdefined('fragment'):
            self.__class__ = AbsoluteURI

class AbsoluteURI(textxirirefs.iri.AbsoluteIRI, URI):
    pass

class RelativeRef(textxirirefs.iri.IRelativeRef, URIReference):
    pass

class Authority(textxirirefs.iri.IAuthority):
    pass

class Path(textxirirefs.iri.IPath):
    pass

class PathAbsolute(textxirirefs.iri.IPathAbsolute, Path):
    pass

class PathAbEmpty(textxirirefs.iri.IPathAbEmpty, Path):
    pass

class PathRootless(textxirirefs.iri.IPathRootless, Path):
    pass

class PathNoScheme(textxirirefs.iri.IPathNoScheme, Path):
    pass

class PathEmpty(textxirirefs.iri.IPathEmpty, Path):
    pass