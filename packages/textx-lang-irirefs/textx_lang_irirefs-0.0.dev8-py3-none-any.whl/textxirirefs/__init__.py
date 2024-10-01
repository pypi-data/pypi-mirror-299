import os
from textx import metamodel_from_file
from textx import LanguageDesc
import textxirirefs.iri
import textxirirefs.uri


__VERSION__ = "0.0dev8"


__iri_classes__ = [c for c in textxirirefs.iri.__dict__.values() 
                    if (isinstance(c, type) and c.__module__ == textxirirefs.iri.__name__)]

__uri_classes__ = [c for c in textxirirefs.iri.__dict__.values() 
                    if (isinstance(c, type) and c.__module__ == textxirirefs.uri.__name__)]

__PATH__ = os.path.dirname(__file__)


def textxirirefs_language():
    mm = metamodel_from_file(os.path.join(__PATH__, 'iri.tx'), classes = __iri_classes__)
    return mm

def textxurirefs_language():
    mm = metamodel_from_file(os.path.join(__PATH__, 'uri.tx'), classes = __uri_classes__)
    return mm

textxirirefs_lang = LanguageDesc('textxirirefs',
                           pattern=None,
                           description='Implementation of IRIReferences standard using textX',
                           metamodel=textxirirefs_language)

textxurirefs_lang =  LanguageDesc('textxurirefs',
                           pattern=None,
                           description='Implementation of URIReferences standard using textX',
                           metamodel=textxurirefs_language)



