from random import randint
from math import sin, cos, tan, sinh, cosh, tanh ,ceil, floor, sqrt, degrees, radians
from os.path import exists, dirname, join
from os import getenv
from o_lexer import OLexer
from o_parser import OParser

def standard_library():
    env = Env()
    env.update({
        'input': lambda prompt: input(prompt),
        'random': lambda max: randint(0, max),
        'typeof': lambda val: type(val),
        'is_float': lambda val: isinstance(val, float),
        'is_int': lambda val: isinstance(val, int),
        'is_string': lambda val: isinstance(val, str),
        'is_list': lambda val: isinstance(val, list),
        'is_bool': lambda val: isinstance(val, bool),
        'to_float': lambda val: float(val),
        'to_int': lambda val: int(val),
        'to_string': lambda val: str(val),
        'to_list': lambda val: list(val),
        'to_bool': lambda val: bool(val),
        'append': lambda lst, val: lst.append(val),
        'pop': lambda lst: lst.pop(),
        'pop_at': lambda lst, idx: lst.pop(idx),
        'extend': lambda lst1, lst2: lst1.extend(lst2),
        'len': lambda obj : len(obj),
        'sin': lambda val : sin(val),
        'cos': lambda val : cos(val),
        'tan': lambda val : tan(val),
        'sinh': lambda val : sinh(val),
        'cosh': lambda val : cosh(val),
        'tanh': lambda val : tanh(val),
        'ceil': lambda val : ceil(val),
        'floor': lambda val : floor(val),
        'abs': lambda val : abs(val),
        'sqrt': lambda val : sqrt(val),
        'pow': lambda base, exponent : pow(base, exponent),
        'deg': lambda val : degrees(val),
        'rad': lambda val : radians(val)
    })
    return env


