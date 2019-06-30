from o_lexer import OLexer
from o_parser import OParser
from o_interpreter import Process
import sys


def repl():
    lexer = OLexer()
    parser = OParser()
    env = {}
    while True:
        try:
            text = input('>> ')
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)
            
            tree = parser.parse(tokens)
            program = Process(tree, env)
            program.run()
            env = program.env


def exec_file():
    lexer = OLexer()
    parser = OParser()
    env = {}
    with open(sys.argv[1]) as opened_file:
        tokens = lexer.tokenize(opened_file.read())
        
        tree = parser.parse(tokens)
        program = Process(tree)
        program.run()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        exec_file()
