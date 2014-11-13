import ast
from ..exceptions import *
from ..StructGen.StructGen import PathGen

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

    def get_paths(self):
        '''
        Based on ast tree, get all paths from it
        :return: paths list
        # each path is a list of ast node
        '''
        self.paths = PathGen(self.ast).get_paths()
        return self.paths