class Process:
    def __init__(self, tree, filename="?", env={}):
        self.tree = tree
        self.file_path = filename
        if not isinstance(env, Env):
            _env = env
            env = Env(outer=standard_library())
            env.update(_env)
        self.env = Env(outer=env)
        self.should_return = False
        self.depth = 0

    def run(self, tree=None, env={}):
        current_env = self.env
        result = None
        if env != {}:
            self.env = env
        if tree is None:
            for line in self.tree:
                result = self.evaluate(line)
                if self.should_return:
                    self.depth -= 1
                    if self.depth <= 0:
                        self.depth = 0
                        self.should_return = False
                    return result
        else:
            for line in tree:
                result = self.evaluate(line)
                if self.should_return:
                    self.depth -= 1
                    if self.depth <= 0:
                        self.depth = 0
                        self.should_return = False
                    return result
        self.env = current_env
        return result

    def stringify(self, expr):
        if expr is None:
            return "nil"
        elif expr is True:
            return "true"
        elif expr is False:
            return "false"
        return str(expr)

    def evaluate(self, parsed):
        # print("PARSED:", parsed)
        if type(parsed) != tuple:
            # print("DIFFERENT TYPE: ", parsed)
            return parsed
        else:
            action = parsed[0]

            if action == 'print':
                result = self.evaluate(parsed[1])
                print(self.stringify(result))
                return None
            elif action == 'import':
                base_dir = getenv('OPATH')
                if base_dir is None:
                    base_dir = dirname(__file__)
                rel_path = 'include/' + parsed[1] + '.olang'
                path = join(base_dir, rel_path)
                if exists(path):
                    fp = open(path)
                    self.import_contents(fp.read())
            elif action == 'fn':
                params = parsed[2]
                body = parsed[3]
                self.env.update({parsed[1]: Function(
                    self, params[1], body, self.env)})
                return None
            elif action == 'call':
                func = self.env.find(parsed[1])
                if not isinstance(func, Function):
                    if type(func) == type(lambda x: x):
                        args = [self.evaluate(arg) for arg in parsed[2][1]]
                        self.depth += 1
                        res = func(*args)
                        self.depth -= 1
                        return res
                    else:
                        print('\'%s\' not a function' % parsed[1])
                        return

                args = [self.evaluate(arg) for arg in parsed[2][1]]
                self.depth += 1
                res = func(*args)
                self.depth -= 1
                return res

            elif action == 'lambda':
                body = parsed[2]
                params = parsed[1]
                return Function(self, params[1], body, self.env)

            elif action == 'return':
                result = self.evaluate(parsed[1])
                self.should_return = True
                return result

            elif action == 'var_define':
                name = parsed[1]
                if name in self.env:
                    print('Cannot redefine variable \'%s\'' % name)
                    return None
                result = self.evaluate(parsed[2])
                self.env.update({name: result})
                return None
            elif action == 'var_assign':
                if type(parsed[1]) is not tuple:
                    if parsed[1] not in self.env:
                        print('Cannot assign to undefined variable \'%s\'' %
                              parsed[1])
                        return None
                    result = self.evaluate(parsed[2])
                    self.env.update({parsed[1]: result})
                    return None
                else:
                    var = self.evaluate(parsed[1][1])
                    index = self.evaluate(parsed[1][2])
                    value = self.evaluate(parsed[2])
                    var[index] = value
            elif action == 'if':
                cond = self.evaluate(parsed[1])
                if cond:
                    return self.evaluate(parsed[2])
                if parsed[3] is not None:
                    return self.evaluate(parsed[3])
            elif action == 'while':
                cond = self.evaluate(parsed[1])
                while cond:
                    self.evaluate(parsed[2])
                    cond = self.evaluate(parsed[1])
            elif action == 'condition':
                return self.evaluate(parsed[1])
            elif action == 'block':
                return self.run(parsed[1])
            elif action == 'var':
                return self.env.find(parsed[1])
            elif action == 'indexing':
                var = self.evaluate(parsed[1])
                index = self.evaluate(parsed[2])
                if index > len(var):
                    print('Index out of bounds error')
                    return None
                elif type(index) != int:
                    print('List indices must be integers')
                    return None
                return var[index]
            elif action == '+':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result + result2
            elif action == '-':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result - result2
            elif action == '*':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result * result2
            elif action == '/':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return int(result / result2)
            elif action == '%':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result % result2
            elif action == '==':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result == result2
            elif action == '!=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result != result2
            elif action == '<':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result < result2
            elif action == '>':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result > result2
            elif action == '<=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result <= result2
            elif action == '>=':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result >= result2
            elif action == '<<':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result << result2
            elif action == '>>':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result >> result2
            elif action == '&':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result & result2
            elif action == '^':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result ^ result2
            elif action == '|':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result | result2
            elif action == '~':
                result = self.evaluate(parsed[1])
                return ~result
            elif action == 'and':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result and result2
            elif action == 'or':
                result = self.evaluate(parsed[1])
                result2 = self.evaluate(parsed[2])
                return result or result2
            elif action == '!':
                result = self.evaluate(parsed[1])
                if result == True:
                    return False
                return True
            elif action == '?:':
                cond = self.evaluate(parsed[1])
                if cond:
                    return self.evaluate(parsed[2])
                return self.evaluate(parsed[3])
            elif action == '.':
                var = self.env.find(parsed[1])
                res = self.evaluate(var[parsed[2]])
                return res

            else:
                if len(parsed) > 0 and type(parsed[0]) == tuple:
                    return self.run(parsed)

                print(parsed)
                return None

    def import_contents(self, file_contents):
        lexer = OLexer()
        parser = OParser()

        tokens = lexer.tokenize(file_contents)

        # for token in tokens:
        #     print(token)
        
        tree = parser.parse(tokens)
        # print(tree)

        program = Process(tree)
        program.run()
        self.env.update(program.env)


class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, name):
        if name in self:
            return self[name]
        elif self.outer is not None:
            return self.outer.find(name)

        print("{} is undefined".format(name))
        return None


class Function(object):
    def __init__(self, process, params, body, env):
        self.process, self.params, self.body, self.env = process, params, body, env

    def __call__(self, *args):
        return self.process.run(self.body, Env(self.params, args, self.env))
