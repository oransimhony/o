from sly import Lexer


class BasicLexer(Lexer):
    tokens = {ID, NUMBER, ASSIGN, STRING, LET,
              PRINT, IF, ELSE, EQEQ, SEP, NOTEQ, LESS, GREATER, LESSEQ, GREATEREQ}
    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    literals = {'=', '+', '-', '/', '*', '(', ')', ',', '{', '}'}

    LET = r'let'
    PRINT = r'print'
    IF = r'if'
    ELSE = r'else'
    LESS = r'<'
    GREATER = r'>'
    LESSEQ = r'<='
    GREATEREQ = r'>='
    NOTEQ = r'!='
    EQEQ = r'=='
    ASSIGN = r'='
    SEP = r';'

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
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
      print("Illegal character '%s' on line %d" % (t.value[0], self.lineno))
      self.index += 1
