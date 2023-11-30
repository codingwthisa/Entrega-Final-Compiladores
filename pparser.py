import sly
from plex import Lexer
from modelo import *
from rich import print
from ASTree import *
import sys

class Parser(sly.Parser):
    debugfile = 'pl0.txt'

    tokens = Lexer.tokens

    precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT'),
    ('nonassoc', 'THEN'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'BEGIN'),
    ('nonassoc', 'FUN'),
)
    
    def __init__(self):
        self.symtable = {}
        self.error_count = 0
        self.index = 0

    @_('funclist')
    def program(self, p):
        return Program(p.funclist)

    @_('stmt')
    def program(self, p):
        return Program([p.stmt])
    
    @_('funclist function')
    def funclist(self, p):
        return p.funclist + [p.function]
    
    @_('function')
    def funclist(self, p):
        return [p.function]
    
    @_('FUN IDENT LPARENT [ parmlist ] RPARENT [ varlist ] BEGIN stmtlist END')
    def function(self, p):
        return FunDefinition(p.IDENT, p.parmlist, p.varlist, p.stmtlist)
    
    @_('LPARENT parmlistitems RPARENT')
    def parmlist(self, p):
        return ParameterList(parameters=p.parmlistitems)
    
    @_('parmlist COMMA parm')
    def parmlist(self, p):
        return p.parmlist + [p.parm]
    
    @_('parm')
    def parmlistitems(self, p):
        return [p.parm]
    
    @_('IDENT COLON typename')
    def parm(self, p):
        return Parameter(p.IDENT, p.typename)
    
    @_('parm')
    def parmlist(self, p):
        return [p.parm]    
    
    @_('INT')
    def typename(self, p):
        return TypeName(base_type='INT')

    @_('FLOAT')
    def typename(self, p):
        return TypeName(base_type='FLOAT')

    @_("INT LBRACKET INUMBER1 RBRACKET")
    def typename(self, p):
        return TypeName(p[0], array_size=p.INUMBER1)

    @_("FLOAT LBRACKET FNUMBER1 RBRACKET")
    def typename(self, p):
        return TypeName(p[0], array_size=p.FNUMBER1)
    
    @_("INT LBRACKET expr RBRACKET")
    def typename(self, p):
        return TypeName(p[0], array_size=p.expr)

    @_("FLOAT LBRACKET expr RBRACKET")
    def typename(self, p):
        return TypeName(p[0], array_size=p.expr)

    @_('decllist optsemi')
    def varlist(self, p):
        return VariableList(declarations=p.decllist)
    
    @_('decllist1 SEMICOLON')
    def varlist(self, p):
        return [p.decllist1]
    
    @_('decllist1 SEMICOLON varlist')
    def varlist(self, p):
        return [p.decllist1] + p.varlist
    
    @_('vardecl')
    def decllist1(self, p):
        return p.vardecl
    
    @_('function')
    def decllist1(self, p):
        return p.function

    # Regla para optsemi
    @_('SEMICOLON')
    def optsemi(self, p):
        pass 

    @_('')  # Regla vacía para indicar que el punto y coma es opcional
    def optsemi(self, p):
        pass

    @_('IDENT COLON typename')
    def vardecl(self, p):
        return Parameter(p.IDENT, p.typename)
    
    @_('vardecl')
    def decllist(self, p):
        return [p.vardecl]

    @_('decllist SEMICOLON vardecl')
    def decllist(self, p):
        return p.decllist + [p.vardecl]

    @_('stmt')
    def stmtlist(self, p):
        return [p.stmt]
    
    @_('stmtlist SEMICOLON stmt')
    def stmtlist(self, p):
        return p.stmtlist + [p.stmt]
    

    @_('PRINT LPARENT STRING RPARENT')
    def stmt(self, p):
        string_value = p.STRING
        print(string_value)

    @_('READ LPARENT location RPARENT')
    def stmt(self, p):
        return ReadStatement(p.location)
    
    @_('WRITE LPARENT expr RPARENT')
    def stmt(self, p):
        return WriteStatement(p.expr)

    @_('WHILE relop DO stmt')
    def stmt(self, p):
        return While(p.relop, p.stmt)

    @_('BREAK')
    def stmt(self, p):
        return Break()


    @_("IF relop THEN stmt %prec THEN")
    def stmt(self, p):
        return IfStatement(p.relop, p.stmt)

    @_("IF relop THEN stmt ELSE stmt %prec ELSE")
    def stmt(self, p):
        return IfElseStatement(p.relop, p.stmt0, p.stmt1)
        
    @_('BEGIN stmtlist END')
    def stmt(self, p):
        return BeginEndBlock(p.stmtlist)

    @_('location ASSIGN expr')
    def stmt(self, p):
        return AssignmentStatement(p.location, p.expr)

    @_('RETURN expr')
    def stmt(self, p):
        return ReturnStatement(p.expr)

    @_('SKIP')
    def stmt(self, p):
        return SkipStatement()
    
    @_('IDENT LPARENT exprlist RPARENT')
    def stmt(self, p):
        return FunctionCall(p.IDENT, p.exprlist)

    @_("IDENT")
    def location(self, p):
        return Location(identifier=p[0])
    
    @_("IDENT LBRACKET expr RBRACKET")
    def location(self, p):
        return ArrayLocation(p[0], index=p.expr)
    
    @_("IDENT LBRACKET expr RBRACKET")
    def expr(self, p):
        return ArrayLocation(p[0], index=p.expr)
    
    @_('[ exprlistitems ]')
    def exprlist(self, p):
        return ExprList(p.exprlistitems)
        
    @_("exprlist [ COMMA expr ]")
    def exprlistitems(self, p):
        return [p.expr] if p[1] is None else [p.expr] + p[1]
    
    @_('expr')
    def exprlist(self, p):
        return [p.expr]
    
    @_("expr PLUS expr",
        "expr MINUS expr",
        "expr TIMES expr",
        "expr DIVIDE expr")
    def expr(self, p):
        return Binop(p[1], p.expr0, p.expr1)

    @_("MINUS expr")
    def expr(self, p):
        return UnaryOperation('-', p.expr)

    @_('PLUS expr')
    def expr(self, p):
        return UnaryOperation('+', p.expr)

    @_('LPARENT expr RPARENT')
    def expr(self, p):
        return p.expr
    
    @_('INUMBER')
    def INUMBER1(self, p):
        return IntegerNumber(int(p[0]))

    @_('FNUMBER')
    def FNUMBER1(self, p):
        return FloatNumber(float(p[0]))

    @_('IDENT')
    def expr(self, p):
        return Identifier(p[0])

    @_('IDENT LPARENT RPARENT')
    def expr(self, p):
        return FunctionCall(identifier=p[0], arguments=[])

    @_('IDENT LPARENT exprlist RPARENT')
    def expr(self, p):
        return FunctionCall(identifier=p[0], arguments=p.exprlist)

    @_('INT LBRACKET expr RBRACKET')
    def expr(self, p):
        return IntConversion(p.expr)
    
    @_('FLOAT LBRACKET expr RBRACKET')
    def expr(self, p):
        return FloatConversion(p.expr)
    
    @_('INT LPARENT expr RPARENT')
    def expr(self, p):
        return IntConversion(p.expr)
    
    @_('FLOAT LPARENT expr RPARENT')
    def expr(self, p):
        return FloatConversion(p.expr)
    
    @_('INUMBER')
    def expr(self, p):
        return IntegerNumber(int(p[0]))
    
    @_('FNUMBER')
    def expr(self, p):
        return FloatNumber(float(p[0]))

    @_('expr LT expr',
    'expr LE expr',
    'expr GT expr',
    'expr GE expr',
    'expr EQ expr',
    'expr NE expr',
    'expr DF expr'
    )
    def relop(self, p):
        return RelationalOperation(p[1], p.expr0, p.expr1)

    @_('relop AND relop',
        'relop OR relop'
        )
    def relop(self, p):
        return LogicalOperation(p[1], p.relop0, p.relop1)

    @_('NOT relop')
    def relop(self, p):
        return NotOperation(p.relop)

    @_('LPARENT relop RPARENT',)
    def relop(self, p):
        return p.relop
    
    @_('exprlist COMMA expr')
    def exprlist(self, p):
        return p.exprlist + [p.expr]
    
    def error(self, p):
        if p:
            print(f"Parser error: Unexpected token '{p.value}' of type '{p.type}' at line {p.lineno}")
            print(f"Context: {self.get_error_context(p)}")
            self.index += 1  
        else:
            print("Parser error: Unexpected end of input")

    def get_error_context(self, p, context_size=20):
        start_index = max(p.index - context_size, 0)
        tokens_list = list(self.tokens)
        end_index = min(p.index + context_size, len(tokens_list))

        context = ' '.join(str(tokens_list[i].value) for i in range(start_index, end_index))
        return f"... {context} ..."

def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as file:
        text = file.read()

    lexer_sly = Lexer()
    parser_sly = Parser()
    result = parser_sly.parse(lexer_sly.tokenize(text))
    ast_visitor = AST(result)

    # Realiza la visita al AST
    ast_visitor.visit(result)

    # Genera el archivo DOT
    dot_content = ast_visitor.to_dot()

    # Opcional: Imprime el contenido DOT en la consola
    print(dot_content)

    # Opcional: Guarda el contenido DOT en un archivo
    dot_filename = "ast.dot"
    with open(dot_filename, "w") as dot_file:
        dot_file.write(dot_content)

if __name__ == '__main__':
    from sys import argv
    main(argv)

