from sly import Parser
from o_lexer import OLexer


class OParser(Parser):
    # debugfile = 'parser.out'
    tokens = OLexer.tokens

    precedence = (
        ('left', EQEQ, NOTEQ, LESS, GREATER, LESSEQ, GREATEREQ),
        ('left', '+', '-'),
        ('left', '%'),
        ('left', '*', '/'),
        ('right', 'UMINUS')
    )

    # @_('NUMBER statement')
    # def line(self, p):
    #   return (p.NUMBER, p.statement)

    @_('program statement')
    def program(self, p):
        return p.program + (p.statement, )

    @_('statement')
    def program(self, p):
        return (p.statement, )

    @_('empty')
    def program(self, p):
        return ()

    @_('FN ID "(" params ")" block')
    def statement(self, p):
        return ('fn', p.ID, ('params', p.params), ('block', p.block))

    @_('LAMBDA "(" params ")" ARROW expr')
    def expr(self, p):
        return ('lambda', ('params', p.params), ('block', ('return', p.expr)))

    @_('var_define SEP')
    def statement(self, p):
        return p.var_define

    @_('LET ID ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.ID, p.expr)

    @_('LET ID SEP')
    def statement(self, p):
        return ('var_define', p.ID, None)

    @_('var_assign SEP')
    def statement(self, p):
        return p.var_assign

    @_('RETURN expr SEP')
    def statement(self, p):
        return ('return', p.expr)

    @_('ID ASSIGN expr')
    def var_assign(self, p):
        return ('var_assign', p.ID, p.expr)

    @_('PRINT expr SEP')
    def statement(self, p):
        return ('print', p.expr)

    @_('IF expr block ELSE block')
    def statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

    @_('IF expr block')
    def statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block), None)

    @_('WHILE expr block')
    def statement(self, p):
        return ('while', ('condition', p.expr), ('block', p.block))

    @_('FOR var_assign SEP expr SEP var_assign block')
    def statement(self, p):
        return (p.var_assign0, ('while', ('condition', p.expr), ('block', p.block + (p.var_assign1, ))))

    @_('ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', p.args))

    @_('expr logical expr')
    def expr(self, p):
        return (p.logical, p.expr0, p.expr1)

    @_('EQEQ')
    def logical(self, p):
        return '=='

    @_('NOTEQ')
    def logical(self, p):
        return '!='

    @_('LESS')
    def logical(self, p):
        return '<'

    @_('GREATER')
    def logical(self, p):
        return '>'

    @_('LESSEQ')
    def logical(self, p):
        return '<='

    @_('GREATEREQ')
    def logical(self, p):
        return '>='

    @_('expr SEP')
    def statement(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

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

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('STRING')
    def expr(self, p):
        return p.STRING

    @_('ID')
    def expr(self, p):
        return ('var', p.ID)

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
