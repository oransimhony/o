from basic_lexer import BasicLexer
from basic_parser import BasicParser
from basic_interpreter import Process
import sys


def repl():
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    while True:
        try:
            text = input('>> ')
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        if text:
            result, env = evaluate(parser.parse(lexer.tokenize(text)), env)
            if result != None:
                print(result)


def exec_file():
    lexer = BasicLexer()
    parser = BasicParser()
    env = {}
    with open(sys.argv[1]) as opened_file:
        # for line in opened_file:
        tokens = lexer.tokenize(opened_file.read())
        # for token in tokens:
        #     print(token)
        
        tree = parser.parse(tokens)
        program = Process(tree)
        program.run()
        # for statement in program:
        # result, env = evaluate(program, env)
        # if result != None:
        #     print(result)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        exec_file()
