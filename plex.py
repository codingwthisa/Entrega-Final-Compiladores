import sly
import sys
from rich import print
from rich.table import Table
from rich.console import Console

class Lexer(sly.Lexer):
    tokens = {
        'FUN', 'BEGIN', 'END', 'IF', 'THEN', 'WHILE',
        'DO', 'WRITE', 'READ', 'IDENT', 'DF',
        'LT', 'LE', 'GT', 'GE', 'NE', 'PLUS', 'MINUS', 'TIMES', 'EQ', 'DIVIDE',
        'ASSIGN', 'LPARENT', 'RPARENT', 'COMMA', 'COLON', 'SEMICOLON', 'STRING',
        'RETURN', 'AND', 'OR', 'NOT', 'PRINT', 'BREAK', 'ELSE', 'SKIP', 
        'INT', 'FLOAT', 'INUMBER', 'FNUMBER', 'LBRACKET', 'RBRACKET'
    }

    # Ignorar espacios en blanco y tabulaciones
    ignore = ' \t'
    literals = '"_[]."_'
    
    # Expresiones regulares para tokens
    FUN = r'fun'
    # VAR = r'var'
    BEGIN = r'begin'
    END = r'end'
    RETURN = r'return'
    SKIP = r'skip'
    ELSE = r'else'
    BREAK = r'break'
    NOT = r'not'
    OR = r'or'
    AND = r'and'
    IF = r'if'
    INT = r'int'
    FLOAT = r'float'
    THEN = r'then'  
    WHILE = r'while'
    DO = r'do\b'
    PRINT = r'print'
    WRITE = r'\bwrite\b'
    READ = r'read'
    IDENT = r'[A-Za-z][A-Za-z0-9_]*'

    COMMENT = r'/\*(.|\n)*?\*/'
    LBRACKET = r'\['
    RBRACKET = r'\]'

    # Operadores y símbolos
    LE = r'<='
    GE = r'>='
    NE = r'<>'
    LT = r'<'
    GT = r'>'
    EQ = r'=='
    DF = r'!='
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r':='
    LPARENT = r'\('
    RPARENT = r'\)'
    COMMA = r','
    SEMICOLON = r';'
    COLON = r':'


    def __init__(self):
        super().__init__()
        self.lineno = 1

    @_(r'\d+\.\d+')
    def FNUMBER(self, t):
        t.value = float(t.value)
        t.lineno = self.lineno
        return t

    @_(r'\d+')
    def INUMBER(self, t):
        t.value = int(t.value)
        t.lineno = self.lineno
        return t
    
    # Manejo de saltos de línea (contador de líneas)
    @_(r'\n+')
    def NEWLINE(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\s*"[^"\\]*(\\.[^"\\]*)*"\s*')
    def STRING(self, t):
        t.value = t.value.strip('" \t\n\r')  # Elimina espacios en blanco y comillas alrededor de la cadena
        t.lineno = self.lineno
        return t

    # Expresión regular para caracteres escapados en cadenas
    @_(r'\\[nrt"\\\\]')
    def ESCAPE(self, t):
        if t.value == r'\\':
            t.value = '\\'
        elif t.value == r'\n':
            t.value = '\n'
        elif t.value == r'\r':
            t.value = '\r'
        elif t.value == r'\t':
            t.value = '\t'
        elif t.value == r'\"':
            t.value = '\"'
        return t

    def COMMENT(self, t):
        self.lineno += t.value.count('\n')
        return None
    

    def error(self, t):
        print(f"Lexer error: Unexpected character '{t.value[0]}' at line {self.lineno}")
        self.index += 1 
        return None

def print_lexer(tokens):
    console = Console()

    if isinstance(tokens, str):
       
        lexer = Lexer()
        tokens = list(lexer.tokenize(tokens))

   
    table = Table(title="Token Information")
    table.add_column("Type", style="cyan")
    table.add_column("Value", style="magenta")
    table.add_column("Line Number", style="yellow")

    
    for tok in tokens:
        table.add_row(str(tok.type), str(tok.value), str(tok.lineno))

    console.print(table)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} filename")
        exit(1)

    filename = sys.argv[1]
    with open(filename, 'r') as file:
        text = file.read()

    lexer_sly = Lexer()

    tokens = list(lexer_sly.tokenize(text))

    print_lexer(tokens)


if __name__ == '__main__':
    main()




