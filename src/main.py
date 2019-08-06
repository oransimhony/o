from o_lexer import OLexer
from o_parser import OParser
from o_interpreter import Process
import sys


def repl():
    lexer = OLexer()
    parser = OParser()
    env = {}
    program = Process((), env=env)
    while True:
        try:
            text = input('>> ')
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        if text:
            tokens = lexer.tokenize(text)

            try:
                tree = parser.parse(tokens)
                program.tree = tree
                program.run()
            except TypeError as e:
                if str(e).startswith("'NoneType' object is not iterable"):
                    print("Syntax Error")
                else:
                    print(e)


def exec_file():
    lexer = OLexer()
    parser = OParser()
    with open(sys.argv[1]) as opened_file:
        tokens = lexer.tokenize(opened_file.read())

        # for token in tokens:
        #     print(token)

        tree = parser.parse(tokens)
        # print(tree)

        program = Process(tree)
        program.run()
        # print(program.env)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        exec_file()
