from random import randint
from math import sin, cos, tan, asin, acos, atan, sinh, cosh, tanh ,ceil, floor, sqrt, degrees, radians, log
from os.path import exists, dirname, join
from os import getenv
from o_lexer import OLexer
from o_parser import OParser

def standard_library():
    """
    Function that generates a dictionary that contains all the basic functions
    """
    env = Env()
    env.update({
        'input': lambda prompt: input(prompt),
        'random': lambda max: randint(0, max),
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
        'asin': lambda val : asin(val),
        'acos': lambda val : acos(val),
        'atan': lambda val : atan(val),
        'sinh': lambda val : sinh(val),
        'cosh': lambda val : cosh(val),
        'tanh': lambda val : tanh(val),
        'ceil': lambda val : ceil(val),
        'floor': lambda val : floor(val),
        'abs': lambda val : abs(val),
        'sqrt': lambda val : sqrt(val),
        'pow': lambda base, exponent : pow(base, exponent),
        'deg': lambda val : degrees(val),
        'rad': lambda val : radians(val),
        'log': lambda val : log(val),
        'exit': lambda val : exit(val),
        'trim': lambda val : val.strip(),
        'split': lambda val, delimeter=" " : val.split(delimeter),
        'print': lambda val : print(val),
    })
    return env


class Process:
    """
    The main process the executes O Abstract Syntax Tree
    """
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
        self.types  =  { 'int': int, 'float': float, 'string': str, 'bool': bool, 'list': list, 'dict': dict }
        self.rtypes = { int: 'int', float: 'float', str: 'string', bool: 'bool', list: 'list', dict: 'dict' }

    def run(self, tree=None, env={}):
        current_env = self.env
        result = None
        if env != {}:
            self.env = env
        if tree is None:
            for line in self.tree:
                try:
                    result = self.evaluate(line)
                except ValueError as e:
                    print(e)
                    break
                except UnboundLocalError as e:
                    print(e)
                    break
                except NameError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    break
                except TypeError as e:
                    print(e)
                    break
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    return result
        else:
            for line in tree:
                try:
                    result = self.evaluate(line)
                except ValueError as e:
                    print(e)
                    break
                except UnboundLocalError as e:
                    print(e)
                    break
                except NameError as e:
                    print(e)
                    break
                except IndexError as e:
                    print(e)
                    break
                except TypeError as e:
                    print(e)
                    break
                if self.depth == 0:
                    self.should_return = False
                if self.should_return:
                    return result
        self.env = current_env
        return result

    def stringify(self, expr):
        """
        Preparing values for printing
        """
        if type(expr) == dict:
            return str(expr)
        elif expr is None:
            return "nil"
        elif expr is True:
            return "true"
        elif expr is False:
            return "false"
        elif expr in self.rtypes:
            return self.rtypes[expr]
        return str(expr)

    def evaluate(self, parsed):
        """
        Evaluating a parsed tree/tuple/expression
        """
        if type(parsed) != tuple:
            return parsed
        else:
            action = parsed[0]
            if action == 'class_func_call':
                instance = self.env.find(parsed[1]).value
                method = instance.find_method(parsed[2])
                args = [self.evaluate(arg) for arg in parsed[3][1]]
                self.depth += 1
                res = method(*args)
                self.depth -= 1
                return res
            elif action == 'class':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                    return None

                class_process = Process((), env=Env(self.env))

                for function in parsed[2][1]:
                    class_process.evaluate(function)

                # print(class_process.env)

                self.env.update({ name: OClass(name, class_process.env) })
            elif action == 'typeof':
                try:
                    if len(parsed[1]) == 2:
                        var = self.env.find(parsed[1][1])
                        return var.type
                    elif len(parsed[1]) == 3:
                        var = self.env.find(parsed[1][1][1])
                        index = self.evaluate(parsed[1][2])
                        return self.rtypes[type(var.value[index])]
                except TypeError as e:
                    return self.rtypes[type(parsed[1])]
            elif action == 'struct':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                    return None

                fields = parsed[2]

                self.env.update({ name: { "__fields__": fields } })
            elif action == 'init_struct':
                name = parsed[1]
                struct_definition = self.env.find(name)
                if struct_definition is None:
                    raise UnboundLocalError('Struct %s is undefined' % name)
                    return None
                fields = struct_definition['__fields__']
                values = [self.evaluate(value) for value in parsed[2]]

                struct = {}
                for i in range(len(fields)):
                    if i < len(values):
                        if type(values[i]) != self.types[fields[i][1]]:
                            raise ValueError("Type for field '{}' should be '{}' but instead got '{}'".format(fields[i][0], fields[i][1], self.rtypes[type(values[i])]))
                        struct.update({ fields[i][0]: values[i] })
                    else:
                        struct.update({ fields[i][0]: None })

                return struct
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
                if isinstance(func, Value):
                    func = func.get()

                if isinstance(func, OClass):
                    return func()
                elif not isinstance(func, Function):
                    if type(func) == type(lambda x: x):
                        args = [self.evaluate(arg) for arg in parsed[2][1]]
                        self.depth += 1
                        res = func(*args)
                        self.depth -= 1
                        return res
                    else:
                        raise ValueError('\'%s\' not a function' % parsed[1])

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
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                result = self.evaluate(parsed[2])
                self.env.update({name: Value(result, type(result))})
                return None
            elif action == 'var_define_no_expr':
                name = parsed[1]
                if name in self.env:
                    raise NameError('Cannot redefine variable \'%s\'' % name)
                self.env.update({name: Value(None, self.types[parsed[2]])})
                return None
            elif action == 'var_assign':
                if type(parsed[1]) is not tuple:
                    if parsed[1] not in self.env:
                        raise UnboundLocalError('Cannot assign to undefined variable \'%s\'' %
                              parsed[1])
                    result = self.evaluate(parsed[2])
                    var = self.env.find(parsed[1])
                    if type(result) != var.type:
                        raise ValueError("Type of variable '{}' should be '{}' but instead got '{}'".format(parsed[1], self.rtypes[var.type], self.rtypes[type(result)]))

                    # self.env.update({parsed[1]: result})
                    var.value = result
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
                var = self.env.find(parsed[1])
                if not isinstance(var, Value):
                    return var
                return var.value
            elif action == 'indexing':
                var = self.evaluate(parsed[1])
                index = self.evaluate(parsed[2])
                if index > len(var):
                    raise IndexError('Index out of bounds error')
                    return None
                elif type(index) != int:
                    raise IndexError('List indices must be integers')
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
                return result / result2
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
                if type(parsed[1]) == tuple:
                    var = self.evaluate(parsed[1])
                else:
                    var = self.env.find(parsed[1])
                if isinstance(var, Value):
                    res = self.evaluate(var.value[parsed[2]])
                else:
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
        tree = parser.parse(tokens)
        program = Process(tree)
        program.run()
        self.env.update(program.env)

