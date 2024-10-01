import unittest
from textx import metamodel_for_language
from textx import metamodel_from_file
import textxirirefs.iri

class TestClassification(unittest.TestCase):

    def setUp(self):
        self.parser = metamodel_for_language('textxirirefs')

    def test_empty_string(self):
        model = self.parser.model_from_str('')
        self.assertIsInstance(model.content, textxirirefs.iri.IRelativeRef) # Should be Relative at the end
        self.assertIsInstance(model.content.path, textxirirefs.iri.IPathEmpty)

    def test_token(self):
        model = self.parser.model_from_str('foo')
        self.assertIsInstance(model.content, textxirirefs.iri.IRelativeRef) # Should be Relative at the end
        self.assertIsInstance(model.content.path, textxirirefs.iri.IPathNoScheme) # Should be PathNoScheme at the end

class TestStandardResolve(unittest.TestCase):
    '''
    Implements all tests of (RFC 3986) https://www.ietf.org/rfc/rfc3986.txt
    5.4.  Reference Resolution Examples
    '''

    def setUp(self):
        self.parser = metamodel_for_language('textxirirefs')
        self.base = self.parser.model_from_str("http://a/b/c/d;p?q")

        
    def test_resolve_normal(self):
        '''
        Tests from 5.4.1.  Normal Examples
        '''
        data = [
            ("g:h",             "g:h"),
            ("g",               "http://a/b/c/g"),
            ("./g",             "http://a/b/c/g"),
            ("g/",              "http://a/b/c/g/"),
            ("/g",              "http://a/g"),
            ("//g",             "http://g"),
            ("?y",              "http://a/b/c/d;p?y"),
            ("g?y",             "http://a/b/c/g?y"),
            ("#s",              "http://a/b/c/d;p?q#s"),
            ("g#s",             "http://a/b/c/g#s"),
            ("g?y#s",           "http://a/b/c/g?y#s"),
            (";x",              "http://a/b/c/;x"),
            ("g;x",             "http://a/b/c/g;x"),
            ("g;x?y#s",         "http://a/b/c/g;x?y#s"),
            ("",                "http://a/b/c/d;p?q"),
            (".",               "http://a/b/c/"),
            ("./",              "http://a/b/c/"),
            ("..",              "http://a/b/"),
            ("../",             "http://a/b/"),
            ("../g",            "http://a/b/g"),
            ("../..",           "http://a/"),
            ("../../",          "http://a/"),
            ("../../g",         "http://a/g")
        ]
        for iriref, expected in data:
            with self.subTest():
                model = self.parser.model_from_str(iriref)
                result=self.base.resolve(model)
                self.assertEqual(result.recompose(), expected)

    def test_resolve_abnormal(self):
        '''
        Tests from 5.4.2.  Abnormal Examples
        '''
        data = [
            ("../../../g",      "http://a/g"),
            ("../../../../g",   "http://a/g"),
            ("/./g",            "http://a/g"),
            ("/../g",           "http://a/g"),
            ("g.",              "http://a/b/c/g."),
            (".g",              "http://a/b/c/.g"),
            ("g..",             "http://a/b/c/g.."),
            ("..g",             "http://a/b/c/..g"),
            ("./../g",          "http://a/b/g"),
            ("./g/.",           "http://a/b/c/g/"),
            ("g/./h",           "http://a/b/c/g/h"),
            ("g/../h",          "http://a/b/c/h"),
            ("g;x=1/./y",       "http://a/b/c/g;x=1/y"),
            ("g;x=1/../y",      "http://a/b/c/y"),
            ("g?y/./x" ,        "http://a/b/c/g?y/./x"),
            ("g?y/../x",        "http://a/b/c/g?y/../x"),
            ("g#s/./x",         "http://a/b/c/g#s/./x"),
            ("g#s/../x",        "http://a/b/c/g#s/../x"),
            ("http:g",          "http:g")    
        ]
        for iriref, expected in data:
            with self.subTest():
                model = self.parser.model_from_str(iriref)
                result = self.base.resolve(model)
                self.assertEqual(result.recompose(), expected)

    def test_resolve_strict(self):
        '''
        Default is strict resolution, but can have non strict resolution for
        backward compatibility with (RFC1630) https://www.ietf.org/rfc/rfc1630.txt
        '''
        data = [
            ("http:g",          "http:g",   True),
            ("http:g" , "http://a/b/c/g",  False)
        ]
        for iriref, expected, strict in data:
            with self.subTest():
                model = self.parser.model_from_str(iriref)
                result = self.base.resolve(model, strict=strict)
                self.assertEqual(result.recompose(), expected)

if __name__ == '__main__':
    unittest.main()