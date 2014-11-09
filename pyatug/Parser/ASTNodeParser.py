import ast
from ..exceptions import *

# Base Parser
class __ASTNodeParser(object):
    '''
    Based on AST node, parse useful informations
    methods:
        - get_paths
    '''
    def __init__(self, ast_node):
        if not isinstance(ast_node, ast.AST):
            raise WrongTypeError('Need to input a ast node instance.')
        else:
            self.ast = ast_node