class Env(dict):
    """
    Environment Class
    """
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, name):
        if name in self:
            return self[name]
        elif self.outer is not None:
            return self.outer.find(name)

        raise UnboundLocalError("{} is undefined".format(name))


class Function(object):
    """
    Function object for O Functions and annoymous functions (lambdas)
    """
    def __init__(self, process, params, body, env):
        self.process, self.params, self.body, self.env = process, params, body, env
        self.type = 'function'

    def __call__(self, *args):
        params = []
        for i in range(len(self.params)):
            if type(args[i]) != self.process.types[self.params[i][1]]:
                raise TypeError("Type of parameter {} should be {} but got {}.".format(self.params[i][0], self.params[i][1], self.process.rtypes[type(args[i])]))
            params.append(self.params[i][0])
        return self.process.run(self.body, Env(params, args, self.env))

class Value(object):
    """
    Class container for values inside the O Language
    """
    def __init__(self, value, val_type):
        self.value = value
        self.type = val_type

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return "{}: {}".format(self.value, self.type)

    def get(self):
        return self.value

class OClass(object):
    """
    Object for classes in O
    """
    def __init__(self, name, env):
        self.name = name
        self.env = env
        self.type = 'class'

    def __str__(self):
        return "<{} class>".format(self.name)

    def __call__(self):
        return OInstance(self)

class OInstance(object):
    """
    Object for instances of a class in O
    """
    def __init__(self, oclass):
        self.oclass = oclass
        self.type = 'instance'
        init_method = self.oclass.env.get('init')
        if init_method is not None:
            init_method()

    def __str__(self):
        return "<{} instance>".format(self.oclass.name)

    def find_method(self, name):
        return self.oclass.env.find(name)
