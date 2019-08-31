from sly import Parser
from o_lexer import OLexer


class OParser(Parser):
    """
    Parser for the O Language
    """
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

    @_('statements')
    def program(self, p):
        return p.statements

    @_('empty')
    def program(self, p):
        return ()

    @_('statement')
    def statements(self, p):
        return (p.statement, )

    @_('statements statement')
    def statements(self, p):
        return p.statements + (p.statement, )

    @_('import_statement')
    def statement(self, p):
        return p.import_statement

    @_('function_definition')
    def statement(self, p):
        return p.function_definition

    @_('return_statement')
    def statement(self, p):
        return p.return_statement

    @_('while_statement')
    def statement(self, p):
        return p.while_statement
    
    @_('for_statement')
    def statement(self, p):
        return p.for_statement
    
    @_('if_statement')
    def statement(self, p):
        return p.if_statement

    @_('struct_definition')
    def statement(self, p):
        return p.struct_definition

    @_('class_definition')
    def statement(self, p):
        return p.class_definition

    @_('CLASS ID "{" function_definitions "}"')
    def class_definition(self, p):
        return ('class', p.ID, ('functions', p.function_definitions))

    @_('empty')
    def function_definitions(self, p):
        return []

    @_('function_definition')
    def function_definitions(self, p):
        return [p.function_definition]

    @_('function_definitions function_definition')
    def function_definitions(self, p):
        return p.function_definitions + [p.function_definition]

    @_('STRUCT ID "{" struct_fields "}" SEP')
    def struct_definition(self, p):
        return ('struct', p.ID, p.struct_fields)

    @_('struct_field')
    def struct_fields(self, p):
        return p.struct_field

    @_('struct_fields struct_field')
    def struct_fields(self, p):
        return p.struct_fields + p.struct_field

    @_('LET ID ":" var_type SEP')
    def struct_field(self, p):
        return [(p.ID, p.var_type)]

    @_('INT_TYPE')
    def var_type(self, p):
        return 'int'

    @_('FLOAT_TYPE')
    def var_type(self, p):
        return 'float'

    @_('STRING_TYPE')
    def var_type(self, p):
        return 'string'

    @_('BOOL_TYPE')
    def var_type(self, p):
        return 'bool'

    @_('LIST_TYPE')
    def var_type(self, p):
        return 'list'

    @_('DICT_TYPE')
    def var_type(self, p):
        return 'dict'

    @_('IMPORT STRING SEP')
    def import_statement(self, p):
        return ('import', p.STRING)

    @_('var_define SEP')
    def statement(self, p):
        return p.var_define

    @_('FN ID "(" params ")" block')
    def function_definition(self, p):
        return ('fn', p.ID, ('params', p.params), ('block', p.block))

    @_('ID LEFTARROW "{" struct_init_exprs "}" ')
    def expr(self, p):
        return ('init_struct', p.ID, p.struct_init_exprs)

    @_('expr')
    def struct_init_exprs(self, p):
        return [p.expr]

    @_('struct_init_exprs "," expr')
    def struct_init_exprs(self, p):
        return p.struct_init_exprs + [p.expr]

    @_('LAMBDA "(" params ")" ARROW expr')
    def expr(self, p):
        return ('lambda', ('params', p.params), ('block', ('return', p.expr)))
        
    @_('LET var ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.var, p.expr)
        
    @_('LET getter ASSIGN expr')
    def var_define(self, p):
        return ('var_define', p.getter, p.expr)

    @_('LET var ":" var_type SEP')
    def statement(self, p):
        return ('var_define_no_expr', p.var, p.var_type)

    @_('TYPEOF expr')
    def expr(self, p):
        return ('typeof', p.expr)

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

    @_('ID DOUBLECOLON ID "(" args ")"')
    def expr(self, p):
        return ('class_func_call', p.ID0, p.ID1, ('args', p.args))

    @_('expr PIPE ID "(" args ")"')
    def expr(self, p):
        return ('call', p.ID, ('args', [p.expr] + p.args))

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

    @_('ID ":" var_type')
    def param(self, p):
        return (p.ID, p.var_type)

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

    @_('"{" member_list "}"')
    def expr(self, p):
        return p.member_list

    @_('empty')
    def member_list(self, p):
        return {}

    @_('member')
    def member_list(self, p):
        return p.member

    @_('member_list "," member')
    def member_list(self, p):
        return { **p.member_list, **p.member }

    @_('STRING ":" expr')
    def member(self, p):
        return { p.STRING : p.expr }

    @_('getter "." ID')
    def getter(self, p):
        return ('.', p.getter, p.ID)

    @_('ID')
    def getter(self, p):
        return p.ID

    @_('getter')
    def expr(self, p):
        return p.getter
