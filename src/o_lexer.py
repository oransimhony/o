from sly import Lexer


class OLexer(Lexer):
    tokens = {ID, INT, FLOAT, ASSIGN, STRING, LET,
              PRINT, IF, ELSE, EQEQ, SEP, NOTEQ, LESS,
              GREATER, LESSEQ, GREATEREQ, NIL, WHILE,
              FOR, FN, RETURN, LAMBDA, ARROW, TRUE, FALSE,
              AND, OR, SHR, SHL, INC, DEC, PLUSASGN,
              MINUSASGN, STARASGN, SLASHASGN, MODULOASGN,
              ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN}
    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~'}

    LET = r'let'
    PRINT = r'print'
    IF = r'if'
    ELSE = r'else'
    NIL = r'nil'
    WHILE = r'while'
    FOR = r'for'
    FN = r'fn'
    RETURN = r'return'
    LAMBDA = r'lambda'
    TRUE = r'true'
    FALSE = r'false'
    AND = r'and'
    OR = r'or'
    INC = r'\+\+'
    DEC = r'--'
    PLUSASGN = r'\+='
    MINUSASGN = r'-='
    STARASGN = r'\*='
    SLASHASGN = r'/='
    MODULOASGN = r'%='
    ANDASGN = r'&='
    ORASGN = r'\|='
    XORASGN = r'^='
    SHLASGN = r'<<='
    SHRASGN = r'>>='
    ARROW = r'=>'
    LESSEQ = r'<='
    GREATEREQ = r'>='
    LESS = r'<'
    GREATER = r'>'
    NOTEQ = r'!='
    EQEQ = r'=='
    ASSIGN = r'='
    SHR = r'>>'
    SHL = r'<<'
    SEP = r';'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'\".*?(?<!\\)(\\\\)*\"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("Illegal character '%s' on line %d" % (t.value[0], self.lineno))
        self.index += 1
