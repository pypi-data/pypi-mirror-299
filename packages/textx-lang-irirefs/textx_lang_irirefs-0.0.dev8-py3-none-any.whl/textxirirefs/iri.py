import copy
from textxirirefs.exceptions import IRIRefResolveError

class IRIRefContainer():

    def __init__(self, content):
        self.content =  content

    def recompose(self, absolute = False):
        return self.content.recompose(absolute)
    
    def clone(self):
        result = copy.copy(self)
        result.content = result.content.clone(result)
        return result

    def resolve(self, relative, strict=True):
        resolved = self.content.resolve(relative.content, strict)
        result = self.clone()
        result.content = resolved
        resolved.parent = result
        return result
    
    def resolve_seglist(self, seglist):
        resolved = self.content.resolve_seglist(seglist)
        result = self.clone()
        result.content = resolved
        resolved.parent = result
        return result
    
    def normalize(self):
        self.content.normalize()

class IRIReference():

    def __init__(self, parent, scheme, authority, path, query, fragment):
        self.parent, self.scheme, self.authority, self.path = parent, scheme, authority, path
        self.query = query[1:] if self.isdefined('query') and len(query) > 1 else None
        self.fragment = fragment[1:] if self.isdefined('fragment') and len(fragment) > 1 else None

    def recompose(self, absolute = False):
        """
        recompose returns a string representation of an iriref model according 
        to RFC 3986 5.3. Component Recomposition 
        """
        return '{scheme}{authority}{path}{query}{fragment}'.format(
            scheme = '{}:'.format(self.scheme) if self.isdefined('scheme') else '',
            authority = self.authority.recompose() if self.isdefined('authority') else '',
            path = self.path.recompose() if self.isdefined('path') else '',
            query = '?{}'.format(self.query) if self.isdefined('query') else '',
            fragment = '#{}'.format(self.fragment) if self.isdefined('fragment') and not absolute else ''
            )
    
    def isdefined(self, attrname):
        return getattr(self, attrname, None) is not None
    
    def clone(self, parent=None):
        self.parent = parent
        result = copy.copy(self)
        if self.isdefined('authority'):
            result.authority = self.authority.clone(result)
        if self.isdefined('path'):  
            result.path = self.path.clone(result)
        return result
    
    def normalize(self):
        pass
    
    


class IRI(IRIReference):
    
   
    def __init__(self, parent, scheme, authority, path, query, fragment):
        super().__init__(parent, scheme, authority, path, query, fragment)
        if not self.isdefined('fragment'):
            self.__class__ = AbsoluteIRI

    def normalize(self):
        self.syntax_based_normalize()
        self.case_normalize()
        self.percent_normalize()
        self.path_segment_normalize()
        self.scheme_based_normalize()

    def syntax_based_normalize(self):
        pass

    def case_normalize(self):
        pass

    def percent_normalize(self):
        pass

    def path_segment_normalize(self):
        pass

    def scheme_based_normalize(self):
        default_ports = {
            'http': 80,
            'https': 443,
            'ftp': 21,
            'telnet': 23,
            'smtp': 25,
            'dns': 53,
            'tftp': 69
        }   
        if self.isdefined('authority') and self.authority.isdefined('port'):
            if self.authority.port == ':' or int(self.authority.port[1:]) == default_ports[self.scheme]:
                self.authority.port = None

    def protocol_based_normalize(self):
        pass

    def resolve(self, relative, strict=True):
        if relative.isdefined('scheme') and (strict or relative.scheme != self.scheme):
            return relative.clone()
        result = self.clone()
        result.fragment = relative.fragment
        result.__class__ = IRI if result.isdefined('fragment') else AbsoluteIRI
        if relative.isdefined('authority'):
            result.authority = relative.authority.clone(result)
            result.path = relative.path.clone(result).remove_dot_segments() if relative.isdefined('path') else None
            result.query = relative.query
            return result
        if not result.isdefined('path') or isinstance(relative.path, IPathEmpty):
            if relative.isdefined('query'): 
                result.query = relative.query
            return result
        if relative.path.absolute:
            result.path = relative.path.clone(result)
        else:
            result.path.merge(relative.path)
        result.path.remove_dot_segments()
        result.query = relative.query
        return result
    
    def resolve_seglist(self, seglist):
        result = self.clone()
        if seglist != []:
            result.query = None
        result.path.merge_seglist(seglist)
        result.path.remove_dot_segments()
        return result



