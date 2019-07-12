from sly import Parser
from o_lexer import OLexer


class OParser(Parser):
    # debugfile = 'parser.out'
    tokens = OLexer.tokens

    precedence = (
        ('right', PLUSASGN, MINUSASGN, STARASGN, SLASHASGN,
         MODULOASGN, ANDASGN, ORASGN, XORASGN, SHLASGN, SHRASGN),
        ('left', OR),
        ('left', AND),
        ('left', '|'),
        ('left', '^'),
        ('left', '&'),
        ('left', EQEQ, NOTEQ),
        ('left', LESS, LESSEQ, GREATER, GREATEREQ),
        ('left', SHL, SHR),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS', 'UPLUS', 'LOGICALNOT', INC, DEC),
        ('right', '!'),
    )

    @_('program statement')
    def program(self, p):
        return p.program + (p.statement, )

    @_('statement')
    def program(self, p):
        return (p.statement, )

    @_('empty')
    def program(self, p):
        return ()

    @_('import_statement')
    def statement(self, p):
        return p.import_statement

    @_('function_declaration')
    def statement(self, p):
        return p.function_declaration

    @_('return_statement')
    def statement(self, p):
        return p.return_statement

    @_('print_statement')
    def statement(self, p):
        return p.print_statement

    @_('while_statement')
    def statement(self, p):
        return p.while_statement
    
    @_('for_statement')
    def statement(self, p):
        return p.for_statement
    
    @_('if_statement')
    def statement(self, p):
        return p.if_statement

    @_('IMPORT ID SEP')
    def import_statement(self, p):
        return ('import', p.ID)

    @_('var_define SEP')
    def statement(self, p):
        return p.var_define

    @_('FN ID "(" params ")" block')
    def function_declaration(self, p):
        return ('fn', p.ID, ('params', p.params), ('block', p.block))

    @_('LAMBDA "(" params ")" ARROW expr')
    def expr(self, p):
        return ('lambda', ('params', p.params), ('block', ('return', p.expr)))
        
    @_('LET var ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.var, p.expr)

    @_('LET var SEP')
    def statement(self, p):
        return ('var_define', p.var, None)

    @_('var_assign SEP')
    def statement(self, p):
        return p.var_assign

    @_('RETURN expr SEP')
    def return_statement(self, p):
        return ('return', p.expr)

    @_('var ASSIGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, p.expr)

    @_('var PLUSASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('+', ('var', p.var), p.expr))

    @_('var MINUSASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('-', ('var', p.var), p.expr))

    @_('var STARASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('*', ('var', p.var), p.expr))

    @_('var SLASHASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('/', ('var', p.var), p.expr))

    @_('var MODULOASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('%', ('var', p.var), p.expr))

    @_('var ANDASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('&', ('var', p.var), p.expr))

    @_('var ORASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('|', ('var', p.var), p.expr))

    @_('var XORASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('^', ('var', p.var), p.expr))

    @_('var SHLASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('<<', ('var', p.var), p.expr))

    @_('var SHRASGN expr')
    def var_assign(self, p):
        return ('var_assign', p.var, ('>>', ('var', p.var), p.expr))

    @_('PRINT expr SEP')
    def print_statement(self, p):
        return ('print', p.expr)

    @_('IF expr block ELSE block')
    def if_statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

    @_('IF expr block')
    def if_statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block), None)

    @_('WHILE expr block')
    def while_statement(self, p):
        return ('while', ('condition', p.expr), ('block', p.block))

    @_('FOR var_assign SEP expr SEP var_assign block')
    def for_statement(self, p):
        return (p.var_assign0, ('while', ('condition', p.expr), ('block', p.block + (p.var_assign1, ))))

    @_('expr "?" expr ":" expr')
    def expr(self, p):
        return ('?:', p.expr0, p.expr1, p.expr2)

    @_('ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', p.args))

    @_('expr EQEQ expr')
    def expr(self, p):
        return ('==', p.expr0, p.expr1)

    @_('expr NOTEQ expr')
    def expr(self, p):
        return ('!=', p.expr0, p.expr1)

    @_('expr LESSEQ expr')
    def expr(self, p):
        return ('<=', p.expr0, p.expr1)

    @_('expr GREATEREQ expr')
    def expr(self, p):
        return ('>=', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ('and', p.expr0, p.expr1)

    @_('expr OR expr')
    def expr(self, p):
        return ('or', p.expr0, p.expr1)

    @_('expr LESS expr')
    def expr(self, p):
        return ('<', p.expr0, p.expr1)

    @_('expr GREATER expr')
    def expr(self, p):
        return ('>', p.expr0, p.expr1)

    @_('expr SHL expr')
    def expr(self, p):
        return ('<<', p.expr0, p.expr1)

    @_('expr SHR expr')
    def expr(self, p):
        return ('>>', p.expr0, p.expr1)

    @_('expr "&" expr')
    def expr(self, p):
        return ('&', p.expr0, p.expr1)

    @_('expr "^" expr')
    def expr(self, p):
        return ('^', p.expr0, p.expr1)

    @_('expr "|" expr')
    def expr(self, p):
        return ('|', p.expr0, p.expr1)

    @_('"~" expr %prec LOGICALNOT')
    def expr(self, p):
        return ('~', p.expr)

    @_('expr SEP')
    def statement(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ('neg', p.expr)

    @_('"+" expr %prec UPLUS')
    def expr(self, p):
        return p.expr

    @_('"!" expr')
    def expr(self, p):
        return ('!', p.expr)

    @_('INC var')
    def var_assign(self, p):
        return ('var_assign', p.var, ('+', ('var', p.var), 1))

    @_('DEC var')
    def var_assign(self, p):
        return ('var_assign', p.var, ('-', ('var', p.var), 1))

    @_('expr "+" expr')
    def expr(self, p):
        return ('+', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('-', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('*', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('/', p.expr0, p.expr1)

    @_('expr "%" expr')
    def expr(self, p):
        return ('%', p.expr0, p.expr1)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('INT')
    def expr(self, p):
        return p.INT

    @_('FLOAT')
    def expr(self, p):
        return p.FLOAT

    @_('STRING')
    def expr(self, p):
        return p.STRING

    @_('TRUE')
    def expr(self, p):
        return True

    @_('FALSE')
    def expr(self, p):
        return False

    @_('list_val')
    def expr(self, p):
        return p.list_val

    @_('"[" exprs "]"')
    def list_val(self, p):
        return p.exprs

    @_('empty')
    def exprs(self, p):
        return []

    @_('expr')
    def exprs(self, p):
        return [p.expr]

    @_('exprs "," expr')
    def exprs(self, p):
        return p.exprs + [p.expr]

    @_('var "[" expr "]"')
    def expr(self, p):
        return ('indexing', ('var', p.var), p.expr)

    @_('var')
    def expr(self, p):
        return ('var', p.var)

    @_('ID')
    def var(self, p):
        return p.ID

    @_('var "[" expr "]"')
    def var(self, p):
        return ('indexing', ('var', p.var), p.expr)

    @_('NIL')
    def expr(self, p):
        return None

    @_('')
    def empty(self, p):
        pass

    @_('"{" program "}"')
    def block(self, p):
        return p.program

    @_('statement')
    def block(self, p):
        return (p.statement, )

    @_('params "," param')
    def params(self, p):
        return p.params + [p.param]

    @_('param')
    def params(self, p):
        return [p.param]

    @_('empty')
    def params(self, p):
        return []

    @_('ID')
    def param(self, p):
        return p.ID

    @_('args "," arg')
    def args(self, p):
        return p.args + [p.arg]

    @_('arg')
    def args(self, p):
        return [p.arg]

    @_('empty')
    def args(self, p):
        return []

    @_('expr')
    def arg(self, p):
        return p.expr
