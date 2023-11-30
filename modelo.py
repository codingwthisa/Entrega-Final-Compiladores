from dataclasses import dataclass
from typing import List, Any, Optional, Union

@dataclass
class Node:
    pass

@dataclass
class Statement(Node):
    pass

@dataclass
class StatementList:
    statements: List[str]
    date: str
    author: str

@dataclass
class DataType(Node):
    pass

@dataclass
class SimpleType(Node):
    name: str

@dataclass
class ArgList:
    arguments: List[str]
    option: Optional[str]
    flag: bool

@dataclass
class Expression(Node):
    pass

@dataclass
class Literal(Expression):
    '''
    Un valor literal como 2, 2.5, o "dos"
    '''
    pass

@dataclass
class DataType(Node):
    pass

@dataclass
class Location(Statement):
    pass

# Nodos Reales del AST
@dataclass
class Number(Literal):
    value: float

@dataclass
class Binop(Expression):
    '''
    Un operador binario como 2 + 3 o x * y
    '''
    op: str
    left: Expression
    right: Expression

@dataclass
class UnaryOp(Node):
    op: str
    expr: Expression

@dataclass
class SimpleLocation(Location):
    name: str

@dataclass
class ReadLocation(Expression):
    location: Location

@dataclass
class WriteLocation(Statement):
    location: Location
    value: Expression

@dataclass
class TypeName:
    base_type: str
    array_size: int = None

@dataclass
class Program:
    funclist: List

    def __str__(self):
        return f"Program({self.funclist})"

@dataclass
class Program2(Node):
    declarations: List

@dataclass
class Function:
    name: str  # Suponiendo que una función tiene un nombre

@dataclass
class CombinedFuncList:
    funclist: List[Function]

    def __str__(self):
        return f"CombinedFuncList({self.funclist})"

@dataclass
class Parameter:
    name: str
    datatype: TypeName 

@dataclass
class ParameterList:
    parameters: List[Parameter]

@dataclass
class VariableList:
    declarations: List

@dataclass
class VarDef:
    name: str
    value: str
    datatype: str

@dataclass
class ArrayLocation(Location):
    name: str
    index: Expression

@dataclass
class WriteStatement:
    expression: Any  # Aquí, 'Any' representa el tipo de la expresión que se va a escribir

    def __str__(self):
        return f"WRITE({self.expression})"

@dataclass
class ReadStatement:
    location: Location

@dataclass
class While(Statement):
    relation: Expression
    stmt: Statement

@dataclass
class Break(Statement):
    pass

@dataclass
class Location:
    identifier: str
    index: Optional[Expression] = None

@dataclass
class RelationalOperation:
    left_operand: Expression
    operator: str  
    right_operand: Expression

@dataclass
class IfStatement:
    condition: RelationalOperation
    then_body: Statement
    else_body: Optional[Statement] = None

@dataclass
class IfElseStatement:
    condition: RelationalOperation
    then_body: Statement
    else_body: Optional[Statement] = None

@dataclass
class BeginEndBlock:
    stmtlist: List[Statement]

@dataclass
class AssignmentStatement:
    location: Location
    expression: Expression

@dataclass
class ReturnStatement:
    expression: Expression

@dataclass
class SkipStatement:
    pass

@dataclass
class FunctionCall:
    identifier: str
    arguments: List[Expression]



@dataclass
class ExprList:
    expressions: List[Expression]

@dataclass
class IntegerNumber:
    value: int

@dataclass
class FloatNumber:
    value: float

@dataclass
class Identifier:
    name: str

@dataclass
class IntConversion:
    expression: Expression

@dataclass
class FloatConversion:
    expression: Expression

@dataclass
class TypeCast(Expression):
    conversion: Union[IntConversion, FloatConversion]

@dataclass
class TypeCast(Expression):
    name: str
    expr: Expression

@dataclass
class LogicalOperation:
    operator: str
    left_operand: RelationalOperation
    right_operand: RelationalOperation

@dataclass
class NotOperation:
    operand: Union[RelationalOperation, LogicalOperation]

@dataclass
class PrintStatement:
    string_expr: str

    def __str__(self):
        return f'PRINT("{self.string_expr}")'

@dataclass
class ArrayType(TypeName):
    name: str = "valor"
    dim: Expression = "valor"

@dataclass
class UnaryOperation:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def execute(self, symtable):
        if self.operator == '-':
            return -self.operand.execute(symtable)
        elif self.operator == '+':
            return self.operand.execute(symtable)
        elif self.operator == 'not':
            return not self.operand.execute(symtable)
        else:
            raise ValueError(f"Operador no válido: {self.operator}")

@dataclass
class Visitor:
    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        visitor_method = getattr(self, method_name, self.generic_visit)
        return visitor_method(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit_{type(node).__name__} method defined")

@dataclass
class FunDefinition(Node):
    name: str
    parameters: List[Parameter]
    local_variables: List[VarDef]
    statements: List[Statement]
