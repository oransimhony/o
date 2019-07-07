from sly import Lexer


class OLexer(Lexer):
    tokens = {ID, INT, FLOAT, ASSIGN, STRING, LET,
              PRINT, IF, ELSE, EQEQ, SEP, NOTEQ, LESS,
              GREATER, LESSEQ, GREATEREQ, NIL, WHILE,
              FOR, FN, RETURN, LAMBDA, ARROW, TRUE, FALSE,
              AND, OR, SHR, SHL, INC, DEC, PLUSASGN,
              MINUSASGN, STARASGN, SLASHASGN, MODULOASGN,
              ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN,
              IMPORT}
    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~',
                '.'}

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
    ID['let'] = LET
    ID['print'] = PRINT
    ID['if'] = IF
    ID['else'] = ELSE
    ID['nil'] = NIL
    ID['while'] = WHILE
    ID['for'] = FOR
    ID['fn'] = FN
    ID['return'] = RETURN
    ID['lambda'] = LAMBDA
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['and'] = AND
    ID['or'] = OR
    ID['import'] = IMPORT

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
