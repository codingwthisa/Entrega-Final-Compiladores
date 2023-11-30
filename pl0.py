# pl0.py
'''
usage: pl0.py [-h] [-d] [-o OUT] [-l] [-D] [-p] [-I] [--sym] [-S] [-R] input

Compiler for PL0

positional arguments:
  input              PL0 program file to compile

optional arguments:
  -h, --help         show this help message and exit
  -D, --debug        Generate assembly with extra information (for debugging purposes)
  -o OUT, --out OUT  File name to store generated executable
  -l, --lex          Store output of lexer
  -d, --dot          Generate AST graph as DOT format
  -p, --png          Generate AST graph as png format
  -I, --ir           Dump the generated Intermediate representation
  --sym              Dump the symbol table
  -S, --asm          Store the generated assembly file
  -R, --exec         Execute the generated program
'''
from contextlib import redirect_stdout
from rich       import print

from plex       import Lexer, print_lexer
from pparser     import Parser
from context    import Context
from ASTree     import *

import argparse


def parse_args():
  cli = argparse.ArgumentParser(
    prog='pl0.py',
    description='Compiler for PL0 programs')

  cli.add_argument(
    '-v', '--version',
    action='version',
    version='0.1')

  fgroup = cli.add_argument_group('Formatting options')

  fgroup.add_argument(
    'input',
    type=str,
    nargs='?',
    help='PL0 program file to compile')

  mutex = fgroup.add_mutually_exclusive_group()

  mutex.add_argument(
    '-l', '--lex',
    action='store_true',
    default=False,
    help='Store output of lexer')

  mutex.add_argument(
    '-d', '--dot',
    action='store_true',
    default=False,
    help='Generate AST graph as DOT format')

  mutex.add_argument(
    '-p', '--png',
    action='store_true',
    help='Generate AST graph as png format')

  mutex.add_argument(
    '--sym',
    action='store_true',
    help='Dump the symbol table')

  return cli.parse_args()


if __name__ == '__main__':

  args = parse_args()
  context = Context()

  if args.input: fname = args.input

  with open(fname, encoding='utf-8') as file:
    source = file.read()

  if args.lex:
    flex = fname.split('.')[0] + '.lex'
    print(f'print lexer: {flex}')
    with open(flex, 'w', encoding='utf-8') as f:
      with redirect_stdout(f):
        print_lexer(source)

  elif args.dot or args.png:
    ast_instance = AST(Program)
    ast_instance.visit(Program)
    ast_tree = ast_instance.get_ast()
    dot = ast.to_dot()
    base = fname.split('.')[0]

    if args.dot:
      fdot = base + '.dot'
      print(f'print ast: {fdot}')
      with open(fdot, 'w') as f:
        with redirect_stdout(f):
          print(dot)

    elif args.png:
      ...

    else:
      context.parse(source)
      context.run()

  else:

    try:
      while True:
        source = input('pl0 $ ')
        context.parse(source)
        if not context.have_errors:
          for stmt in context.ast.stmts:
            context.ast = stmt
            context.run()

    except EOFError:
      pass

