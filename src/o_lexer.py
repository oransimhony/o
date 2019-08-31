from sly import Lexer


class OLexer(Lexer):
    """
    O language Lexer
    """
    tokens = {ID, INT, FLOAT, ASSIGN, STRING, LET,
              IF, ELSE, EQEQ, SEP, NOTEQ, LESS,
              GREATER, LESSEQ, GREATEREQ, NIL, WHILE,
              FOR, FN, RETURN, LAMBDA, ARROW, TRUE, FALSE,
              AND, OR, SHR, SHL, INC, DEC, PLUSASGN,
              MINUSASGN, STARASGN, SLASHASGN, MODULOASGN,
              ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN,
              IMPORT, STRUCT, INT_TYPE, FLOAT_TYPE, BOOL_TYPE,
              LIST_TYPE, DICT_TYPE, STRING_TYPE, TYPEOF,
              LEFTARROW, PIPE, CLASS, DOUBLECOLON}
    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~',
                '.'}

    INC = r'\+\+'
    DEC = r'--'
    PIPE = r'\|>'
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
    LEFTARROW = r'<-'
    SHR = r'>>'
    SHL = r'<<'
    LESS = r'<'
    GREATER = r'>'
    NOTEQ = r'!='
    EQEQ = r'=='
    ASSIGN = r'='
    SEP = r';'
    DOUBLECOLON = r'::'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['let'] = LET
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
    ID['struct'] = STRUCT
    ID['int'] = INT_TYPE
    ID['float'] = FLOAT_TYPE
    ID['string'] = STRING_TYPE
    ID['bool'] = BOOL_TYPE
    ID['list'] = LIST_TYPE
    ID['dict'] = DICT_TYPE
    ID['typeof'] = TYPEOF
    ID['class'] = CLASS

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        """
        Parsing float numbers
        """
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
        """
        Parsing integers
        """
        t.value = int(t.value)
        return t

    @_(r'\".*?(?<!\\)(\\\\)*\"')
    def STRING(self, t):
        """
        Parsing strings (including escape characters)
        """
        t.value = t.value[1:-1]
        t.value = t.value.replace(r"\n", "\n")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\\", "\\")
        t.value = t.value.replace(r"\"", "\"")
        t.value = t.value.replace(r"\a", "\a")
        t.value = t.value.replace(r"\b", "\b")
        t.value = t.value.replace(r"\r", "\r")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\v", "\v")
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("Illegal character '%s' on line %d" % (t.value[0], self.lineno))
        self.index += 1