class AbsoluteIRI(IRI):

    def __init__(self, parent, scheme, authority, path, query):
        super().__init__(parent, scheme, authority, path, query, None)


class IRelativeRef(IRIReference):

    def __init__(self, parent, authority, path, query, fragment):
        super().__init__(parent, None, authority, path, query, fragment)

    def resolve(self, relative, strict=True):
        raise IRIRefResolveError(self.recompose())
    
    def resolve_seglist(self, seglist):
        raise IRIRefResolveError(self.recompose())


class IAuthority():

    def __init__(self, parent, user, host, port):
        self.parent, self.user, self.host, self.port = parent, user, host, port

    def recompose(self):
        return '//{user}{host}{port}'.format(
            user = '{}@'.format(self.user) if self.isdefined('user') else '',
            host = self.host,
            port = ':{}'.format(self.port) if self.isdefined('port') else ''
        )
    
    def isdefined(self, attrname):
        return getattr(self, attrname, None) is not None
    
    def clone(self, parent):
        result = copy.copy(self)
        self.parent = parent
        return result
    
class IPath():

    absolute = False

    def __init__(self, parent, segments):
        self.parent, self.segments = parent, segments

    def recompose(self):
        return'{lead}{segments}'.format(
            lead = '/' if self.absolute else '',
            segments = '/'.join(self.segments)
        )
    
    def clone(self, parent):
        result = copy.copy(self)
        result.segments = result.segments.copy()
        self.parent = parent
        return result
    
    def merge(self, path):
        self.merge_seglist(path.segments)

    def merge_seglist(self, seglist):
        if self.parent.isdefined('authority') and self.segments == []:
            self.segments = seglist
            self.__class__ = IPathAbEmpty
        elif self.segments == []:
            self.segments = seglist
            if seglist != []:
                self.__class__ = IPathRootless 
        else:
            self.segments.pop()
            self.segments.extend(seglist)

    def remove_dot_segments(self):
        output = []
        input = ['/'] if self.absolute else []
        if self.segments != []:
            for segment in self.segments[:-1]:
                input.extend([segment, '/'])
            input.append(self.segments[len(self.segments)-1])
        while(input != []):
            #print("Input: ", input, ", output: ", output)
            if   input[0:2] in [['..', '/'], ['.', '/']]:
                input = input[2:]
            elif input[0:3] == ['/', '.', '/']:
                input = input[2:]
            elif input[0:2] == ['/', '.']:
                input = input[:-1]
            elif input[0:3] == ['/', '..', '/']:
                input = input[2:]
                if output != []:
                    output.pop()
                if output != []:
                    output.pop()
            elif input[0:2] == ['/', '..']:
                input = input[:-1]
                if output != []:
                    output.pop()
                if output != []:
                    output.pop()
            elif input in [['..'], ['.']]:
                input = []
            elif input[0] == '/':
                output.extend(input[0:2])
                input = input[2:]
            else:
                output.append(input[0])
                input = input[1:]
        self.absolute = True if (output != [] and output[0] == '/') else False
        if output != [] and output[-1] == '/':
            output.append('')
        self.segments = [elem for elem in output if elem != '/']
    
class IPathAbsolute(IPath):
    absolute = True


class IPathAbEmpty(IPath):
    absolute = True

class IPathRootless(IPath):
    pass


class IPathNoScheme(IPath):
    pass

class IPathEmpty(IPath):
    pass
