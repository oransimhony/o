from sly import Parser
from basic_lexer import BasicLexer


class BasicParser(Parser):
    debugfile = 'parser.out'
    tokens = BasicLexer.tokens

    precedence = (
        ('left', EQEQ),
        ('left', '+', '-'),
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

    @_('LET ID ASSIGN expr SEP')
    def statement(self, p):
        return ('var_define', p.ID, p.expr)

    @_('ID ASSIGN expr SEP')
    def statement(self, p):
        return ('var_assign', p.ID, p.expr)

    @_('PRINT expr SEP')
    def statement(self, p):
        return ('print', p.expr)

    @_('IF condition block ELSE block')
    def statement(self, p):
        return ('if', ('condition', p.condition), ('thenBody', p.block0), ('elseBody', p.block1))

    @_('IF condition block')
    def statement(self, p):
        return ('if', ('condition', p.condition), ('thenBody', p.block0), ('elseBody', None))

    @_('expr EQEQ expr')
    def condition(self, p):
        return ('eqeq', p.expr0, p.expr1)

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

    @_('')
    def empty(self, p):
        pass

    @_('"{" program "}"')
    def block(self, p):
        return p.program

    @_('statement')
    def block(self, p):
        return p.statement
