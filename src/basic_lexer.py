from sly import Lexer


class BasicLexer(Lexer):
    tokens = {ID, NUMBER, ASSIGN, STRING, LET, PRINT, IF, THEN, ELSE, EQEQ, NEWLINE}
    ignore = ' \t'

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    LET = r'let'
    PRINT = r'print'
    IF = r'if'
    ELSE = r'else'
    THEN = r'then'
    EQEQ = r'=='
    ASSIGN = r'='

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'


    @_(r'\d+')
    def NUMBER(self, t):
      t.value = int(t.value)
      return t

    @_(r'\".*\"')
    def STRING(self, t):
      t.value = t.value[1:-1]
      return t

    @_(r'\n+')
    def NEWLINE(self, t):
      self.lineno += t.value.count('\n')
      return t
