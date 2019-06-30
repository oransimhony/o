class Process:
  def __init__(self, tree, filename="?", env={}):
    self.tree = tree
    self.file_path = filename
    self.env = env

  def run(self, tree=None):
    if tree is None:
      print(self.tree)
      for line in self.tree:
        # print(line)
        self.evaluate(line)
    else:
      for line in tree:
        self.evaluate(line)


  def stringify(self, expr):
    if expr is None:
        return "nil"
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
        elif action == 'var_define':
            if parsed[1] in self.env:
                print('Cannot redefine variable \'%s\'' % parsed[1])
                return None
            result = self.evaluate(parsed[2])
            self.env[parsed[1]] = result
            return None
        elif action == 'var_assign':
            if parsed[1] not in self.env:
                print('Cannot assign to undefined variable \'%s\'' % parsed[1])
                return None
            result = self.evaluate(parsed[2])
            self.env[parsed[1]] = result
            return None 
        elif action == 'if':
            # print(parsed)
            # print(parsed[3])
            cond = self.evaluate(parsed[1])
            if cond:
                return self.evaluate(parsed[2])
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
            if parsed[1] in self.env:
                return self.env[parsed[1]]
            else:
                print("{} is undefined".format(parsed[1]))
                return None
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
        elif action == '==':
            result = self.evaluate(parsed[1])
            result2 = self.evaluate(parsed[2])
            return result == result2
        elif action == '!=':
            result = self.evaluate(parsed[1])
            result2 = self.evaluate(parsed[2])
            return not (result == result2)
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
        else:
            if len(parsed) > 0 and type(parsed[0]) == tuple:
              return self.run(parsed)

            print(parsed)
            return None