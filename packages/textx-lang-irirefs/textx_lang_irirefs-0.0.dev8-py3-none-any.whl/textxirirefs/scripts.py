import argparse
import textxirirefs
from textx import metamodel_for_language

argparser = argparse.ArgumentParser(
                    prog='irirefresolve'.format(textxirirefs.__VERSION__),
                    description='''This command returns the resolution of a relative IRI against a base IRI, 
                    according to the algorithm standardized in [RFC 3986] URI Generic Syntax. 
                    
                    When the --compatibility flag is set, an non strict resolution algorithm 
                    is applied according to prior specifications of partial URI [RFC1630]''',
                    epilog='From textx-lang-irirefs ({}), (c)2023 Jean-François Baget, Inria.'.format(textxirirefs.__VERSION__))
argparser.add_argument('-c', '--compatibility',
                    action='store_true', help='non strict resolution when in compatibility mode')
argparser.add_argument('base', help = 'the IRI against which is resolved the relative')
argparser.add_argument('relative', help = 'the relativeIRI to resolve against a base')

def resolve():
    arguments = argparser.parse_args()
    parser = metamodel_for_language('textxirirefs')
    relativemodel = parser.model_from_str(arguments.relative)
    basemodel = parser.model_from_str(arguments.base)
    print(basemodel.resolve(relativemodel, strict=not arguments.compatibility).recompose())
    