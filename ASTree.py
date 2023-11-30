from typing import List
from rich.tree import Tree
from rich.console import Console
from modelo import *
from graphviz import Digraph

class AST(Visitor):
    def __init__(self, program):
        self.program = program
        self.console = Console()
        self.ast_tree = Tree(f"[bold white]Abstract Syntax Tree[/bold white]")
        self.node_counter = 0

    def visualize_tree(self, node, tree=None, level=0):
        tree = tree or Tree(f"[bold white]{type(node).__name__}[/bold white]")

        if node is not None:
            for field_name, field_value in node.__dict__.items():
                if isinstance(field_value, list):
                    for item in field_value:
                        self.visualize_tree(item, tree.add(f"[blue]{field_name}[/blue]"))
                elif isinstance(field_value, Node):
                    self.visualize_tree(field_value, tree.add(f"[blue]{field_name}[/blue]"))
                else:
                    tree.add(f"[blue]{field_name}[/blue]: {field_value}")

        return tree

    def visit_Program(self, node):
        console = Console()
        tree = Tree(f"[blue]{type(node).__name__}[/blue]")
        
        for func in node.funclist:
            self.visualize_tree(func, tree.add(f"[blue]funclist[/blue]"))

        console.print(tree)
    
    def visit_FunDefinition(self, node):
        tree = Tree(f"[bold blue]FunDefinition: {node.name}[/bold blue]")
        
        if node.parameters:
            parameters_node = tree.add("[blue]Parameters[/blue]")
            for param in node.parameters:
                self.visualize_tree(param, parameters_node)

        if node.local_variables:
            local_variables_node = tree.add("[blue]Local Variables[/blue]")
            for var in node.local_variables:
                self.visualize_tree(var, local_variables_node)

        if node.statements:
            statements_node = tree.add("[blue]Statements[/blue]")
            for statement in node.statements:
                self.visualize_tree(statement, statements_node)

        console = Console()
        console.print(tree)

    def visit_Parameter(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]name[/blue]: {node.name}")
        self.visualize_tree(node.datatype, tree)
        self.console.print(tree)
    
    def visit_VarDef(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]name[/blue]: {node.name}")
        tree.add(f"[blue]value[/blue]: {node.value}")
        tree.add(f"[blue]datatype[/blue]: {node.datatype}")
        self.console.print(tree)
    
    def visit_LogicalOperation(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]operator[/blue]: {node.operator}")
        tree.add(f"[blue]left_operand[/blue]")
        self.visualize_tree(node.left_operand, tree)
        tree.add(f"[blue]right_operand[/blue]")
        self.visualize_tree(node.right_operand, tree)
        self.console.print(tree)

    def visit_Binop(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]op[/blue]: {node.op}")
        tree.add(f"[blue]left[/blue]")
        self.visualize_tree(node.left, tree)
        tree.add(f"[blue]right[/blue]")
        self.visualize_tree(node.right, tree)
        self.console.print(tree)

    def visit_UnaryOp(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]op[/blue]: {node.op}")
        tree.add(f"[blue]expr[/blue]")
        self.visualize_tree(node.expr, tree)
        self.console.print(tree)
    
    def visit_TypeName(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]base_type[/blue]: {node.base_type}")
        if node.array_size is not None:
            tree.add(f"[blue]array_size[/blue]: {node.array_size}")
        self.console.print(tree)

    def visit_FunctionCall(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]identifier[/blue]: {node.identifier}")
        arguments_node = tree.add("[blue]arguments[/blue]")
        for arg in node.arguments:
            self.visualize_tree(arg, arguments_node)
        self.console.print(tree)
    
    def visit_SimpleLocation(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]name[/blue]: {node.name}")
        self.console.print(tree)

    def visit_ArrayLocation(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]name[/blue]: {node.name}")
        tree.add(f"[blue]index[/blue]")
        self.visualize_tree(node.index, tree)
        self.console.print(tree)

    def visit_AssignmentStatement(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]location[/blue]")
        self.visualize_tree(node.location, tree)
        tree.add(f"[blue]expression[/blue]")
        self.visualize_tree(node.expression, tree)
        self.console.print(tree)
    
    def visit_IntegerNumber(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]value[/blue]: {node.value}")
        self.console.print(tree)

    def visit_FloatNumber(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]value[/blue]: {node.value}")
        self.console.print(tree)

    def visit_ReturnStatement(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]expression[/blue]")
        self.visualize_tree(node.expression, tree)
        self.console.print(tree)

    def visit_IfStatement(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]condition[/blue]")
        self.visualize_tree(node.condition, tree)
        tree.add(f"[blue]then_body[/blue]")
        self.visualize_tree(node.then_body, tree)
        self.console.print(tree)

    def visit_IfElseStatement(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]condition[/blue]")
        self.visualize_tree(node.condition, tree)
        tree.add(f"[blue]then_body[/blue]")
        self.visualize_tree(node.then_body, tree)
        if node.else_body:
            tree.add(f"[blue]else_body[/blue]")
            self.visualize_tree(node.else_body, tree)
        self.console.print(tree)
    
    def visit_Break(self, node):
        tree = self.visualize_tree(node)
        self.console.print(tree)

    def visit_SkipStatement(self, node):
        tree = self.visualize_tree(node)
        self.console.print(tree)

    def visit_While(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]relation[/blue]")
        self.visualize_tree(node.relation, tree)
        tree.add(f"[blue]stmt[/blue]")
        self.visualize_tree(node.stmt, tree)
        self.console.print(tree)
    
    def visit_ReadStatement(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]location[/blue]")
        self.visualize_tree(node.location, tree)
        self.console.print(tree)

    def visit_PrintStatement(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]string_expr[/blue]: {node.string_expr}")
        self.console.print(tree)

    def visit_WriteStatement(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]expression[/blue]")
        self.visualize_tree(node.expression, tree)
        self.console.print(tree)

    def visit_ArrayType(self, node):
        tree = self.visualize_tree(node)
        tree.add(f"[blue]name[/blue]: {node.name}")
        tree.add(f"[blue]dim[/blue]")
        self.visualize_tree(node.dim, tree)
        self.console.print(tree)

    def to_dot(self, filename="ast.dot"):
        dot = Digraph(comment='Abstract Syntax Tree', format='png')
        self._add_nodes_edges(dot, self.program)
        dot.render(filename, cleanup=True)

        return f"AST DOT file generated: {filename}"

        return dot

    def _add_nodes_edges(self, dot, node):
        if node is None:
            return  

        current_node_id = self.node_counter
        self.node_counter += 1  

        dot.node(str(current_node_id), label=type(node).__name__)

        if hasattr(node, '__dict__'):
            for field_name, field_value in node.__dict__.items():
                if isinstance(field_value, list):
                    for item in field_value:
                        self._add_nodes_edges(dot, item)
                elif isinstance(field_value, Node):
                    self._add_nodes_edges(dot, field_value)

                dot.edge(str(current_node_id), str(self.node_counter), label=field_name)
    