'''
this function will return a structure object from the parse tree
'''
import ast
from _ast import Add
from _ast import Sub
from _ast import Mult
from _ast import Div
from _ast import Mod
from _ast import Pow
from _ast import LShift
from _ast import RShift
from _ast import BitOr
from _ast import BitXor
from _ast import BitAnd
from _ast import FloorDiv
from _ast import If
from _ast import Eq
from _ast import NotEq
from _ast import Lt
from _ast import LtE
from _ast import Gt
from _ast import GtE
from _ast import Is
from _ast import IsNot
from _ast import In
from _ast import NotIn
from _ast import And
from _ast import Or
from _ast import Invert
from _ast import Not
from _ast import UAdd
from _ast import USub
from _ast import Name


BINOP_SYMBOLS = {}
BINOP_SYMBOLS[Add] = '+'
BINOP_SYMBOLS[Sub] = '-'
BINOP_SYMBOLS[Mult] = '*'
BINOP_SYMBOLS[Div] = '/'
BINOP_SYMBOLS[Mod] = '%'
BINOP_SYMBOLS[Pow] = '**'
BINOP_SYMBOLS[LShift] = '<<'
BINOP_SYMBOLS[RShift] = '>>'
BINOP_SYMBOLS[BitOr] = '|'
BINOP_SYMBOLS[BitXor] = '^'
BINOP_SYMBOLS[BitAnd] = '&'
BINOP_SYMBOLS[FloorDiv] = '//'

CMPOP_SYMBOLS = {}
CMPOP_SYMBOLS[Eq] = '=='
CMPOP_SYMBOLS[NotEq] = '!='
CMPOP_SYMBOLS[Lt] = '<'
CMPOP_SYMBOLS[LtE] = '<='
CMPOP_SYMBOLS[Gt] = '>'
CMPOP_SYMBOLS[GtE] = '>='
CMPOP_SYMBOLS[Is] = 'is'
CMPOP_SYMBOLS[IsNot] = 'is not'
CMPOP_SYMBOLS[In] = 'in'
CMPOP_SYMBOLS[NotIn] = 'not in'

BOOLOP_SYMBOLS = {}
BOOLOP_SYMBOLS[And] = 'and'
BOOLOP_SYMBOLS[Or] = 'or'

UNARYOP_SYMBOLS = {}
UNARYOP_SYMBOLS[Invert] = '~'
UNARYOP_SYMBOLS[Not] = 'not'
UNARYOP_SYMBOLS[UAdd] = '+'
UNARYOP_SYMBOLS[USub] = '-'


def get_children(node):
    return [x for x in ast.iter_child_nodes(node)]


class PathGen(object):

    def __init__(self, ast_node):
        self.identation = 0
        self.ast = ast_node

    def debug(self, str):
        debug = False
        if(debug):
            print str

    def get_paths(self):
        '''
        API
        :return: paths list
        '''
        return self.print_node(self.ast)

    def print_node_string(self, node):
        self.ident_with = "    "
        self.identation = 0
        result = ""
        nodes = self.print_node(node)
        for n in nodes:
            result += (n+"\n")
        return result

    def format_line(self, str):
        return self.ident_with * self.identation + str

    # this call will go through the child node and returns the structure
    def print_node(self, node):
        if hasattr(node, "body"):
            method = 'visit_' + node.__class__.__name__
            result = getattr(self, method)
            return result(node)
        else:
            if node.__class__.__name__ == 'Expr':
                return self.visit_Expr(node)
            else:
                return node

    def body(self, nodes):
        self.identation += 1
        result = []
        for node in nodes:
            result.append(self.print_node(node))
        self.identation -= 1
        return result

    def visit_Module(self, node):
        result = {}
        children = get_children(node)
        for child in children:
            if(child.__class__.__name__ == "ClassDef"):
                child_result = self.print_node(child)
                result.update(child_result)
        return result

    def visit_ClassDef(self, node):
        value = []
        for b in self.body(node.body):
            value.append(b)
        return {node: value}

    def visit_FunctionDef(self, node):
        result = []
        for b in self.body(node.body):
            if(isinstance(b, list)):
                for ele in b:
                    ele = result+ele
                result = b
            else:
                result.append(b)
        return (node, result)

    def visit_If(self, node):
        result = []
        r = [node]
        for b in self.body(node.body):
            r.append(b)
        result.append(r)

        if(len(node.orelse) == 0):
                pass
        elif len(node.orelse) == 1 and isinstance(node.orelse[0], If):
            node_el = node.orelse[0]
            for b in self.visit_If(node_el):
                result.append(b)
        else:
            # print node.orelse[0]
            r = []
            for b in self.body(node.orelse):
                r.append(b)
            result.append(r)
        return result

    def visit_Expr(self, node):
        return node.value
