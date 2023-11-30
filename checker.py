from modelo import *
from plex import Lexer
from pparser import Parser
from dataclasses import dataclass, field
from rich import print
import sys

# ---------------------------------------------------------------------
#  Tabla de Simbolos
# ---------------------------------------------------------------------

class Symtab:
    class SymbolDefinedError(Exception):
        pass

    def __init__(self, parent=None):
        self.entries = {}
        self.parent = parent
        self.in_while_context = False 
        if self.parent:
            self.parent.children.append(self)
        self.children = []

    def add(self, name, value):
        if name in self.entries:
            raise Symtab.SymbolDefinedError()
        self.entries[name] = value

    def get(self, name):
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None

@dataclass
class Literal(Expression):
	...

@dataclass
class Integer(Literal):
    value : int
    type : DataType = field(default_factory=SimpleType('int'))

@dataclass
class Float(Literal):
    value: float
    type: DataType = field(default_factory= SimpleType('float'))


class Checker(Visitor):
    def visit(self, node: Any, symtab: Symtab):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, symtab)

    def generic_visit(self, node: Any, symtab: Symtab):
        if node is None:
            return

        for field_name, field_value in node.__dict__.items():
            if field_value is None:
                continue

            if isinstance(field_value, list):
                for item in field_value:
                    self.visit(item, symtab)
            elif isinstance(field_value, Symtab):
                self.visit(field_value, symtab)
            elif isinstance(field_value, Expression):
                self.visit(field_value, symtab)

    
    def visit_Program(self, node: Program, symtab: Symtab):
        for func in node.funclist:
            self.visit(func, symtab)

        main_function = symtab.get('main')
        if main_function is None or not isinstance(main_function, FunDefinition):
            raise Symtab.SymbolDefinedError("Error: No se encontró la función 'main' en el programa.")
    
    def visit_FunDefinition(self, node: FunDefinition, symtab: Symtab):
        print("Fue a FunDefinition")
        existing_function = symtab.get(node.name)

        if existing_function is not None:
            raise Symtab.SymbolDefinedError(f"La función {node.name} ya está definida.")
        else:
            function_symtab = Symtab(parent=symtab)

            symtab.add(node.name, (node, function_symtab))

        if node.parameters is not None:
            for param in node.parameters:
                self.visit(param, function_symtab)

        if node.local_variables is not None:
            for local_var in node.local_variables:
                self.visit(local_var, function_symtab)

        for statement in node.statements:
            self.visit(statement, function_symtab)

    
    def visit_Parameter(self, node: Parameter, symtab: Symtab):
        print("Fue a Parameter")
        try:
            symtab.add(node.name, node)
        except Symtab.SymbolDefinedError:
            raise Symtab.SymbolDefinedError(f"El parámetro {node.name} ya está definido.")
    
    def visit_VarDef(self, node: VarDef, symtab: Symtab):
        print("fue a VarDef")
        try:
            symtab.add(node.name, node)
        except Symtab.SymbolDefinedError:
            raise Symtab.SymbolDefinedError(f"La variable {node.name} ya está definida.")

        self.visit(node.type_name, symtab)
    
    def visit_LogicalOperation(self, node: LogicalOperation, symtab: Symtab):
        print("fue a logical operation")
        self.visit(node.left, symtab)
        self.visit(node.right, symtab)
    
    def visit_BinOp(self, node: Binop, symtab: Symtab):
        print("visitó binop")
        self.visit(node.left, symtab)
        self.visit(node.right, symtab)
    
    def visit_UnaryOp(self, node: UnaryOp, symtab: Symtab):
        print("visitó unop")
        self.visit(node.expression, symtab)
    
    def visit_TypeName(self, node: TypeName, symtab: Symtab):
        print("typename")
        pass
    
    def visit_FunctionCall(self, node: FunctionCall, symtab: Symtab):
        print("visitó functioncall")
        function_name = node.identifier
        function = symtab.get(function_name)

        if function is None or not isinstance(function, FunDefinition):
            raise Symtab.SymbolDefinedError(f"La función {function_name} no está definida.")

        if len(node.arguments) != len(function.parameters):
            raise Symtab.SymbolDefinedError(f"La función {function_name} espera {len(function.parameters)} argumentos, pero se proporcionaron {len(node.arguments)}.")

        for argument in node.arguments:
            self.visit(argument, symtab)
    
    def visit_SimpleLocation(self, node: SimpleLocation, symtab: Symtab):
        print("simple location")
        variable_name = node.name
        variable = symtab.get(variable_name)

        if variable is None or not isinstance(variable, VarDef):
            raise Symtab.SymbolDefinedError(f"La variable {variable_name} no está definida.")
    
    def visit_ArrayLocation(self, node: ArrayLocation, symtab: Symtab):
        print("array location")
        array_name = node.name
        array = symtab.get(array_name)

        if array is None or not isinstance(array, ArrayType):
            raise Symtab.SymbolDefinedError(f"El array {array_name} no está definido.")

        self.visit(node.index, symtab)
    
    def visit_AssignmentStatement(self, node: AssignmentStatement, symtab: Symtab):
        print("visitó assign")
        left_type = self.visit(node.location, symtab)
        right_type = self.visit(node.expression, symtab)

        if left_type == right_type:
            return left_type
        else:
            raise symtab.SemanticError(f"La asignación es incompatible. Se esperaba {left_type}, pero se encontró {right_type}")
            
    def visit_IntegerNumber(self, node: IntegerNumber, symtab: Symtab):
        print("integer")
        value = node.value
        if not isinstance(value, int):
            raise Symtab.SymbolDefinedError("El valor del entero no es un tipo entero válido.")

    def visit_FloatNumber(self, node: FloatNumber, symtab: Symtab):
        print("float")
        value = node.value
        if not isinstance(value, float):
            raise Symtab.SymbolDefinedError("El valor del flotante no es un tipo flotante válido.")
    
    def visit_ReturnStatement(self, node: ReturnStatement, symtab: Symtab):
        print("return")
        if node.expression is not None:
            self.visit(node.expression, symtab)

    def visit_IfStatement(self, node: IfStatement, symtab: Symtab):
        print("if")
        self.visit(node.condition, symtab)

        self.visit(node.then_body, symtab)

        if node.else_body:
            self.visit(node.else_body, symtab)

    def visit_IfElseStatement(self, node: IfElseStatement, symtab: Symtab):
        print("if-else")
        self.visit(node.condition, symtab)

        self.visit(node.then_body, symtab)

        self.visit(node.else_body, symtab)

    
    def visit_Break(self, node: Break, symtab: Symtab):
        print("break")
        if not symtab.in_while_context:
            raise Symtab.SymbolDefinedError("La declaración 'break' debe estar dentro de un bucle (while).")
    
    def visit_While(self, node, symtab: Symtab = None):
        print("visitó while")
        symtab = symtab or self.symtab
        symtab.in_while_context = True

        self.visit(node.relation, symtab)
        self.visit(node.stmt, symtab)  

        symtab.in_while_context = False
    
    def visit_ReadStatement(self, node: ReadStatement, symtab: Symtab):
        print("read")
        variable_name = node.location.name
        variable = symtab.get(variable_name)

        if variable is None or not isinstance(variable, VarDef):
            raise Symtab.SymbolDefinedError(f"La variable {variable_name} no está declarada antes de la lectura.")

        if not isinstance(node.location, (SimpleLocation, ArrayLocation)):
            raise Symtab.SymbolDefinedError(f"La ubicación {node.location} no es válida en una declaración de lectura.")

        self.visit(node.location, symtab)

    
    def visit_PrintStatement(self, node: PrintStatement, symtab: Symtab):
        print("print")
        pass

    def visit_WriteStatement(self, node: WriteStatement, symtab: Symtab):
        print("write")

        if not isinstance(node.expression, (SimpleLocation, ArrayLocation)):
            raise Symtab.SymbolDefinedError("La expresión en la declaración 'write' no es una ubicación válida.")

        self.visit(node.expression, symtab)

        return self.visit(node.expression, symtab)


def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)
    
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        text = file.read()

    lex = Lexer()
    parser = Parser()
    Nodo = parser.parse(lex.tokenize(text))
    semantico=Checker()
    Tabla= Symtab()
    semantico.visit(Nodo,Tabla)


if __name__ == '__main__':
    from sys import argv
    main(argv)