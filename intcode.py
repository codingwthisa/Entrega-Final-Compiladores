#checker.py
from modelo import *
from plex import Lexer
from pparser import Parser
from dataclasses import dataclass, field
from typing import Any
import sys

class IntermediateCodeGenerator:
    def __init__(self):
        self.intermediate_code = []
        self.register_counter = 0 

    def generate_code(self, node):
        self.intermediate_code = []  # Reiniciamos el código intermedio
        self.visit(node)
        return self.intermediate_code

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node.__class__.__name__} method")

    def visit_Program(self, node):
        self.intermediate_code.append(":::::::::: __pl0_init([]) -> I ::::::::::")
        self.intermediate_code.append("========================================")

        for func_def in node.funclist:
            self.visit(func_def)

    def visit_FunDefinition(self, node):
        self.intermediate_code.append(
            f":::::::::: {node.name}({[param.name for param in node.parameters] if node.parameters else []}) -> I ::::::::::"
        )
        for statement in node.statements:
            result = self.visit(statement)
            if result:
                self.intermediate_code.extend(result)  

        self.intermediate_code.append("========================================")

    def visit_VarDef(self, node):
        pass

    def visit_AssignmentStatement(self, node):
        self.intermediate_code.append(('MOVI', self.visit(node.expression), f'R{node.location}'))

    def visit_Binop(self, node):
        op_code = {
            '+': 'ADDI',
            '-': 'SUBI',
            '*': 'MULI',
            '/': 'DIVI',
        }[node.op]
        left_operand = self.visit(node.left)
        right_operand = self.visit(node.right)
        result_register = f'R{self.register_counter}'
        self.register_counter += 1
        self.intermediate_code.append((op_code, left_operand, right_operand, result_register))
        return result_register
    
    def visit_Identifier(self, node):
        return f'{node.name}'
    
    def visit_FunctionCall(self, node):
        args_code = ', '.join([self.visit(arg) for arg in node.arguments])
        return f'CALL {node.identifier}({args_code})'


    def visit_IntegerNumber(self, node):
        return str(node.value)
    
    def visit_FloatNumber(self, node):
        return str(node.value)

    def visit_ReturnStatement(self, node):
        expression_code = self.visit(node.expression)
        return [('RETURN', expression_code)]

    def visit_IfStatement(self, node):
        condition_code = self.visit(node.condition)
        then_body_code = self.visit(node.then_body)
        return [('IF', condition_code, 'GOTO', then_body_code)]

    def visit_IfElseStatement(self, node):
        condition_code = self.visit(node.condition)
        then_body_code = self.visit(node.then_body)
        else_body_code = self.visit(node.else_body)
        return [('IF', condition_code, 'GOTO', then_body_code),
                ('GOTO', else_body_code)]

    def visit_Break(self, node):
        return [('GOTO', 'exit_loop_label')] 

    def visit_While(self, node):
        start_label = f'while_start_label'
        exit_label = f'while_exit_label'
        
        condition_code = self.visit(node.relation)
        stmt_code = self.visit(node.stmt)

        return [(start_label + ':'),
                ('IF', condition_code, 'GOTO', stmt_code),
                ('GOTO', exit_label),
                (stmt_code + ':'),
                ('GOTO', start_label),
                (exit_label + ':')]
    
    def visit_RelationalOperation(self, node):
        left_operand = self.visit(node.left_operand)
        right_operand = self.visit(node.right_operand)
        op_code = {
            '<': 'LT',
            '>': 'GT',
            '<=': 'LTE',
            '>=': 'GTE',
            '==': 'EQ',
            '!=': 'NEQ',
        }[node.operator]

        result_register = f'R{node.result}'
        self.intermediate_code.append((op_code, left_operand, right_operand, result_register))

        return result_register
    
    def visit_str(self, node):
        return node


    def visit_ReadStatement(self, node):
        return [('READ', f'R{node.location}')]

    def visit_PrintStatement(self, node):
        expr_code = self.visit(node.string_expr)
        return [('PRINT', expr_code)]

    def visit_WriteStatement(self, node):
        expr_code = self.visit(node.expression)
        return [('WRITE', expr_code)]

    def visit_ArrayType(self, node):
        dim_code = self.visit(node.dim)
        return [('ARRAY', dim_code)]
    
    def visit_ArrayLocation(self, node):
        index_code = self.visit(node.index)
        return f'ARRAY_LOAD {node.name}, {index_code}'


def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)
    
    filename = argv[1]
    with open(filename, 'r') as file:
        text = file.read()

    lexer_sly = Lexer()
    parser_sly = Parser()
    
    result = parser_sly.parse(lexer_sly.tokenize(text))

    code_generator = IntermediateCodeGenerator()

    intermediate_code = code_generator.generate_code(result)

    print("Intermediate Code:")
    for instruction in intermediate_code:
        print(instruction)

if __name__ == '__main__':
    main(sys.argv)