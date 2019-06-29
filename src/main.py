from basic_lexer import BasicLexer
from basic_parser import BasicParser
import sys


def evaluate(parsed, env):
    # print("PARSED:", parsed)
    if type(parsed) != tuple:
        # print("DIFFERENT TYPE: ", parsed)
        return (parsed, env)
    else:
        action = parsed[0]

        if action == 'print':
            result, env = evaluate(parsed[1], env)
            print(result)
            return (None, env)
        elif action == 'var_define':
            if parsed[1] in env:
                print('Cannot redefine variable \'%s\'' % parsed[1])
                return (None, env)
            result, env = evaluate(parsed[2], env)
            env[parsed[1]] = result
            return (None, env)
        elif action == 'var_assign':
            if parsed[1] not in env:
                print('Cannot assign to undefined variable \'%s\'' % parsed[1])
                return (None, env)
            result, env = evaluate(parsed[2], env)
            env[parsed[1]] = result
            return (None, env)
        elif action == 'if':
            result, env = evaluate(parsed[1], env)
            if result:
              return evaluate(parsed[2], env)
            return evaluate(parsed[3], env)

        elif action == 'var':
            if parsed[1] in env:
                return (env[parsed[1]], env)
            else:
                print("{} is undefined".format(parsed[1]))
                return (None, env)
        elif action == '+':
            result, env = evaluate(parsed[1], env)
            result2, env = evaluate(parsed[2], env)
            return (result + result2, env)
        elif action == '-':
            result, env = evaluate(parsed[1], env)
            result2, env = evaluate(parsed[2], env)
            return (result - result2, env)
        elif action == '*':
            result, env = evaluate(parsed[1], env)
            result2, env = evaluate(parsed[2], env)
            return (result * result2, env)
        elif action == '/':
            result, env = evaluate(parsed[1], env)
            result2, env = evaluate(parsed[2], env)
            return (int(result / result2), env)
        elif action == 'eqeq':
            result, env = evaluate(parsed[1], env)
            result2, env = evaluate(parsed[2], env)
            return (result == result2, env)
        else:
            print(parsed)
            return (None, env)


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
        # for token in lexer.tokenize(opened_file.read()):
        #     print(token)
        program = parser.parse(lexer.tokenize(opened_file.read()))
        for statement in program:
          result, env = evaluate(statement, env)
          if result != None:
              print(result)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()
    else:
        exec_file()
