from sly import Parser
from basic_lexer import BasicLexer


class BasicParser(Parser):
    tokens = BasicLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS')
    )

    # @_('NUMBER statement')
    # def line(self, p):
    #   return (p.NUMBER, p.statement)

    @_('statements')
    def program(self, p):
        return p.statements

    @_('statements newlines statement')
    def statements(self, p):
        if p.statement is None:
            return p.statements
        return p.statements + [ p.statement ]

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_('newlines newline')
    def newlines(self, p):
        pass

    @_('newline')
    def newlines(self, p):
        pass

    @_('NEWLINE')
    def newline(self, p):
        pass

    @_('')
    def statement(self, p):
        pass

    @_('PRINT expr')
    def statement(self, p):
        return ('print', p.expr)

    @_('LET ID ASSIGN expr')
    def statement(self, p):
        return ('var_define', p.ID, p.expr)

    @_('ID ASSIGN expr')
    def statement(self, p):
        return ('var_assign', p.ID, p.expr)

    @_('IF condition THEN statement')
    def statement(self, p):
        return ('if', p.condition, p.statement, None)

    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return ('if', p.condition, p.statement0, p.statement1)

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr "+" term')
    def expr(self, p):
        return ('+', p.expr, p.term)

    @_('expr "-" term')
    def expr(self, p):
        return ('-', p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term

    @_('term "*" factor')
    def term(self, p):
        return ('*', p.term, p.factor)

    @_('term "/" factor')
    def term(self, p):
        return ('/', p.term, p.factor)

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('"(" expr ")"')
    def factor(self, p):
        return p.expr

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('STRING')
    def expr(self, p):
        return p.STRING

    @_('ID')
    def factor(self, p):
        return ('var', p.ID)

    @_('expr EQEQ expr')
    def condition(self, p):
        return ('eqeq', p.expr0, p.expr1)
